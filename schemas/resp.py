from pydantic import BaseModel


class BaseResponse[T](BaseModel):
    code: int
    data: T
    message: str
    
    
class MessageResponse(BaseModel):
    code: int
    message: str