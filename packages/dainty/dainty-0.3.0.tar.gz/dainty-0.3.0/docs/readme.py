from typing import Literal

from pydantic import Field

from dainty import DaintyModel
from dainty.dainty import DaintyForm


class MyModel(DaintyModel):
    name: str
    age: int = Field(ge=20, lt=40)
    gender: Literal["Male", "Female", "Non Binary", "Other"]

    dainty_form = DaintyForm(target_url="/submit")


print(MyModel.to_html(form=True))
