from pydantic import BaseModel,EmailStr

class LoginUser(BaseModel):
    username: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    refresh_tokenL: str
    token_type: str

class ReturnUser(BaseModel):
    username: str
    isactive:bool



