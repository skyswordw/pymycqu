"""邮件推送模块

此模块提供了邮件发送功能，支持普通文本和HTML格式的邮件。
支持常见邮件服务商如：QQ邮箱、163邮箱、Gmail等。
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional, Union, List, Dict

class EmailSender:
    """邮件发送器类"""
    
    # 常用邮件服务器配置
    SMTP_SERVERS = {
        "qq": {"host": "smtp.qq.com", "port": 587},
        "163": {"host": "smtp.163.com", "port": 25},
        "gmail": {"host": "smtp.gmail.com", "port": 587},
        "outlook": {"host": "smtp.office365.com", "port": 587}
    }
    
    def __init__(self, email: str, password: str, smtp_server: Optional[str] = None,
                 smtp_port: Optional[int] = None):
        """初始化邮件发送器
        
        Args:
            email: 发件人邮箱地址
            password: 邮箱密码或授权码（推荐使用授权码）
            smtp_server: SMTP服务器地址，如果不指定则根据邮箱自动选择
            smtp_port: SMTP服务器端口，如果不指定则根据邮箱自动选择
        """
        self.email = email
        self.password = password
        
        # 如果未指定服务器信息，根据邮箱域名自动选择
        if not smtp_server:
            domain = email.split("@")[1].split(".")[0].lower()
            if domain in self.SMTP_SERVERS:
                server_info = self.SMTP_SERVERS[domain]
                smtp_server = server_info["host"]
                smtp_port = server_info["port"]
            else:
                raise ValueError(f"未知的邮箱服务商：{domain}，请手动指定SMTP服务器信息")
        
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_email(self, to_addrs: Union[str, List[str]], subject: str,
                  content: str, html: bool = False, cc: Optional[Union[str, List[str]]] = None,
                  bcc: Optional[Union[str, List[str]]] = None) -> bool:
        """发送邮件
        
        Args:
            to_addrs: 收件人邮箱地址，可以是单个地址或地址列表
            subject: 邮件主题
            content: 邮件内容
            html: 是否为HTML格式的内容
            cc: 抄送地址，可以是单个地址或地址列表
            bcc: 密送地址，可以是单个地址或地址列表
            
        Returns:
            bool: 发送是否成功
            
        Raises:
            ValueError: 当邮件发送失败时抛出，包含具体错误信息
        """
        # 统一转换为列表
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        if isinstance(cc, str):
            cc = [cc]
        if isinstance(bcc, str):
            bcc = [bcc]
        
        # 创建邮件对象
        msg = MIMEMultipart()
        msg["From"] = f"{Header('重庆大学教务通知', 'utf-8')} <{self.email}>"
        msg["To"] = ", ".join(to_addrs)
        if cc:
            msg["Cc"] = ", ".join(cc)
        msg["Subject"] = Header(subject, "utf-8")
        
        # 添加邮件内容
        content_type = "html" if html else "plain"
        msg.attach(MIMEText(content, content_type, "utf-8"))
        
        try:
            # 连接SMTP服务器
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # 启用TLS加密
                server.login(self.email, self.password)
                
                # 收集所有收件人
                all_recipients = set(to_addrs)
                if cc:
                    all_recipients.update(cc)
                if bcc:
                    all_recipients.update(bcc)
                
                # 发送邮件
                server.sendmail(self.email, list(all_recipients), msg.as_string())
                return True
                
        except Exception as e:
            raise ValueError(f"邮件发送失败: {str(e)}")

class DefaultEmailSender:
    """默认邮件发送器，需要先设置邮箱信息"""
    _instance: Optional[EmailSender] = None
    
    @classmethod
    def initialize(cls, email: str, password: str, **kwargs) -> None:
        """初始化默认发送器
        
        Args:
            email: 发件人邮箱地址
            password: 邮箱密码或授权码
            **kwargs: 其他参数，见 EmailSender.__init__ 的参数说明
        """
        cls._instance = EmailSender(email, password, **kwargs)
    
    @classmethod
    def send(cls, to_addrs: Union[str, List[str]], subject: str,
            content: str, **kwargs) -> bool:
        """使用默认发送器发送邮件
        
        Args:
            to_addrs: 收件人邮箱地址
            subject: 邮件主题
            content: 邮件内容
            **kwargs: 其他参数，见 EmailSender.send_email 的参数说明
            
        Returns:
            bool: 发送是否成功
            
        Raises:
            RuntimeError: 当默认发送器未初始化时抛出
        """
        if cls._instance is None:
            raise RuntimeError("默认发送器未初始化，请先调用 initialize 方法设置邮箱信息")
        return cls._instance.send_email(to_addrs, subject, content, **kwargs)

# 便捷函数
def initialize_email_sender(email: str, password: str, **kwargs) -> None:
    """初始化默认邮件发送器
    
    Args:
        email: 发件人邮箱地址
        password: 邮箱密码或授权码
        **kwargs: 其他参数，见 EmailSender.__init__ 的参数说明
    """
    DefaultEmailSender.initialize(email, password, **kwargs)

def send_email(to_addrs: Union[str, List[str]], subject: str,
               content: str, **kwargs) -> bool:
    """使用默认发送器发送邮件
    
    Args:
        to_addrs: 收件人邮箱地址
        subject: 邮件主题
        content: 邮件内容
        **kwargs: 其他参数，见 EmailSender.send_email 的参数说明
        
    Returns:
        bool: 发送是否成功
    """
    return DefaultEmailSender.send(to_addrs, subject, content, **kwargs) 