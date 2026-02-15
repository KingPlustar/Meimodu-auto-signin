from typing import Annotated
from pydantic import AfterValidator, BaseModel, TypeAdapter

from config import UserConfig


def anonymous(name: str) -> str:
    try:
        if not TypeAdapter(bool).validate_strings(UserConfig.ANONYMOUS):
            return name
        
        name_len = len(name)
        if name_len <= 1:
            return '*'
        if name_len == 2:
            return name[0] + '*'
        return name[0] + ('*' * (name_len - 2)) + name[-1]
    except Exception:
        return name
    

class LoginInfo(BaseModel):
    username: str
    password: str = ""
    code: str = ""
    deviceId: str = ""
    inviteCode: str = ""


class LoginData(BaseModel):
    token: str
    id: int
    email: str
    nickname: Annotated[str, AfterValidator(anonymous)]
    gender: int
    password: str


class UserData(BaseModel):
    id: int
    email: str
    nickname: Annotated[str, AfterValidator(anonymous)]
    balance: float # 电量余额
