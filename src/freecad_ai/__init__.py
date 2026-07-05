"""
FreeCAD AI Assistant - Init Module

این فایل نقطه ورود اصلی پکیج freecad_ai است.
"""

__version__ = "0.1.0"
__author__ = "FreeCAD AI Team"
__description__ = "AI Assistant for FreeCAD - Natural Language to 3D Modeling"

from .core.config import Config, get_config, reload_config
from .llm.abstraction import (
    LLMProvider, 
    ClaudeProvider, 
    OpenAIProvider,
    OpenRouterProvider,
    DeepSeekProvider,
    LLMOrchestrator,
    Message,
    ToolDefinition
)
from .context.manager import ContextManager, get_context_manager
from .executor.safe_executor import SafeExecutor, get_executor, safe_execute
from .listeners.event_listeners import (
    EventListener,
    ContextAwareListener,
    EventType,
    Event,
    get_listener,
    get_context_listener
)

__all__ = [
    # Version
    '__version__',
    '__author__',
    '__description__',
    
    # Config
    'Config',
    'get_config',
    'reload_config',
    
    # LLM
    'LLMProvider',
    'ClaudeProvider',
    'OpenAIProvider',
    'OpenRouterProvider',
    'DeepSeekProvider',
    'LLMOrchestrator',
    'Message',
    'ToolDefinition',
    
    # Context
    'ContextManager',
    'get_context_manager',
    
    # Executor
    'SafeExecutor',
    'get_executor',
    'safe_execute',
    
    # Listeners
    'EventListener',
    'ContextAwareListener',
    'EventType',
    'Event',
    'get_listener',
    'get_context_listener'
]