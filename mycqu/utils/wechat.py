"""微信推送模块

此模块提供了微信消息推送的功能，使用 Server酱 服务实现。
使用前需要在 https://sct.ftqq.com/ 获取 PUSH_KEY
"""
from typing import Optional
import requests
from urllib.parse import urljoin

class WechatPusher:
    """微信推送器类"""
    
    BASE_URL = "https://sctapi.ftqq.com/"
    
    def __init__(self, push_key: str):
        """初始化微信推送器
        
        Args:
            push_key: Server酱的 PUSH_KEY，在 https://sct.ftqq.com/ 获取
        """
        self.push_key = push_key
    
    def send(self, title: str, content: Optional[str] = None, *, 
             channel: Optional[str] = None) -> bool:
        """发送微信消息
        
        Args:
            title: 消息标题，必填，最长为 32 个字符
            content: 消息内容，选填，支持 markdown 格式
            channel: 推送通道，可选值：微信服务号=9，企业微信群机器人=1，
                    企业微信应用消息=2，测试号=3，SMS=4，邮件=5，
                    钉钉群机器人=6，飞书群机器人=7，测试回调=8
        
        Returns:
            bool: 推送是否成功
            
        Raises:
            ValueError: 当推送失败时抛出，包含具体错误信息
        """
        url = urljoin(self.BASE_URL, self.push_key + ".send")
        
        data = {
            "title": title[:32],  # 标题限制32字符
            "desp": content,
        }
        if channel is not None:
            data["channel"] = channel
            
        try:
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get("code") == 0:
                return True
            else:
                raise ValueError(f"推送失败: {result.get('message', '未知错误')}")
        except Exception as e:
            raise ValueError(f"推送失败: {str(e)}")

class DefaultWechatPusher:
    """默认微信推送器，需要先设置 PUSH_KEY"""
    _instance: Optional[WechatPusher] = None
    
    @classmethod
    def initialize(cls, push_key: str) -> None:
        """初始化默认推送器
        
        Args:
            push_key: Server酱的 PUSH_KEY
        """
        cls._instance = WechatPusher(push_key)
    
    @classmethod
    def send(cls, title: str, content: Optional[str] = None, **kwargs) -> bool:
        """使用默认推送器发送消息
        
        Args:
            title: 消息标题
            content: 消息内容
            **kwargs: 其他参数，见 WechatPusher.send 的参数说明
            
        Returns:
            bool: 推送是否成功
            
        Raises:
            RuntimeError: 当默认推送器未初始化时抛出
        """
        if cls._instance is None:
            raise RuntimeError("默认推送器未初始化，请先调用 initialize 方法设置 PUSH_KEY")
        return cls._instance.send(title, content, **kwargs)

# 便捷函数
def initialize_wechat_push(push_key: str) -> None:
    """初始化默认微信推送器
    
    Args:
        push_key: Server酱的 PUSH_KEY
    """
    DefaultWechatPusher.initialize(push_key)

def send_wechat_message(title: str, content: Optional[str] = None, **kwargs) -> bool:
    """使用默认推送器发送微信消息
    
    Args:
        title: 消息标题
        content: 消息内容
        **kwargs: 其他参数，见 WechatPusher.send 的参数说明
        
    Returns:
        bool: 推送是否成功
    """
    return DefaultWechatPusher.send(title, content, **kwargs) 