"""تست اعتبار API Key"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ خطا: ANTHROPIC_API_KEY در فایل .env یافت نشد")
    exit(1)

print(f"✅ API Key یافت شد: {api_key[:10]}...{api_key[-4:]}")

# تست ساده با requests
try:
    import requests
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "Hi"}]
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data,
        timeout=10
    )
    
    if response.status_code == 200:
        print("✅ API Key معتبر است!")
        print(f"پاسخ: {response.json()}")
    elif response.status_code == 401:
        print("❌ API Key نامعتبر است (401 Unauthorized)")
    elif response.status_code == 403:
        print("❌ دسترسی ممنوع (403 Forbidden) - ممکن است API Key منقضی شده باشد")
    else:
        print(f"⚠️ کد وضعیت: {response.status_code}")
        print(f"پاسخ: {response.text}")
        
except ImportError:
    print("⚠️ کتابخانه requests نصب نیست. دستور زیر را اجرا کنید:")
    print("pip install requests")
except Exception as e:
    print(f"❌ خطا در تست API: {e}")
