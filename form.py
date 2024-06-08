from traceback import print_exc

from pydantic import BaseModel, Field, EmailStr
from pydantic_core import ValidationError


class ContactForm(BaseModel):
    username: str = Field(min_length=2, max_length=24)
    email: EmailStr = Field(...)
    message: str = Field(max_length=256)


def pyform(data):
    try:
        return ContactForm.model_validate(obj=data).model_dump()
    except ValidationError as e:
        print_exc()
        return f'Your {", ".join(err["loc"][0] for err in e.errors())} is invalid! Please Try Again'
