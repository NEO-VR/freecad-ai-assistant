"""
FreeCAD AI Assistant - Configuration
مدیریت تنظیمات و کلیدهای API با استفاده از Pydantic
"""
import os
import logging
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

logger = logging.getLogger("FreeCAD_AI_Config")

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

class Config(BaseSettings):
    """
    کلاس پیکربندی اصلی
    
    Attributes:
        anthropic_api_key: کلید API Anthropic (Claude)
        openai_api_key: کلید API OpenAI
        default_provider: ارائه‌دهنده پیش‌فرض (claude, openai, ...)
        default_model: مدل پیش‌فرض
    """
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    deepseek_api_key: str = Field(default="", env="DEEPSEEK_API_KEY")
    
    default_provider: str = Field(default="claude", env="DEFAULT_PROVIDER")
    default_model: str = Field(default="claude-sonnet-4-6", env="DEFAULT_MODEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# نمونه_singleton برای دسترسی آسان
_config_instance = None

def get_config() -> Config:
    """
    دریافت نمونه پیکربندی (Singleton)
    
    Returns:
        Config: نمونه پیکربندی
    """
    global _config_instance
    if _config_instance is None:
        try:
            _config_instance = Config()
            logger.info("Configuration loaded successfully")
            
            # لاگ امن (بدون نمایش کلید کامل)
            if _config_instance.anthropic_api_key:
                logger.debug(f"Anthropic Key found: {_config_instance.anthropic_api_key[:5]}...")
            if _config_instance.openai_api_key:
                logger.debug(f"OpenAI Key found: {_config_instance.openai_api_key[:5]}...")
                
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}", exc_info=True)
            raise
    return _config_instance
