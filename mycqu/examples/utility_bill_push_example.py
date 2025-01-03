"""水电费推送示例

本示例展示了如何使用 mycqu.utils.wechat 模块推送水电费相关信息
"""
from datetime import datetime
from mycqu.utils.wechat import (
    initialize_wechat_push,
    send_wechat_message
)

def format_bill_message(electricity_fee: float, water_fee: float) -> str:
    """格式化水电费账单消息
    
    Args:
        electricity_fee: 电费金额
        water_fee: 水费金额
    
    Returns:
        str: 格式化后的Markdown消息
    """
    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    total_fee = electricity_fee + water_fee
    
    message = f"""
# 宿舍水电费账单提醒

**查询时间**：{current_time}

## 本月账单详情
- 电费：**¥{electricity_fee:.2f}**
- 水费：**¥{water_fee:.2f}**
- 总计：**¥{total_fee:.2f}**

> 温馨提示：
> 1. 余额不足时请及时充值，以免影响正常使用
> 2. 请节约用水用电，践行绿色环保理念
"""
    return message

def demo_utility_bill_push():
    """水电费推送示例"""
    # 首先需要在 https://sct.ftqq.com/ 获取你的 PUSH_KEY
    PUSH_KEY = "SCT42439TQD7Vua2vPAEprxKx7NdLFlOM"  # 替换为你的 PUSH_KEY
    
    # 初始化微信推送
    initialize_wechat_push(PUSH_KEY)
    
    # 模拟水电费数据（实际使用时替换为真实数据）
    electricity_fee = 35.60  # 电费
    water_fee = 12.80       # 水费
    
    # 格式化消息内容
    message_content = format_bill_message(electricity_fee, water_fee)
    
    # 发送消息
    send_wechat_message("宿舍水电费提醒", message_content)

def demo_low_balance_alert():
    """余额不足提醒示例"""
    # 模拟余额数据
    electricity_balance = 10.50  # 电费余额
    water_balance = 5.20        # 水费余额
    
    # 设置预警阈值
    THRESHOLD = 20.0  # 当余额低于20元时发出提醒
    
    if electricity_balance < THRESHOLD or water_balance < THRESHOLD:
        alert_message = f"""
# ⚠️ 水电费余额不足提醒

## 当前余额
- 电费余额：**¥{electricity_balance:.2f}**
- 水费余额：**¥{water_balance:.2f}**

**请及时充值，以免影响正常使用！**
"""
        send_wechat_message("水电费余额不足提醒", alert_message)

def main():
    """主函数，运行所有示例"""
    print("运行水电费推送示例...")
    demo_utility_bill_push()
    
    print("\n运行余额不足提醒示例...")
    demo_low_balance_alert()

if __name__ == "__main__":
    main() 