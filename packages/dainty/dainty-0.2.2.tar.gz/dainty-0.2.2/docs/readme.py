from typing import Literal

from dainty import DaintyModel


class MyModel(DaintyModel):
    name: str
    age: int
    gender: Literal["Male", "Female", "Non Binary", "Other"]


print(MyModel.to_html(form=True))
