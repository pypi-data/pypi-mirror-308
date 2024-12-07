from typing import Literal, Optional

from pydantic import Field

from dainty import DaintyModel
from dainty.dainty import DaintyExtras, DaintyForm, Number


class Parent(DaintyModel):
    name: str
    age: int


class MyModel(DaintyModel):
    name: str
    age: Number = Field(gt=17, lt=41, description="Age must be between 18 and 40")
    gender: Literal["Male", "Female", "Non Binary", "Other"] = Field(
        "Other", json_schema_extra=DaintyExtras(dainty_select_type="radio").model_dump()
    )
    origin: Optional[Literal["Earth", "Mars", "Venus"]] = None
    parent: Parent

    dainty_form = DaintyForm(target_url="/submit")


html = MyModel.to_html(form=True)

# print(html)
