"""
FreeCAD AI Assistant - Phase 2 Test Script
تست لایه LLM و اتصال به API
"""
import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("🚀 شروع تست Phase 2")
print("=" * 60)

# تست ۱: بررسی پیکربندی
print("\n🔍 تست پیکربندی...")
try:
    from freecad_ai.core.config import get_config
    config = get_config()
    
    api_key = config.anthropic_api_key
    if api_key and len(api_key) > 10:
        print(f"✅ API Key: Found (starts with {api_key[:10]}...)")
    else:
        print("❌ API Key: Not found or invalid")
        sys.exit(1)
    
    print(f"✅ Provider: {config.default_provider}")
except Exception as e:
    print(f"❌ Config error: {e}")
    sys.exit(1)

# تست ۲: تست مستقیم Claude API
print("\n🤖 تست مستقیم Claude API...")
try:
    from freecad_ai.llm.abstraction import ClaudeProvider, Message
    
    # استفاده از مدل معتبر
    claude = ClaudeProvider(
        api_key=config.anthropic_api_key, 
        model="claude-sonnet-4-6"
    )
    
    if claude.client:
        print("✅ Claude Provider ساخته شد")
        
        # ارسال پیام تست
        response = claude.chat(
            messages=[Message(role="user", content="Hello!")]
        )
        
        text = claude.parse_response(response)
        if text:
            print(f"✅ پاسخ: {text[:50]}...")
        else:
            print("⚠️ پاسخ خالی بود")
    else:
        print("❌ Claude client مقداردهی نشد")
        
except Exception as e:
    print(f"❌ خطا در اتصال به Claude: {e}")

# تست ۳: تست LLM Orchestrator
print("\n🧠 تست LLM Orchestrator...")
try:
    from freecad_ai.llm.abstraction import LLMOrchestrator
    
    # تبدیل Config به دیکشنری
    config_dict = {
        "anthropic_api_key": config.anthropic_api_key,
        "openai_api_key": getattr(config, 'openai_api_key', None),
        "openrouter_api_key": getattr(config, 'openrouter_api_key', None),
        "deepseek_api_key": getattr(config, 'deepseek_api_key', None),
        "default_provider": "claude",
        "default_model": "claude-sonnet-4-6"
    }
    
    orchestrator = LLMOrchestrator(config=config_dict)
    
    available = orchestrator.list_available_providers()
    print(f"✅ Providerهای در دسترس: {available}")
    
    default = orchestrator.get_default_provider()
    if default:
        print(f"✅ Provider پیش‌فرض: {default.__class__.__name__}")
        
        # تست چت با orchestrator
        response = default.chat(
            messages=[Message(role="user", content="This is a test from Orchestrator")]
        )
        text = default.parse_response(response)
        print(f"✅ پاسخ Orchestrator: {text[:50]}...")
    
except Exception as e:
    print(f"❌ خطا در Orchestrator: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ پایان تست‌ها")
print("=" * 60)
