import cloudscraper
from requests import Response, Session
from requests.exceptions import ConnectionError

from config import API_CONFIG, REQUEST_CONFIG, TARGET_URL, UserConfig
from meimo_logger import setup_logger
from schemas.auth import LoginInfo, LoginData, UserData
from schemas.resp import BaseResponse


class MeimoaiAPI:
    def __init__(self) -> None:
        self.base_url = API_CONFIG["base_url"]
        self.login_endpoint = API_CONFIG["endpoints"]["login"]
        self.sign_in_endpoint = API_CONFIG["endpoints"]["sign-in"]
        self.info_endpoint = API_CONFIG["endpoints"]["info"]
        
        self.timeout = REQUEST_CONFIG.get("timeout", 10)
        
        
    def login(self, session: Session) -> Response:
        url = f"{self.base_url}{self.login_endpoint}"

        data = LoginInfo(
            username=UserConfig.EMAIL,
            password=UserConfig.PASSWORD
        )

        response = session.post(url, json=data.model_dump(), timeout=self.timeout)

        return response
    
    
    def sign_in(self, session: Session) -> Response:
        url = f"{self.base_url}{self.sign_in_endpoint}"

        response = session.post(url, timeout=self.timeout)

        return response
    
    
    def get_user_info(self, session: Session) -> Response:
        url = f"{self.base_url}{self.info_endpoint}"

        response = session.post(url, timeout=self.timeout)
        
        return response


class MeimoaiCrawler:
    def __init__(self) -> None:
        self.api = MeimoaiAPI()
        self.session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',      # 指定为 Chrome
                'platform': 'windows',    # Windows 平台
                'mobile': False,          # 桌面版
                'desktop': True,          # 桌面模式
            }
        )
        
        self.logger = setup_logger()
        self.default_headers: dict = {k: v for k, v in REQUEST_CONFIG.get("headers", {}).items() if v}
    
    
    def has_authorized(self) -> bool:
        auth_header = self.session.headers.get("Authorization")
        return auth_header is not None and auth_header.strip() != ""
        
        
    def connect(self, apply_headers_config: bool = True, test_connection: bool = True) -> bool:
        if apply_headers_config:
            self.session.headers.update({**self.default_headers, **self.session.headers})
        
        if not test_connection:
            return True
        
        try:
            response = self.session.get(TARGET_URL, timeout=self.api.timeout)
            self.logger.info(f"成功连接到 {TARGET_URL}")

            if response.status_code == 200:
                return True
            
            self.logger.error(f"无法正确连接到 {TARGET_URL}，状态码：{response.status_code}，响应内容：\n{response.text}")
        except ConnectionError as e:
            self.logger.error(f"测试连接到 {TARGET_URL} 失败，请检查网络连接配置: \n{e}")
            
        return False
        
        
    def login(self) -> bool:
        """
        登录以获取 token，并更新 session 的 Authorization 头。
        经测试自己抓包 Authorization 字段直接填上后貌似无法直接使用，可能和会话存储有关？

        :return: 登录是否成功
        :rtype: bool
        """
        if self.has_authorized():
            self.logger.info("已存在有效的授权信息，跳过登录步骤。")
            return True
        
        response = self.api.login(self.session)
        
        if response.status_code != 200:
            self.logger.error(f"登录失败，状态码：{response.status_code}，目标url：{response.url}，响应内容：\n{response.text}")
            return False
        
        response_json = response.json()
        if response_json.get("code") != 200:
            self.logger.error(f"登录失败，目标url：{response.url}，响应内容：\n{response.text}")
            return False
        
        login_response = BaseResponse[LoginData].model_validate(response_json)
        self.logger.info(f"登录成功，用户昵称：{login_response.data.nickname}")
        self.session.headers.update({
            "Authorization": login_response.data.token
        })
        return True
            
            
    def sign_in(self) -> bool:
        """
        签到逻辑

        :return: 签到是否成功
        :rtype: bool
        """
        response = self.api.sign_in(self.session)
        
        if response.status_code != 200:
            self.logger.error(f"签到失败，状态码：{response.status_code}，目标url：{response.url}，响应内容：\n{response.text}")
            print(f"\n{self.session.headers = }\n\n{self.session.cookies = }")
            return False
        
        response_json = response.json()
        if response_json.get("code") != 200:
            self.logger.error(f"签到失败，目标url：{response.url}，响应内容：\n{response.text}")
            return False
        
        sign_in_response = BaseResponse[bool].model_validate(response.json())
        self.logger.info(f"签到成功，响应内容：\n{sign_in_response.model_dump_json(indent=2)}")
        return True
        
        
    def get_user_info(self) -> UserData | None:
        """
        获取用户信息，用来计算签到后电量是否增加

        :return: 返回为 None 说明获取失败
        :rtype: UserData | None
        """
        response = self.api.get_user_info(self.session)

        if response.status_code != 200:
            self.logger.error(f"获取用户信息失败，状态码：{response.status_code}，目标url：{response.url}，响应内容：\n{response.text}")
            return None
        
        response_json = response.json()
        if response_json.get("code") != 200:
            self.logger.error(f"获取用户信息失败，目标url：{response.url}，响应内容：\n{response.text}")
            return None
        
        user_info_response = BaseResponse[UserData].model_validate(response.json())
        self.logger.info(f"获取用户信息成功")
        return user_info_response.data