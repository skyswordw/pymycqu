"""验证码识别模块

此模块提供了验证码识别的功能，使用 ddddocr 库实现。
"""
from typing import Union
import ddddocr

class CaptchaRecognizer:
    """验证码识别器类"""
    
    def __init__(self):
        """初始化验证码识别器"""
        self._ocr = ddddocr.DdddOcr(show_ad=False)
    
    def recognize(self, image_data: Union[bytes, str]) -> str:
        """识别验证码
        
        Args:
            image_data: 图片数据，可以是字节流或图片文件路径
            
        Returns:
            str: 识别出的验证码文本
            
        Raises:
            ValueError: 当输入的图片数据无效时抛出
        """
        try:
            if isinstance(image_data, str):
                with open(image_data, 'rb') as f:
                    image_data = f.read()
            
            result = self._ocr.classification(image_data)
            return result
        except Exception as e:
            raise ValueError(f"验证码识别失败: {str(e)}")

# 创建一个默认的识别器实例供直接使用
default_recognizer = CaptchaRecognizer()

def recognize_captcha(image_data: Union[bytes, str]) -> str:
    """使用默认识别器识别验证码
    
    Args:
        image_data: 图片数据，可以是字节流或图片文件路径
        
    Returns:
        str: 识别出的验证码文本
    """
    return default_recognizer.recognize(image_data) 