import warnings
from dataclasses import dataclass
from datetime import date, datetime, time
from enum import EnumType
from pathlib import Path
from types import UnionType
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    TypeAliasType,
    Union,
    get_args,
    get_origin,
)
from uuid import UUID

import pyhtml as p
from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, model_validator
from pydantic.config import JsonDict
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

UUID_PATTERN = "[0-9a-fA-F]{{8}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{12}}"

with open(Path(__file__).parent / "static" / "style.css") as f:
    CSS = f.read()


class DaintyParsingWarning(UserWarning):
    pass


type Number = int | float

type DaintySelectOne = Literal["radio", "select"]
type DaintySelectMany = Literal["checkbox", "multiselect"]
type DaintySelectType = Union[DaintySelectOne, DaintySelectMany]


@dataclass
class Constraints:
    min_length: str | None = None
    max_length: str | None = None
    pattern: str | None = None
    gt: int | None = None
    lt: int | None = None
    ge: int | None = None
    le: int | None = None


@dataclass
class ExtraMetadata:
    description: str = ""


class DaintyExtras(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    dainty_select_type: Optional[DaintySelectType] = None

    @model_validator(mode="before")
    def validate_fields(cls, data):
        for key in data:
            if not key.startswith("dainty_"):
                raise DaintyExtrasValidationError("Field names must start with dainty_")

        return data


class DaintyExtrasValidationError(ValueError):
    pass


@dataclass
class DaintyForm:
    form_id: str = ""
    action: str = "post"
    target_url: str | None = None


class DaintyModel(BaseModel):
    model_config = ConfigDict(ignored_types=(DaintyForm,))
    dainty_form = DaintyForm()

    root: ClassVar[p.Tag]

    @classmethod
    def to_html(cls, form: bool = False):
        """
        Generate HTML elements for the model fields.

        Args:
            form (bool): If True, wrap the fields in a form tag and add a button at the end.
        """

        cls._create_root(form)

        for key, field in cls.model_fields.items():
            cls.validate_dainty_field(key, field)
            cls.root.children.append(
                DaintyFieldGenerator._generate_field_html(key, field)
            )

        if form:
            cls.root.children.append(
                p.input(
                    type="submit",
                    value="Submit",
                    method=cls.dainty_form.action,
                    formaction=cls.dainty_form.target_url,
                )
            )
        return cls.root

    @classmethod
    def _create_root(cls, form: bool):
        if form:
            cls.root = p.form()
        else:
            cls.root = p.div()

        cls.root.attributes["class"] = "dainty-root"

        if form_id := cls.dainty_form.form_id:
            cls.root.attributes["id"] = form_id

        cls.root.children.append(p.style(CSS))

    @classmethod
    def validate_dainty_field(cls, key, field):
        return
        print(key, field)


class DaintyFieldGenerator:
    @classmethod
    def _generate_field_html(cls, key: str, field: FieldInfo):
        annotation = field.annotation
        default = "" if field.default is PydanticUndefined else field.default
        required = field.is_required()
        field_html = p.label(f"{key}: ", for_=key)

        dainty_extras = {}
        if json_schema_extra := field.json_schema_extra:
            for k, value in json_schema_extra.items():
                if k.startswith("dainty_"):
                    dainty_extras[k] = value

        dainty_extras = DaintyExtras(**dainty_extras)

        constraints, extra = cls._extract_metadata(field.metadata)

        input_html = cls._generate_input_html(
            key,
            annotation,
            default,
            required,
            constraints,
            dainty_extras,
        )
        if input_html:
            field_html.children.append(input_html)

        if extra.description:
            field_html.children.append(p.small(extra.description))

        return field_html

    @staticmethod
    def _extract_metadata(metadata: list[Any]) -> tuple[Constraints, ExtraMetadata]:
        constraints = Constraints()
        extra = ExtraMetadata()

        for constraint in metadata:
            if hasattr(constraint, "min_length"):
                constraints.min_length = constraint.min_length
            elif hasattr(constraint, "max_length"):
                constraints.max_length = constraint.max_length
            elif hasattr(constraint, "pattern"):
                constraints.pattern = constraint.pattern
            elif hasattr(constraint, "gt"):
                constraints.gt = constraint.gt
            elif hasattr(constraint, "lt"):
                constraints.lt = constraint.lt
            elif hasattr(constraint, "ge"):
                constraints.ge = constraint.ge
            elif hasattr(constraint, "le"):
                constraints.le = constraint.le
            elif hasattr(constraint, "description"):
                extra.description = constraint.description

        return constraints, extra

    @classmethod
    def _generate_input_html(
        cls,
        key: str,
        annotation,
        default,
        required: bool,
        constraints: Constraints,
        dainty_extras: DaintyExtras,
    ) -> p.Tag | None:
        """Generate HTML input element based on field type and attributes."""

        # Resolve type alias
        if type(annotation) is TypeAliasType:
            annotation = annotation.__value__

        # Determine if we're dealing with a complex type
        if origin := get_origin(annotation):
            return cls._handle_complex_type(
                key, annotation, origin, default, required, constraints, dainty_extras
            )

        return cls._handle_simple_type(key, annotation, default, required, constraints)

    @classmethod
    def _handle_simple_type(cls, key, annotation, default, required, constraints):
        """Handle basic types that don't need get_origin/get_args processing."""
        if isinstance(annotation, EnumType):
            return cls._generate_select_html(
                key, [item.value for item in annotation], default, required
            )

        # Handle nested DaintyModel
        try:
            if issubclass(annotation, DaintyModel):
                return annotation.to_html()
        except TypeError:
            pass

        # Handle basic types
        if handler := cls._get_type_handler(annotation):
            return handler(key, default, required, constraints)

        warnings.warn(
            f"Unsupported simple type: {annotation}",
            DaintyParsingWarning,
        )
        return None

    @classmethod
    def _handle_complex_type(
        cls, key, annotation, origin, default, required, constraints, dainty_extras
    ):
        """Handle complex types that need get_origin/get_args processing."""
        args = get_args(annotation)

        type_handlers = {
            Literal: cls._handle_literal_type,
            list: cls._handle_list_type,
            Union: cls._handle_union_type,
            UnionType: cls._handle_union_type,
        }

        if handler := type_handlers.get(origin):
            return handler(key, args, default, required, constraints, dainty_extras)

        warnings.warn(
            f"Unsupported complex type - origin: {origin}, args: {args}",
            DaintyParsingWarning,
        )
        return None

    @classmethod
    def _handle_union_type(
        cls, key, args, default, required, constraints, dainty_extras
    ):
        """Handle Union types including Optional and number unions."""
        # Handle Optional (Union with None)
        if len(args) == 2 and type(None) in args:
            non_none_type = next(arg for arg in args if arg is not type(None))
            return cls._generate_input_html(
                key, non_none_type, default, False, constraints, dainty_extras
            )

        # Handle number union (int | float)
        if set(args) == {float, int}:
            return cls._generate_number_html(key, default, required, constraints)

        warnings.warn(
            f"Unsupported Union type with args: {args}",
            DaintyParsingWarning,
        )
        return None

    @classmethod
    def _handle_literal_type(
        cls, key, args, default, required, constraints, dainty_extras
    ):
        """Handle Literal type annotations."""
        match dainty_extras.dainty_select_type:
            case "radio":
                return cls._generate_fieldset_html(
                    "radio", key, args, default, required
                )
            case "select":
                return cls._generate_select_html(key, args, default, required)
            case "checkbox" | "multiselect":
                raise ValueError("Checkbox or multiselect must be a list")

        return cls._generate_select_html(key, args, default, required)

    @classmethod
    def _handle_list_type(
        cls, key, args, default, required, constraints, dainty_extras
    ):
        """Handle list type annotations."""
        literal_values = [arg for args in args for arg in args.__args__]

        match dainty_extras.dainty_select_type:
            case "checkbox":
                return cls._generate_fieldset_html(
                    "checkbox", key, literal_values, default, required
                )
            case "multiselect":
                return cls._generate_select_html(
                    key, literal_values, default, required, multiple=True
                )
        return None

    @classmethod
    def _get_type_handler(cls, annotation):
        """Get the appropriate handler function for the given type."""
        type_map = {
            int: cls._generate_number_html,
            float: cls._generate_number_html,
            str: cls._generate_text_html,
            bool: cls._generate_checkbox_html,
            date: cls._generate_date_html,
            time: cls._generate_time_html,
            datetime: cls._generate_datetime_html,
            EmailStr: cls._generate_email_html,
            SecretStr: cls._generate_password_html,
            UUID: cls._generate_uuid_html,
        }
        return type_map.get(annotation)

    @classmethod
    def _generate_select_html(cls, key, options, default, required, multiple=False):
        options_html = [cls._create_option(option, default) for option in options]

        return p.select(
            options_html, name=key, id=key, required=required, multiple=multiple
        )

    @staticmethod
    def _create_option(option, default):
        selected = True if option == default else False
        return p.option(option, value=option, selected=selected)

    @classmethod
    def _generate_fieldset_html(cls, input_type, key, options, default, required):
        title = key
        fieldset = p.fieldset(p.legend(title), id=key)
        for n, option in enumerate(options):
            fieldset.children.append(
                p.label(
                    option,
                    p.input(
                        type_=input_type,
                        name=f"{title}",
                        id=f"{title}_{n}",
                        value=option,
                    ),
                    for_=f"{title}_{n}",
                )
            )

        return fieldset

    @staticmethod
    def _generate_number_html(
        key, default: int, required: bool, constraints: Constraints
    ):
        min_val = (
            constraints.ge
            if constraints.ge is not None
            else constraints.gt + 1
            if constraints.gt is not None
            else None
        )
        max_val = (
            constraints.le
            if constraints.le is not None
            else constraints.lt - 1
            if constraints.lt is not None
            else None
        )
        step = "0.01" if isinstance(default, float) else "1"

        return p.input(
            type_="number",
            name=key,
            id=key,
            value=str(default),
            step=step,
            min=str(min_val),
            max=str(max_val),
            required=required,
        )

    @staticmethod
    def _generate_text_html(key, default, required: bool, constraints: Constraints):
        return p.input(
            type_="text",
            name=key,
            id=key,
            value=default,
            minlength=constraints.min_length,
            maxlength=constraints.max_length,
            pattern=constraints.pattern,
            required=required,
        )

    @staticmethod
    def _generate_checkbox_html(key, default, *_):
        checked = "checked" if default else None
        return p.input(
            type_="checkbox",
            name=key,
            id=key,
            checked=checked,
        )

    @staticmethod
    def _generate_date_html(key, default, required: bool, *_):
        return p.input(
            type_="date",
            name=key,
            id=key,
            value=default,
            required=required,
        )

    @staticmethod
    def _generate_time_html(key, default, required, *_):
        return p.input(
            type_="time",
            name=key,
            id=key,
            value=default,
            required=required,
        )

    @staticmethod
    def _generate_datetime_html(key, default, required, *_):
        return p.input(
            type_="datetime-local",
            name=key,
            id=key,
            value=default,
            required=required,
        )

    @staticmethod
    def _generate_email_html(key, default, required, *_):
        return p.input(
            type_="email",
            name=key,
            id=key,
            value=default,
            required=required,
        )

    @staticmethod
    def _generate_password_html(key, default, required, *_):
        return p.input(
            type_="password",
            name=key,
            id=key,
            value=default,
            required=required,
        )

    @staticmethod
    def _generate_url_html(key, default, required, *_):
        return p.input(
            type_="url",
            name=key,
            id=key,
            value=default,
            required=required,
        )

    @staticmethod
    def _generate_uuid_html(key, default, required, *_):
        return p.input(
            type_="text",
            name=key,
            id=key,
            value=default,
            pattern=UUID_PATTERN,
            required=required,
        )
