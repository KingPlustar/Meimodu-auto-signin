from typing import TypedDict


class RequestConfig(TypedDict):
    """请求配置"""
    timeout: int
    headers: dict[str, str]


ApiEndpoints = TypedDict('ApiEndpoints', {
    'login': str,
    'sign-in': str,
    'info': str,
})


class ApiConfig(TypedDict):
    """API配置"""
    base_url: str
    endpoints: ApiEndpoints
    