from pydantic import BaseModel, Field, EmailStr
from pydantic_core import ValidationError


class ContactForm(BaseModel):
    username: str = Field(min_length=2, max_length=24)
    email: EmailStr = Field(...)
    message: str = Field(max_length=256)


def pyform(data):
    try:
        contact_form = ContactForm(**data)
    except ValidationError as e:
        errors = e.errors()
        for error in errors:
            field = error['loc'][0]
            return f'Your {field} is invalid! Please Try Again'
    else:
        return contact_form.model_dump()
    
