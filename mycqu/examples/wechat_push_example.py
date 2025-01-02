"""微信推送模块使用示例

本示例展示了如何使用 mycqu.utils.wechat 模块进行微信消息推送
"""
from mycqu.utils.wechat import (
    WechatPusher,
    initialize_wechat_push,
    send_wechat_message
)

def demo_basic_usage():
    """基础使用示例"""
    # 首先需要在 https://sct.ftqq.com/ 获取你的 PUSH_KEY
    PUSH_KEY = "YOUR_PUSH_KEY"  # 替换为你的 PUSH_KEY
    
    # 方式1：使用便捷函数（推荐）
    initialize_wechat_push(PUSH_KEY)
    
    # 发送简单消息
    send_wechat_message("课程提醒", "你有一节《高等数学》课程将在30分钟后开始")
    
    # 发送带 Markdown 格式的消息
    markdown_content = """
    # 成绩通知
    
    你的期末考试成绩已出：
    
    - 高等数学：**95**
    - 大学物理：**88**
    - 程序设计：**92**
    
    > 请查收你的成绩单！
    """
    send_wechat_message("成绩通知", markdown_content)

def demo_advanced_usage():
    """高级使用示例"""
    PUSH_KEY = "YOUR_PUSH_KEY"
    
    # 方式2：直接使用 WechatPusher 类
    pusher = WechatPusher(PUSH_KEY)
    
    # 使用微信服务号推送（channel=9）
    pusher.send(
        title="图书馆提醒",
        content="你借阅的《Python编程》将在3天后到期，请及时续借或归还。",
        channel="9"
    )
    
    # 使用企业微信推送（channel=2）
    pusher.send(
        title="系统通知",
        content="服务器CPU使用率超过90%，请及时检查。",
        channel="2"
    )

def demo_error_handling():
    """错误处理示例"""
    try:
        # 使用无效的 PUSH_KEY
        pusher = WechatPusher("invalid_key")
        pusher.send("测试标题", "测试内容")
    except ValueError as e:
        print(f"推送失败：{e}")
    
    try:
        # 未初始化就使用默认推送器
        send_wechat_message("测试标题", "测试内容")
    except RuntimeError as e:
        print(f"推送失败：{e}")

def main():
    """主函数，运行所有示例"""
    print("运行基础使用示例...")
    demo_basic_usage()
    
    print("\n运行高级使用示例...")
    demo_advanced_usage()
    
    print("\n运行错误处理示例...")
    demo_error_handling()

if __name__ == "__main__":
    main() 