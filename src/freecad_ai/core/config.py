"""
FreeCAD AI Assistant - Configuration
"""
import os
import logging
from dotenv import load_dotenv
# تغییر مهم برای Pydantic v2:
from pydantic_settings import BaseSettings  
from pydantic import Field

logger = logging.getLogger("FreeCAD_AI_Config")

load_dotenv()

class Config(BaseSettings):
    anthropic_api_key: str = Field(default="", validation_alias="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    openrouter_api_key: str = Field(default="", validation_alias="OPENROUTER_API_KEY")
    deepseek_api_key: str = Field(default="", validation_alias="DEEPSEEK_API_KEY")
    
    default_provider: str = Field(default="claude", validation_alias="DEFAULT_PROVIDER")
    default_model: str = Field(default="claude-sonnet-4-6", validation_alias="DEFAULT_MODEL")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

_config_instance = None

def get_config() -> Config:
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance