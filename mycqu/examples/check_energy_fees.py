from mycqu.auth import login, NeedCaptcha
from mycqu.card import access_card
from mycqu.card.models.energy_fees import EnergyFees
from requests import Session
import argparse

def check_energy_fees(username: str = "27130525", 
                     password: str = "bdsc11081bdsc", 
                     room: str = "ea548", 
                     is_huxi: bool = True):
    """查询宿舍电费

    Args:
        username (str): 统一身份认证用户名
        password (str): 统一身份认证密码
        room (str): 宿舍房间号
        is_huxi (bool): 是否是虎溪校区
    """
    session = Session()
    
    # 登录统一身份认证
    try:
        login(session, username, password)
    except NeedCaptcha as e:
        with open("captcha.jpg", "wb") as file:
            file.write(e.image)
        print("请查看 captcha.jpg 并输入验证码: ", end="")
        e.after_captcha(input())
    
    # 访问一卡通系统
    access_card(session)
    
    # 获取电费信息
    try:
        fees = EnergyFees.fetch(session, is_huxi, room)
        print(f"\n{'='*20} 电费查询结果 {'='*20}")
        print(f"房间号: {room}")
        print(f"账户余额: {fees.balance:.2f} 元")
        
        if is_huxi:
            if fees.electricity_subsidy is not None:
                print(f"电剩余补助: {fees.electricity_subsidy:.2f} 元")
            if fees.water_subsidy is not None:
                print(f"水剩余补助: {fees.water_subsidy:.2f} 元")
        else:
            if fees.subsidies is not None:
                print(f"补贴余额: {fees.subsidies:.2f} 元")
        print('='*50)
    except Exception as e:
        print(f"查询失败: {str(e)}")

if __name__ == "__main__":
    # 直接运行查询
    check_energy_fees()