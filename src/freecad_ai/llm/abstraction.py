"""
FreeCAD AI Assistant - LLM Abstraction Layer

این ماژول لایه انتزاع برای ارتباط با LLM Providers مختلف را فراهم می‌کند.
پشتیبانی‌شده: Claude, OpenAI, OpenRouter, DeepSeek
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """ساختار پیام برای ارتباط با LLM"""
    role: str
    content: str


@dataclass
class ToolDefinition:
    """تعریف یک Tool برای Function Calling"""
    name: str
    description: str
    parameters: Dict[str, Any]


class LLMProvider(ABC):
    """کلاس پایه انتزاعی برای LLM Providers"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = None
        self._initialize_client()
    
    @abstractmethod
    def _initialize_client(self) -> None:
        pass
    
    @abstractmethod
    def chat(self, messages: List[Message], tools: Optional[List[ToolDefinition]] = None, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def parse_response(self, response: Dict[str, Any]) -> str:
        pass
    
    def is_available(self) -> bool:
        return bool(self.api_key)


class ClaudeProvider(LLMProvider):
    """Provider برای Claude API (Anthropic)"""
    
    def _initialize_client(self) -> None:
        try:
            from anthropic import Anthropic
            # حذف آرگومان‌های قدیمی مثل proxies
            self.client = Anthropic(api_key=self.api_key)
            logger.info("Claude client initialized successfully")
        except ImportError:
            logger.error("anthropic package not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize Claude client: {e}")
            self.client = None
    
    def chat(self, messages: List[Message], tools: Optional[List[ToolDefinition]] = None, **kwargs) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError("Claude client not initialized")
        
        system_message = ""
        chat_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                chat_messages.append({"role": msg.role, "content": msg.content})
        
        request_kwargs = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "messages": chat_messages
        }
        
        if system_message:
            request_kwargs["system"] = system_message
        
        if tools:
            request_kwargs["tools"] = [
                {"name": tool.name, "description": tool.description, "input_schema": tool.parameters}
                for tool in tools
            ]
        
        try:
            response = self.client.messages.create(**request_kwargs)
            return {"content": response.content, "raw": response, "provider": "claude"}
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def parse_response(self, response: Dict[str, Any]) -> str:
        content = response.get("content", [])
        text_parts = []
        for block in content:
            if hasattr(block, 'text'):
                text_parts.append(block.text)
            elif isinstance(block, dict) and 'text' in block:
                text_parts.append(block['text'])
        return "\n".join(text_parts) if text_parts else ""


class OpenAIProvider(LLMProvider):
    """Provider برای OpenAI API"""
    
    def _initialize_client(self) -> None:
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized successfully")
        except ImportError:
            logger.error("openai package not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def chat(self, messages: List[Message], tools: Optional[List[ToolDefinition]] = None, **kwargs) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        openai_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        request_kwargs = {
            "model": self.model,
            "messages": openai_messages,
            "max_tokens": kwargs.get("max_tokens", 4096)
        }
        
        if tools:
            request_kwargs["tools"] = [
                {"type": "function", "function": {"name": tool.name, "description": tool.description, "parameters": tool.parameters}}
                for tool in tools
            ]
        
        try:
            response = self.client.chat.completions.create(**request_kwargs)
            return {"content": response.choices[0].message, "raw": response, "provider": "openai"}
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def parse_response(self, response: Dict[str, Any]) -> str:
        message = response.get("content")
        if hasattr(message, 'content'):
            return message.content or ""
        elif isinstance(message, dict):
            return message.get('content', '')
        return ""


class OpenRouterProvider(OpenAIProvider):
    """Provider برای OpenRouter"""
    
    def _initialize_client(self) -> None:
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            logger.info("OpenRouter client initialized successfully")
        except ImportError:
            logger.error("openai package not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter client: {e}")
            self.client = None


class DeepSeekProvider(OpenAIProvider):
    """Provider برای DeepSeek API"""
    
    def _initialize_client(self) -> None:
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com/v1"
            )
            logger.info("DeepSeek client initialized successfully")
        except ImportError:
            logger.error("openai package not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize DeepSeek client: {e}")
            self.client = None


class LLMOrchestrator:
    """مدیریت‌کننده اصلی LLMها"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers: Dict[str, LLMProvider] = {}
        self._initialize_providers()
    
    def _initialize_providers(self) -> None:
        if self.config.get("anthropic_api_key"):
            self.providers["claude"] = ClaudeProvider(
                api_key=self.config["anthropic_api_key"],
                model=self.config.get("default_model", "claude-3-sonnet-20240229")
            )
        
        if self.config.get("openai_api_key"):
            self.providers["openai"] = OpenAIProvider(
                api_key=self.config["openai_api_key"],
                model=self.config.get("openai_model", "gpt-4-turbo-preview")
            )
        
        if self.config.get("openrouter_api_key"):
            self.providers["openrouter"] = OpenRouterProvider(
                api_key=self.config["openrouter_api_key"],
                model=self.config.get("openrouter_model", "anthropic/claude-3-sonnet")
            )
        
        if self.config.get("deepseek_api_key"):
            self.providers["deepseek"] = DeepSeekProvider(
                api_key=self.config["deepseek_api_key"],
                model=self.config.get("deepseek_model", "deepseek-chat")
            )
        
        logger.info(f"Initialized {len(self.providers)} LLM providers")
    
    def get_provider(self, name: str) -> Optional[LLMProvider]:
        return self.providers.get(name)
    
    def get_default_provider(self) -> Optional[LLMProvider]:
        default_name = self.config.get("default_provider", "claude")
        return self.get_provider(default_name)
    
    def list_available_providers(self) -> List[str]:
        return [name for name, provider in self.providers.items() if provider.is_available()]
