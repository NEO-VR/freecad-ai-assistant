"""
FreeCAD AI Assistant - Test Suite

تست‌های اولیه برای Workbench
"""

import unittest
import sys
import os

# اضافه کردن مسیر src به path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestConfig(unittest.TestCase):
    """تست‌های ماژول Config"""
    
    def test_config_creation(self):
        """تست ساخت نمونه Config"""
        from freecad_ai.core.config import Config
        
        config = Config()
        
        self.assertEqual(config.default_provider, "anthropic")
        self.assertEqual(config.language, "fa")
        self.assertFalse(config.debug_mode)
    
    def test_config_from_env(self):
        """تست بارگذاری Config از environment"""
        from freecad_ai.core.config import Config
        
        # تنظیم متغیرهای محیطی تست
        os.environ['FREECAD_AI_DEFAULT_PROVIDER'] = 'openai'
        os.environ['FREECAD_AI_LANGUAGE'] = 'en'
        
        config = Config.from_env()
        
        self.assertEqual(config.default_provider, "openai")
        self.assertEqual(config.language, "en")
        
        # پاک کردن متغیرها
        del os.environ['FREECAD_AI_DEFAULT_PROVIDER']
        del os.environ['FREECAD_AI_LANGUAGE']
    
    def test_get_config_singleton(self):
        """تست singleton بودن get_config"""
        from freecad_ai.core.config import get_config
        
        config1 = get_config()
        config2 = get_config()
        
        self.assertIs(config1, config2)


class TestContextManager(unittest.TestCase):
    """تست‌های ماژول Context Manager"""
    
    def test_context_manager_creation(self):
        """تست ساخت نمونه Context Manager"""
        from freecad_ai.context.manager import ContextManager
        
        manager = ContextManager()
        
        # در حالت mock باید context ساختگی برگرداند
        context = manager.get_context()
        
        self.assertIn("active_document", context)
        self.assertIn("selected_objects", context)
        self.assertIn("model_units", context)
    
    def test_context_format_for_llm(self):
        """تست فرمت‌دهی Context برای LLM"""
        from freecad_ai.context.manager import ContextManager
        
        manager = ContextManager()
        context = {
            "active_document": "TestDoc",
            "selected_objects": ["Cylinder_001"],
            "active_sketch": None,
            "model_units": "mm"
        }
        
        formatted = manager.format_for_llm(context)
        
        self.assertIn("TestDoc", formatted)
        self.assertIn("Cylinder_001", formatted)
        self.assertIn("mm", formatted)


class TestSafeExecutor(unittest.TestCase):
    """تست‌های ماژول Safe Executor"""
    
    def test_executor_creation(self):
        """تست ساخت نمونه Safe Executor"""
        from freecad_ai.executor.safe_executor import SafeExecutor
        
        executor = SafeExecutor()
        
        # در حالت mock باید همیشه True برگرداند
        result = executor.execute("pass")
        
        self.assertTrue(result)
    
    def test_code_validation(self):
        """تست اعتبارسنجی کد"""
        from freecad_ai.executor.safe_executor import SafeExecutor
        
        executor = SafeExecutor()
        
        # کد ایمن
        is_valid, msg = executor.validate_code("print('hello')")
        self.assertTrue(is_valid)
        
        # کد خطرناک
        is_valid, msg = executor.validate_code("import os")
        self.assertFalse(is_valid)
    
    def test_transaction_state(self):
        """تست وضعیت Transaction"""
        from freecad_ai.executor.safe_executor import SafeExecutor
        
        executor = SafeExecutor()
        
        self.assertFalse(executor.is_in_transaction())
        self.assertIsNone(executor.get_current_transaction())


class TestLLMAbstraction(unittest.TestCase):
    """تست‌های ماژول LLM Abstraction"""
    
    def test_message_creation(self):
        """تست ساخت نمونه Message"""
        from freecad_ai.llm.abstraction import Message
        
        msg = Message(role="user", content="Hello")
        
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "Hello")
    
    def test_tool_definition_creation(self):
        """تست ساخت نمونه ToolDefinition"""
        from freecad_ai.llm.abstraction import ToolDefinition
        
        tool = ToolDefinition(
            name="create_cylinder",
            description="Create a cylinder",
            parameters={"type": "object"}
        )
        
        self.assertEqual(tool.name, "create_cylinder")
        self.assertIsNotNone(tool.description)


class TestEventListeners(unittest.TestCase):
    """تست‌های ماژول Event Listeners"""
    
    def test_event_type_enum(self):
        """تست Enum EventType"""
        from freecad_ai.listeners.event_listeners import EventType
        
        self.assertEqual(EventType.DOCUMENT_CREATED.value, "DocumentCreated")
        self.assertEqual(EventType.SELECTION_CHANGED.value, "SelectionChanged")
    
    def test_event_creation(self):
        """تست ساخت نمونه Event"""
        from freecad_ai.listeners.event_listeners import Event, EventType
        
        event = Event(
            type=EventType.OBJECT_ADDED,
            data={"object": "TestObject"}
        )
        
        self.assertEqual(event.type, EventType.OBJECT_ADDED)
        self.assertEqual(event.data["object"], "TestObject")
    
    def test_listener_creation(self):
        """تست ساخت نمونه EventListener"""
        from freecad_ai.listeners.event_listeners import EventListener
        
        listener = EventListener()
        
        self.assertFalse(listener.is_enabled())


class TestWorkbenchIntegration(unittest.TestCase):
    """تست‌های یکپارچگی Workbench"""
    
    def test_package_import(self):
        """تست ایمپورت پکیج اصلی"""
        try:
            import freecad_ai
            self.assertTrue(hasattr(freecad_ai, '__version__'))
        except ImportError:
            self.fail("Failed to import freecad_ai package")
    
    def test_version_format(self):
        """تست فرمت نسخه"""
        import freecad_ai
        
        version = freecad_ai.__version__
        
        # نسخه باید فرمت x.y.z داشته باشد
        parts = version.split('.')
        self.assertEqual(len(parts), 3)
        
        for part in parts:
            self.assertTrue(part.isdigit())


if __name__ == '__main__':
    # اجرای تست‌ها
    unittest.main(verbosity=2)
