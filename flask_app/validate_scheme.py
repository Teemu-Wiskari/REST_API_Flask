import pydantic
import requests as requests
from typing import Optional


class CreateUser(pydantic.BaseModel):
    """Валидация пользователя"""

    username: str
    password: str
    email: Optional[str] = 'missing@email'


    @pydantic.field_validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('password short!')
        return value


class PatchUser(pydantic.BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    @pydantic.field_validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('passwortd short!')

        return value


class CreateAd(pydantic.BaseModel):
    """Валидация рекламы"""

    user_id: int
    header: Optional[str] = 'made ad'
    description: Optional[str] = None

    @pydantic.field_validator('user_id')
    def validate_ad_owner(cls, value):
        url = f'http://localhost:5000/user/{value}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError('user not found...')
        return value


class PatchAd(pydantic.BaseModel):

    user_id: Optional[int] = None
    header: Optional[str] = None
    description: Optional[str] = None

    @pydantic.field_validator('user_id')
    def validate_ad_owner(cls, value):
        url = f'http://localhost:5000/user/{value}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError('user not found...')
        return value

