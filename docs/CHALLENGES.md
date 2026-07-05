# 🚧 چالش‌ها و راه‌حل‌ها: FreeCAD AI Assistant

## چالش‌های فنی

### ۱. ناپایداری نام‌های توپولوژیک (Topological Naming)

**چالش**: 
در نسخه‌های قدیمی FreeCAD، نام Face/Edge/Vertex بعد از عملیات Boolean تغییر می‌کرد.

**وضعیت**: ✅ حل‌شده در FreeCAD 1.x

**راه‌حل**:
- FreeCAD 1.0+ این مشکل را حل کرده است
- می‌توانیم با اطمینان از نام‌ها استفاده کنیم
- همچنان بهتر است از IDهای پایدار استفاده شود

**کد نمونه**:
```python
# در FreeCAD 1.x ایمن است
face = obj.Shape.Faces[0]
# اما همچنان بهتر است از Label استفاده کنیم
obj.Label = "BaseCylinder"
```

---

### ۲. مدیریت Transactionها

**چالش**:
باز کردن Transactionهای تو در تو ممکن است باعث خطا شود.

**راه‌حل**:
```python
class SafeExecutor:
    def __init__(self):
        self.transaction_depth = 0
    
    def execute(self, code: str) -> bool:
        doc = App.ActiveDocument
        if not doc:
            return False
        
        try:
            # فقط اگر Transaction باز نیست، باز کن
            if self.transaction_depth == 0:
                doc.openTransaction("AI Assistant")
            self.transaction_depth += 1
            
            exec(code)
            
            self.transaction_depth -= 1
            if self.transaction_depth == 0:
                doc.commitTransaction()
                
            return True
            
        except Exception as e:
            self.transaction_depth -= 1
            if self.transaction_depth == 0:
                doc.abortTransaction()
            raise e
```

---

### ۳. همگام‌سازی UI با FreeCAD

**چالش**:
UI باید با تغییرات FreeCAD به‌روز شود.

**راه‌حل**:
- استفاده از Signal/Slot PySide6
- اتصال به Eventهای FreeCAD
- به‌روزرسانی خودکار Context

```python
from PySide6.QtCore import Signal, QObject

class ContextListener(QObject):
    context_changed = Signal(dict)
    
    def on_selection_changed(self):
        context = self.get_context()
        self.context_changed.emit(context)
```

---

### ۴. مدیریت خطاهای LLM

**چالش**:
LLM ممکن است کد نادرست یا مخرب تولید کند.

**راه‌حل‌ها**:

#### الف) Tool Use به جای Code Generation
```python
# ❌ بد: اجرای کد آزاد
code = llm.generate_code("make cylinder")
exec(code)

# ✅ خوب: استفاده از Tools تعریف‌شده
tools = [
    {
        "name": "create_cylinder",
        "parameters": {
            "radius": {"type": "number"},
            "height": {"type": "number"}
        }
    }
]
response = llm.chat(messages, tools=tools)
```

#### ب) اعتبارسنجی پارامترها
```python
def validate_cylinder_params(radius: float, height: float) -> bool:
    MAX_SIZE = 10000  # mm
    MIN_SIZE = 0.1
    
    if not (MIN_SIZE <= radius <= MAX_SIZE):
        return False
    if not (MIN_SIZE <= height <= MAX_SIZE):
        return False
    
    return True
```

#### ج) محدودیت Transaction
```python
MAX_TRANSACTION_TIME = 30  # seconds

def safe_execute_with_timeout(code: str) -> bool:
    try:
        result = subprocess.run(
            ["python", "-c", code],
            timeout=MAX_TRANSACTION_TIME
        )
        return result.returncode == 0
    except TimeoutExpired:
        return False
```

---

### ۵. مدیریت API Keys

**چالش**:
ذخیره امن API keys کاربران.

**راه‌حل**:
- هرگز API key را در کد ذخیره نکن
- از environment variables استفاده کن
- از `.env` فایل با gitignore استفاده کن

```python
# .env.example (در git هست)
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# .env (در git نیست)
ANTHROPIC_API_KEY=sk-ant-actual-key
OPENAI_API_KEY=sk-actual-key

# در کد
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
```

---

### ۶. پشتیبانی از چند زبان

**چالش**:
پشتیبانی همزمان از فارسی و انگلیسی.

**راه‌حل**:
- استفاده از i18n framework
- تشخیص خودکار زبان کاربر
- پرامپت‌های دو زبانه

```python
class MultiLanguageSupport:
    def __init__(self):
        self.translations = {
            'en': {
                'welcome': 'Welcome to FreeCAD AI Assistant',
                'error': 'An error occurred'
            },
            'fa': {
                'welcome': 'به دستیار هوشمند FreeCAD خوش آمدید',
                'error': 'خطایی رخ داد'
            }
        }
    
    def detect_language(self, text: str) -> str:
        # Simple heuristic
        if any('\u0600' <= c <= '\u06FF' for c in text):
            return 'fa'
        return 'en'
```

---

### ۷. Performance و Latency

**چالش**:
API calls ممکن است کند باشند.

**راه‌حل‌ها**:

#### الف) Async Processing
```python
import asyncio

async def chat_with_llm(messages: list) -> str:
    response = await client.messages.create(
        model="claude-3-sonnet-20240229",
        messages=messages
    )
    return response.content
```

#### ب) Caching Context
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_context(doc_hash: str) -> dict:
    return build_context()
```

#### ج) Streaming Responses
```python
def stream_response(messages: list):
    stream = client.messages.create(
        model="claude-3-sonnet-20240229",
        messages=messages,
        stream=True
    )
    
    for chunk in stream:
        yield chunk.text
```

---

### ۸. تست در محیط FreeCAD

**چالش**:
FreeCAD یک GUI application است و تست آن سخت است.

**راه‌حل‌ها**:

#### الف) Headless Mode
```bash
FreeCAD -c "import sys; sys.exit()"
```

#### ب) Mock FreeCAD API
```python
class MockFreeCAD:
    class ActiveDocument:
        def openTransaction(self, name): pass
        def commitTransaction(self): pass
        def abortTransaction(self): pass
```

#### ج) Integration Tests
```python
def test_create_cylinder():
    doc = FreeCAD.newDocument()
    result = create_cylinder(10, 50)
    assert result is not None
    assert len(doc.Objects) > 0
```

---

## چالش‌های تجاری

### ۹. مدل درآمدزایی

**چالش**:
تعادل بین ویژگی‌های رایگان و پولی.

**راه‌حل**:
- هسته اصلی رایگان (MIT License)
- Agentهای تخصصی پولی
- پشتیبانی تجاری پولی

---

### ۱۰. رقابت با ابزارهای موجود

**چالش**:
ابزارهای مشابه وجود دارند.

**راه‌حل**:
- تمرکز بر FreeCAD (niche market)
- پشتیبانی از فارسی
- قیمت‌گذاری مناسب
- جامعه کاربری قوی

---

## درس‌های آموخته‌شده

### ✅ انجام‌شده
1. تصمیم API-Only پیچیدگی را کاهش داد
2. PySide6 انتخاب درستی برای FreeCAD 1.x بود
3. Transactionها ایمنی خوبی فراهم می‌کنند

### ⚠️ در حال بررسی
1. نیاز به benchmark performance داریم
2. باید UX را با کاربران واقعی تست کنیم
3. مستندات باید کامل‌تر شود

---

*آخرین به‌روزرسانی: 2025-07-05*
