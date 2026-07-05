"""
FreeCAD AI Assistant - Core Configuration Module

این ماژول پیکربندی اصلی پروژه را مدیریت می‌کند.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class Config:
    """
    کلاس پیکربندی پروژه FreeCAD AI Assistant
    
    Attributes:
        anthropic_api_key: کلید API برای Claude
        openai_api_key: کلید API برای OpenAI
        openrouter_api_key: کلید API برای OpenRouter
        deepseek_api_key: کلید API برای DeepSeek
        default_provider: provider پیش‌فرض (anthropic)
        default_model: مدل پیش‌فرض
        language: زبان رابط کاربری (fa/en)
        debug_mode: حالت دیباگ
    """
    
    # API Keys
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    
    # Settings
    default_provider: str = "anthropic"
    default_model: str = "claude-3-sonnet-20240229"
    language: str = "fa"
    debug_mode: bool = False
    
    # Transaction settings
    max_transaction_time: int = 30  # seconds
    max_context_size: int = 10000  # characters
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        ساخت پیکربندی از متغیرهای محیطی
        
        Returns:
            Config: نمونه پیکربندی
        """
        # بارگذاری فایل .env
        load_dotenv()
        
        config = cls(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY"),
            default_provider=os.getenv("FREECAD_AI_DEFAULT_PROVIDER", "anthropic"),
            default_model=os.getenv("FREECAD_AI_DEFAULT_MODEL", "claude-3-sonnet-20240229"),
            language=os.getenv("FREECAD_AI_LANGUAGE", "fa"),
            debug_mode=os.getenv("FREECAD_AI_DEBUG", "false").lower() == "true"
        )
        
        return config
    
    def is_provider_available(self, provider: str) -> bool:
        """
        بررسی در دسترس بودن یک provider
        
        Args:
            provider: نام provider
            
        Returns:
            bool: True اگر API key موجود باشد
        """
        key_map = {
            "anthropic": self.anthropic_api_key,
            "openai": self.openai_api_key,
            "openrouter": self.openrouter_api_key,
            "deepseek": self.deepseek_api_key
        }
        
        return bool(key_map.get(provider))
    
    def get_available_providers(self) -> list[str]:
        """
        دریافت لیست providerهای در دسترس
        
        Returns:
            list[str]: لیست نام providerها
        """
        available = []
        for provider in ["anthropic", "openai", "openrouter", "deepseek"]:
            if self.is_provider_available(provider):
                available.append(provider)
        
        return available
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تبدیل پیکربندی به دیکشنری
        
        Returns:
            Dict[str, Any]: دیکشنری پیکربندی (بدون API keys)
        """
        return {
            "default_provider": self.default_provider,
            "default_model": self.default_model,
            "language": self.language,
            "debug_mode": self.debug_mode,
            "max_transaction_time": self.max_transaction_time,
            "max_context_size": self.max_context_size,
            "available_providers": self.get_available_providers()
        }


# نمونه جهانی پیکربندی
_global_config: Optional[Config] = None


def get_config() -> Config:
    """
    دریافت نمونه جهانی پیکربندی
    
    Returns:
        Config: نمونه پیکربندی
    """
    global _global_config
    
    if _global_config is None:
        _global_config = Config.from_env()
    
    return _global_config


def reload_config() -> Config:
    """
    بارگذاری مجدد پیکربندی از محیط
    
    Returns:
        Config: نمونه پیکربندی جدید
    """
    global _global_config
    _global_config = Config.from_env()
    return _global_config
