from typing import Annotated, Literal

import uvicorn
from fastapi import FastAPI, Form
from pydantic import Field, SecretStr
from starlette.responses import HTMLResponse

from dainty import DaintyExtras, DaintyForm, DaintyModel

app = FastAPI()


class FormData(DaintyModel):
    name: str = Field(min_length=2, max_length=50)
    nationality: Literal["US", "UK", "IN", "AU", "CA"] = Field(
        json_schema_extra=DaintyExtras(dainty_select_type="multiselect").model_dump()
    )

    hobbies: list[Literal["reading", "writing", "coding", "singing"]] = Field(
        json_schema_extra=DaintyExtras(dainty_select_type="checkbox").model_dump()
    )
    age: int = Field(ge=18, le=100)
    username: str = Field(min_length=3, max_length=50)
    password: SecretStr = Field(min_length=8, max_length=50)

    dainty_form = DaintyForm()


@app.post("/signup")
async def api_login(data: Annotated[FormData, Form()]):
    print(data)
    return HTMLResponse("Login successful")


@app.get("/signup")
async def login():
    return HTMLResponse(str(FormData.to_html(form=True)))


if __name__ == "__main__":
    uvicorn.run(app)
