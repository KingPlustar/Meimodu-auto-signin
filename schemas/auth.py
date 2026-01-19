from pydantic import BaseModel, Field


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
    
    
class UserData(BaseModel):
    id: int
    email: str
    nickname: str
    balance: float # 电量余额