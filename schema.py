from pydantic import BaseModel , EmailStr , Field

class UserSchema(BaseModel):
    name : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    age : int = Field(default=None)


class UserLoginSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)


