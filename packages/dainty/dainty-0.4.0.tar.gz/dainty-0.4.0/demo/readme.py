from typing import Literal

from pydantic import Field

from dainty import DaintyModel
from dainty.dainty import DaintyForm


class Parent(DaintyModel):
    name: str
    age: int


class MyModel(DaintyModel):
    name: str
    age: int = Field(gt=17, lt=41, description="Age must be between 18 and 40")
    gender: Literal["Male", "Female", "Non Binary", "Other"] = "Other"
    parent: Parent

    dainty_form = DaintyForm(target_url="/submit")


html = MyModel.to_html(form=True)

print(html)
