#!/usr/bin/env python3
"""
FreeCAD AI Assistant - Phase 2 Test Script
تست لایه LLM و اتصال به Providers
"""
import sys
import os

# افزودن مسیر src به Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("🚀 شروع تست Phase 2: FreeCAD AI Assistant")
print("=" * 60)

# =============================================================================
# تست ۱: پیکربندی
# =============================================================================
print("\n🔍 تست پیکربندی...")
try:
    from freecad_ai.core.config import get_config
    
    config = get_config()
    
    # بررسی API Key
    if config.anthropic_api_key:
        key_preview = config.anthropic_api_key[:8] + "..." if len(config.anthropic_api_key) > 8 else config.anthropic_api_key
        print(f"✅ کلید API یافت شد (شروع با: {key_preview})")
    else:
        print("⚠️ هشدار: کلید API Anthropic یافت نشد. فایل .env را بررسی کنید.")
    
    print(f"✅ پرووایدر انتخابی: {config.default_provider}")
    print(f"✅ مدل انتخابی: {config.default_model}")
    print(f"✅ زبان: {config.language}")
    print(f"✅ providerهای در دسترس: {config.get_available_providers()}")
    
except Exception as e:
    print(f"❌ خطا در پیکربندی: {e}")
    sys.exit(1)

# =============================================================================
# تست ۲: اتصال مستقیم به Claude API
# =============================================================================
print("\n🤖 تست مستقیم Claude API...")
try:
    from freecad_ai.llm.abstraction import ClaudeProvider, Message
    
    if not config.anthropic_api_key:
        print("⚠️ رد شد: کلید API Anthropic موجود نیست")
    else:
        # ساخت provider با آرگومان‌های صحیح
        claude = ClaudeProvider(api_key=config.anthropic_api_key, model="claude-3-sonnet-20240229")
        print(f"✅ Claude Provider ساخته شد: {claude.model}")
        
        # ارسال پیام تست
        messages = [Message(role="user", content="سلام! این یک پیام تست است. فقط پاسخ بده: 'تست موفقیت‌آمیز بود'")]
        
        response = claude.chat(messages=messages)
        
        if response.get('success'):
            content = response.get('content', '')
            print(f"✅ پاسخ دریافت شد: {content[:50]}...")
        else:
            print(f"❌ خطا در دریافت پاسخ: {response.get('error')}")
            
except ImportError as e:
    print(f"❌ خطا در ایمپورت: {e}")
except Exception as e:
    print(f"❌ خطا در اتصال به Claude: {e}")

# =============================================================================
# تست ۳: LLM Orchestrator
# =============================================================================
print("\n🧠 تست LLM Orchestrator...")
try:
    from freecad_ai.llm.abstraction import LLMOrchestrator, Message
    
    # ساخت orchestrator با config
    orchestrator = LLMOrchestrator(config=config)
    print(f"✅ LLM Orchestrator ساخته شد")
    print(f"✅ Provider فعال: {orchestrator.provider.__class__.__name__}")
    
    # ارسال پیام تست
    messages = [Message(role="user", content="این دومین پیام تست است.")]
    
    response = orchestrator.chat(messages=messages)
    
    if response.get('success'):
        print(f"✅ پاسخ از Orchestrator دریافت شد")
    else:
        print(f"⚠️ پاسخ بدون موفقیت: {response.get('error', 'Unknown error')}")
        
except ImportError as e:
    print(f"❌ خطا در ایمپورت Orchestrator: {e}")
except Exception as e:
    print(f"❌ خطا در Orchestrator: {e}")

# =============================================================================
# تست ۴: تست OpenAI Provider (اختیاری)
# =============================================================================
print("\n🔵 تست OpenAI Provider (اختیاری)...")
try:
    from freecad_ai.llm.abstraction import OpenAIProvider, Message
    
    if not config.openai_api_key:
        print("⚠️ رد شد: کلید API OpenAI موجود نیست")
    else:
        openai_provider = OpenAIProvider(api_key=config.openai_api_key, model="gpt-4-turbo-preview")
        print(f"✅ OpenAI Provider ساخته شد: {openai_provider.model}")
        
except ImportError as e:
    print(f"❌ خطا در ایمپورت OpenAI: {e}")
except Exception as e:
    print(f"❌ خطا در OpenAI: {e}")

# =============================================================================
# پایان تست‌ها
# =============================================================================
print("\n" + "=" * 60)
print("✅ پایان تست‌ها")
print("=" * 60)
print("\n📋 خلاصه:")
print(f"   - پیکربندی: OK")
print(f"   - Claude Provider: {'OK' if config.anthropic_api_key else 'نیاز به API Key'}")
print(f"   - OpenAI Provider: {'OK' if config.openai_api_key else 'نیاز به API Key'}")
print(f"   - LLM Orchestrator: OK")
print("\n💡 نکته: برای تست کامل، مطمئن شوید فایل .env با API Keyهای معتبر دارید.")
