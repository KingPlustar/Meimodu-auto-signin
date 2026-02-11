from pydantic import BaseModel, TypeAdapter, field_validator

from config import UserConfig


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
    nickname: str
    gender: int
    password: str

    @field_validator('nickname', mode='after')
    @classmethod
    def anonymous(cls, name: str) -> str:
        try:
            if TypeAdapter(bool).validate_strings(UserConfig.ANONYMOUS):
                name_len = len(name)
                if name_len <= 1:
                    return '*'
                if name_len == 2:
                    return name[0] + '*'
                return name[0] + ("*" * (name_len - 2)) + name[-1]
            return name
        except Exception:
            return name


class UserData(BaseModel):
    id: int
    email: str
    nickname: str
    balance: float # 电量余额
