from typing import Any, Literal

from pydantic import BaseModel, TypeAdapter


class DataResponse[T](BaseModel):
    code: Literal[200]
    data: T
    message: str
    
    
class MsgResponse(BaseModel):
    code: int
    message: str
    

type Resp[T] = DataResponse[T] | MsgResponse


def parse_resp[T](data: Any, data_type: type[T]) -> Resp[T]:
    """
    使用 discriminated union 自动根据 "code" 字段解析 API 响应。
    即使拥有 data 字段，但 code 不为 200，同样会被自动解析为 MsgResponse。
    
    当 code == 200 时返回 DataResponse[T]，否则返回 MsgResponse。
    配合 match-case 或 isinstance 使用即可免去手动判断 code 并手动转化模型的分支代码。
    
    该功能适用于需要强制自己在处理正确响应时考虑错误响应的情况。
    如果只需要单独处理 DataResponse 或 MsgResponse 则无需使用此方法。

    :param data: API 返回的 JSON 反序列化后的 dict 对象
    :type data: Any
    :param data_type: DataResponse.data 字段的类型，例如 LoginData、bool
    :type data_type: type[T]
    :return: 成功时为 DataResponse[T]，失败时为 MsgResponse
    :rtype: Resp[T]
    """
    return TypeAdapter(Resp[data_type]).validate_python(data)
