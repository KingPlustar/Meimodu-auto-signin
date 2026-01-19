import random
from time import sleep

from meimo_crawler import MeimoaiCrawler


def bai_piao(meimo: MeimoaiCrawler) -> None:
    if not meimo.connect():
        meimo.logger.error("连接出错，程序终止。")
        return
    
    # 进行登录获取 token
    sleep(random.uniform(1, 3))
    if not meimo.login():
        meimo.logger.error("登录出错，程序终止。")
        return
    
    # 获取用户信息，记录当前电量
    sleep(random.uniform(1, 2))
    user_info = meimo.get_user_info()
    if user_info is None:
        meimo.logger.warning("获取用户信息出错，取消电量对比")
    else:
        meimo.logger.info(f"用户昵称：{user_info.nickname}，当前电量：{user_info.balance}。")
    
    # 执行签到
    sleep(random.uniform(1, 3))
    if not meimo.sign_in():
        meimo.logger.error("签到出错，程序终止。")
        return
    
    # 再次获取用户信息，检查电量是否增加
    sleep(random.uniform(1, 2))
    user_info_after = meimo.get_user_info()
    if user_info is None:
        if user_info_after is not None:
            meimo.logger.info(f"签到后电量：{user_info_after.balance}，无法对比签到前电量")
    elif user_info_after is None:
        meimo.logger.warning("获取用户信息出错，取消电量对比")
    else:
        delta_balance = user_info_after.balance - user_info.balance
        meimo.logger.info(f"签到前电量：{user_info.balance}，签到后电量：{user_info_after.balance}，增加电量：{delta_balance}。")
        if delta_balance <= 0:
            meimo.logger.warning("签到后电量未增加，检查是否重复签到")
    
    meimo.logger.info("程序执行完毕。")


if __name__ == "__main__":
    meimo = MeimoaiCrawler()
    meimo.logger.info("程序开始执行")
    
    try:
        bai_piao(meimo)
    except Exception as e:
        meimo.logger.error(f"程序执行异常终止，可能是程序已过时！")
        meimo.logger.exception(e)