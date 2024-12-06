import uuid
from datetime import date, datetime, time
from decimal import Decimal
from enum import StrEnum
from typing import Literal, Optional
from uuid import UUID

import pytest
from pydantic import EmailStr, Field, HttpUrl, SecretStr

from dainty.dainty import DaintyModel, DaintyExtras, DaintyParsingWarning


class Gender(StrEnum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non binary"
    OTHER = "Other"


class UserType(StrEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Parent(DaintyModel):
    name: str
    age: int


class Person(DaintyModel):
    name: str = Field(
        ..., min_length=2, max_length=50, description="Full name of the person"
    )
    email: EmailStr
    password: SecretStr
    gender: Gender
    age: int = Field(gt=17, lt=41, description="Age must be between 18 and 40")
    birth_date: date
    website: Optional[HttpUrl] = None
    user_type: UserType = Field(default=UserType.USER)
    balance: Decimal = Field(ge=0, default=0)
    active: bool = True
    login_time: time = Field(default=time(9, 0))
    last_login: datetime = Field(default=datetime.now())
    user_id: UUID = Field(default_factory=uuid.uuid4)
    country: Literal["US", "UK", "NZ"] = Field(
        json_schema_extra=DaintyExtras(dainty_type="radio").model_dump()
    )
    parent: Parent


def test_dainty_to_html():
    with pytest.warns(DaintyParsingWarning):
        with open("dainty.html", "w") as f:
            f.write(Person.to_html())


if __name__ == "__main__":
    test_dainty_to_html()
