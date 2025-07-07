import os
from typing import Optional, List, Dict, Any, Union
try:
    from openai import OpenAI
except ImportError:
    # 处理导入错误，在后续代码中添加检查
    OpenAI = None

from backend.config import settings


class Generator:
    """文本生成器类"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        default_model: Optional[str] = None,
    ):
        # 使用提供的参数或配置中的默认值
        self.base_url = base_url or settings.openai_base_url
        self.api_key = api_key or settings.openai_api_key
        self.default_model = default_model or settings.default_model
        
        # 检查OpenAI是否已成功导入
        if OpenAI is None:
            print("警告: 未找到OpenAI模块，需要安装'openai'包")
            self.client = None
        else:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )

    def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        model: Optional[str] = None
    ) -> str:
        """使用OpenAI API生成响应"""
        if self.client is None:
            return "错误: OpenAI客户端未初始化"
            
        if model is None:
            model = self.default_model
             
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            # 记录错误并返回友好的错误消息
            print(f"生成文本时出错: {e}")
            return f"生成文本时出错: {str(e)}"

    def generate_with_default_messages(
        self, 
        user_content: str, 
        model: Optional[str] = None
    ) -> str:
        """使用默认消息生成文本响应"""
        if model is None:
            model = self.default_model
             
        messages = [
            {
                "role": "system",
                "content": "You are a human.",
            },
            {
                "role": "user",
                "content": user_content,
            },
        ]
        return self.generate_response(messages, model)
