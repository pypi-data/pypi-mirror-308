import warnings
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import EnumType
from pathlib import Path
from typing import Any, ClassVar, Literal, get_origin
from uuid import UUID

import pyhtml as p
from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr
from pydantic.config import JsonDict
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

UUID_PATTERN = "[0-9a-fA-F]{{8}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{4}}-[0-9a-fA-F]{{12}}"

with open(Path(__file__).parent / "static" / "style.css") as f:
    CSS = f.read()


class DaintyParsingWarning(UserWarning):
    pass


type Number = int | float


@dataclass
class Constraints:
    min_length: str = ""
    max_length: str = ""
    pattern: str = ""
    gt: Number | None = None
    lt: Number | None = None
    ge: Number | None = None
    le: Number | None = None


@dataclass
class ExtraMetadata:
    description: str = ""


class DaintyExtras(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    dainty_type: Literal["radio"]


@dataclass
class DaintyForm:
    form_id: str = ""
    action: str = "post"
    target_url: str | None = None


class DaintyModel(BaseModel):
    model_config = ConfigDict(ignored_types=(DaintyForm,))

    root: ClassVar[p.Tag]
    dainty_form = DaintyForm()

    @classmethod
    def to_html(cls, form: bool = False):
        """
        Generate HTML elements for the model fields.

        Args:
            form (bool): If True, wrap the fields in a form tag and add a button at the end.
        """

        cls._create_root(form)

        for key, field in cls.model_fields.items():
            cls.root.children.append(cls._generate_field_html(key, field))

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
    def _generate_field_html(cls, key: str, field: FieldInfo):
        annotation = field.annotation
        default = "" if field.default is PydanticUndefined else field.default
        required = field.is_required()
        field_html = p.label(f"{key.title()}: ", for_=key)

        dainty_extras = {}
        if json_schema_extra := field.json_schema_extra:
            for key, value in json_schema_extra.items():
                if key.startswith("dainty_"):
                    dainty_extras[key] = value

        constraints, extra = cls._extract_metadata(field.metadata)

        field_html.children.append(
            cls._generate_input_html(
                key,
                annotation,
                default,
                required,
                constraints,
                dainty_extras,
            )
        )

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
        dainty_extras: JsonDict,
    ) -> p.Tag | None:
        if get_origin(annotation) is Literal:
            return cls._generate_select_html(
                key, annotation.__args__, default, required
            )

        if isinstance(annotation, EnumType):
            return cls._generate_select_html(
                key, [item.value for item in annotation], default, required
            )

        type_map = {
            int: cls._generate_number_html,
            float: cls._generate_number_html,
            Decimal: cls._generate_number_html,
            str: cls._generate_text_html,
            bool: cls._generate_checkbox_html,
            date: cls._generate_date_html,
            time: cls._generate_time_html,
            datetime: cls._generate_datetime_html,
            EmailStr: cls._generate_email_html,
            SecretStr: cls._generate_password_html,
            UUID: cls._generate_uuid_html,
        }

        if annotation in type_map:
            return type_map[annotation](key, default, required, constraints)
        try:
            if issubclass(annotation, DaintyModel):
                return annotation.to_html()
        except TypeError:
            pass

        warnings.warn(f"Unsupported type {annotation}", DaintyParsingWarning)

        return

    @classmethod
    def _generate_select_html(cls, key, options, default, required):
        options_html = [cls._create_option(option, default) for option in options]

        return p.select(options_html, name=key, id=key, required=required)

    @staticmethod
    def _create_option(option, default):
        selected = True if option == default else False
        return p.option(option, value=option, selected=selected)

    @staticmethod
    def _generate_number_html(key, default: Number, required: bool, constraints):
        min_val = (
            constraints.ge
            if constraints.ge is not None
            else constraints.gt + 1
            if constraints.gt is not None
            else ""
        )
        max_val = (
            constraints.le
            if constraints.le is not None
            else constraints.lt - 1
            if constraints.lt is not None
            else ""
        )
        step = "0.01" if isinstance(default, float) else "1"

        return p.input(
            type_="number",
            name=key,
            id=key,
            value=str(default),
            step=step,
            min=min_val,
            max=max_val,
            required=required,
        )

    @staticmethod
    def _generate_text_html(key, default, required: bool, constraints):
        min_length = (
            f"minlength='{constraints.min_length}'" if constraints.min_length else ""
        )
        max_length = (
            f"maxlength='{constraints.max_length}'" if constraints.max_length else ""
        )
        pattern = f"pattern='{constraints.pattern}'" if constraints.pattern else ""
        return p.input(
            type_="text",
            name=key,
            id=key,
            value=default,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            required=required,
        )

    @staticmethod
    def _generate_checkbox_html(key, default, *_):
        checked = "checked" if default else ""
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
