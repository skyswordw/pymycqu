"""邮件发送模块使用示例

本示例展示了如何使用 mycqu.utils.email_sender 模块发送邮件
"""
from mycqu.utils.email_sender import (
    EmailSender,
    initialize_email_sender,
    send_email
)

def demo_basic_usage():
    """基础使用示例"""
    # 使用QQ邮箱（推荐使用授权码而不是密码）
    EMAIL = "your_email@qq.com"  # 替换为你的邮箱
    PASSWORD = "your_password"    # 替换为你的密码或授权码
    
    # 方式1：使用便捷函数（推荐）
    initialize_email_sender(EMAIL, PASSWORD)
    
    # 发送简单文本邮件
    send_email(
        "student@example.com",
        "课程提醒",
        "你有一节《高等数学》课程将在30分钟后开始"
    )
    
    # 发送HTML格式的邮件
    html_content = """
    <h1>成绩通知</h1>
    <p>你的期末考试成绩已出：</p>
    <ul>
        <li>高等数学：<strong>95</strong></li>
        <li>大学物理：<strong>88</strong></li>
        <li>程序设计：<strong>92</strong></li>
    </ul>
    <blockquote>请查收你的成绩单！</blockquote>
    """
    send_email(
        "student@example.com",
        "成绩通知",
        html_content,
        html=True
    )

def demo_advanced_usage():
    """高级使用示例"""
    # 方式2：直接使用 EmailSender 类
    sender = EmailSender(
        "your_email@163.com",     # 使用163邮箱
        "your_password",          # 密码或授权码
        # 也可以手动指定SMTP服务器信息
        smtp_server="smtp.163.com",
        smtp_port=25
    )
    
    # 发送给多个收件人
    sender.send_email(
        ["student1@example.com", "student2@example.com"],
        "图书馆提醒",
        "你借阅的《Python编程》将在3天后到期，请及时续借或归还。"
    )
    
    # 使用抄送和密送
    sender.send_email(
        "student@example.com",
        "系统通知",
        "这是一条重要通知。",
        cc="teacher@example.com",
        bcc="admin@example.com"
    )

def demo_error_handling():
    """错误处理示例"""
    try:
        # 使用无效的邮箱信息
        sender = EmailSender("invalid@example.com", "wrong_password")
        sender.send_email("test@example.com", "测试", "测试内容")
    except ValueError as e:
        print(f"发送失败：{e}")
    
    try:
        # 未初始化就使用默认发送器
        send_email("test@example.com", "测试", "测试内容")
    except RuntimeError as e:
        print(f"发送失败：{e}")

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