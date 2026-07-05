# 🏗️ معماری سیستم: FreeCAD AI Assistant

## نمای کلی

```
┌─────────────────────────────────────────────────────────────┐
│                     FreeCAD Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              AI Assistant Workbench                   │   │
│  │                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │   │
│  │  │   Event     │  │   Context   │  │     LLM      │  │   │
│  │  │  Listeners  │→ │   Manager   │→ │ Orchestrator │  │   │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │   │
│  │         ↓                                    ↓        │   │
│  │  ┌─────────────┐                    ┌──────────────┐  │   │
│  │  │    FreeCAD  │                    │    Safe      │  │   │
│  │  │    Events   │                    │  Execution   │  │   │
│  │  └─────────────┘                    │   Engine     │  │   │
│  │                                     └──────────────┘  │   │
│  │                                            ↓           │   │
│  │  ┌──────────────────────────────────────────────┐     │   │
│  │  │            UI Panel (PySide6)                │     │   │
│  │  │  - Chat Box                                  │     │   │
│  │  │  - API Key Input                             │     │   │
│  │  │  - Quick Actions                             │     │   │
│  │  └──────────────────────────────────────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  LLM Providers  │
                    ├─────────────────┤
                    │ • Claude API    │
                    │ • OpenAI API    │
                    │ • OpenRouter    │
                    │ • DeepSeek API  │
                    └─────────────────┘
```

## ماژول‌های اصلی

### ۱. Event Listeners (چشم و گوش)

**مسیر**: `src/freecad_ai/listeners/event_listeners.py`

**وظایف**:
- شنود رویدادهای FreeCAD با استفاده از Observer Pattern
- تشخیص ایجاد آبجکت جدید
- نظارت بر تغییرات Sketch
- ردیابی انتخاب Face/Edge/Vertex

**APIهای FreeCAD**:
```python
import FreeCAD as App

# Subscribe to events
App.addEvent("DocumentCreated", callback)
App.addEvent("ObjectAdded", callback)
App.addEvent("SelectionChanged", callback)
```

---

### ۲. Context Manager (حافظه کوتاه‌مدت)

**مسیر**: `src/freecad_ai/context/manager.py`

**وظایف**:
- جمع‌آوری وضعیت فعلی FreeCAD
- تبدیل به JSON فشرده برای LLM
- مدیریت تاریخچه Context

**خروجی نمونه**:
```json
{
  "active_document": "Gear_Project",
  "selected_objects": ["Cylinder_001"],
  "active_sketch": null,
  "model_units": "mm",
  "document_objects": [
    {"name": "Cylinder_001", "type": "Part::Cylinder"},
    {"name": "Sketch_002", "type": "Sketcher::SketchObject"}
  ]
}
```

---

### ۳. LLM Orchestrator (مغز متفکر)

**مسیر**: `src/freecad_ai/llm/abstraction.py`

**وظایف**:
- مدیریت ارتباط با LLM Providers
- ساخت پرامپت‌ها
- مدیریت Function Calling
- پردازش پاسخ‌ها

**Abstraction Layer**:
```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def chat(self, messages: list, tools: list) -> dict:
        pass
    
    @abstractmethod
    def parse_response(self, response: dict) -> str:
        pass

class ClaudeProvider(LLMProvider):
    # Implementation for Claude API
    pass

class OpenAIProvider(LLMProvider):
    # Implementation for OpenAI API
    pass
```

**Providers پشتیبانی‌شده**:
1. **Claude API** (پیش‌فرض)
2. **OpenAI API** (GPT-4, GPT-3.5)
3. **OpenRouter** (Multi-model)
4. **DeepSeek API** (ارزان)

---

### ۴. Safe Execution Engine (دست‌های ایمن)

**مسیر**: `src/freecad_ai/executor/safe_executor.py`

**وظایف**:
- اجرای ایمن کد تولیدشده توسط LLM
- مدیریت Transactions
- بازگشت خودکار در صورت خطا

**مکانیزم**:
```python
import FreeCAD as App

def safe_execute(code: str) -> bool:
    """
    اجرای ایمن کد با Transaction
    """
    doc = App.ActiveDocument
    if not doc:
        return False
    
    try:
        # باز کردن Transaction
        doc.openTransaction("AI Assistant Operation")
        
        # اجرای کد
        exec(code)
        
        # Commit موفق
        doc.commitTransaction()
        return True
        
    except Exception as e:
        # Abort در صورت خطا
        doc.abortTransaction()
        logging.error(f"Execution failed: {e}")
        return False
```

---

### ۵. UI Panel (رابط کاربری)

**مسیر**: `src/freecad_ai/ui/panel.py`

**وظایف**:
- نمایش چت‌باکس
- ورودی API Key
- دکمه‌های Quick Action
- یکپارچه‌سازی با FreeCAD GUI

**تکنولوژی**: PySide6 (Qt6)

**ساختار**:
```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QDockWidget
)

class AIPanelWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        # Chat area
        # Input field
        # Send button
        # API key input
        pass
```

---

## جریان داده (Data Flow)

### سناریوی نمونه: کاربر می‌گوید "یک استوانه بساز"

```
1. User Input (UI Panel)
   ↓ "Create a cylinder with radius 10mm and height 50mm"
   
2. Context Manager
   ↓ Collects current FreeCAD state
   ↓ {"active_document": "Part", "units": "mm", ...}
   
3. LLM Orchestrator
   ↓ Sends: [context] + [user_message]
   ↓ Receives: Tool call: create_cylinder(radius=10, height=50)
   
4. Safe Execution Engine
   ↓ Opens Transaction
   ↓ Executes: Part.makeCylinder(10, 50)
   ↓ Commits Transaction
   
5. UI Panel
   ↓ Shows: "✓ Cylinder created successfully!"
```

---

## امنیت

### لایه‌های امنیتی

1. **Transaction-based Execution**
   - تمام عملیات‌ها قابل بازگشت هستند
   
2. **Tool Use Only**
   - LLM نمی‌تواند کد آزاد اجرا کند
   - فقط از Tools تعریف‌شده استفاده می‌کند
   
3. **API Key Management**
   - کاربران API key خود را وارد می‌کنند
   - هیچ keyای در کد ذخیره نمی‌شود
   
4. **Input Validation**
   - تمام ورودی‌ها اعتبارسنجی می‌شوند
   - محدودیت اندازه ورودی/خروجی

---

## مقیاس‌پذیری

### توسعه آینده

#### Agentهای تخصصی
```
freecad_ai/
├── agents/
│   ├── sketch_agent.py       # متخصص Sketch
│   ├── part_agent.py         # متخصص Part Design
│   ├── assembly_agent.py     # متخصص Assembly
│   └── fem_agent.py          # متخصص FEM
```

#### پشتیبانی از زبان‌ها
```
freecad_ai/
├── i18n/
│   ├── fa_IR.json           # فارسی
│   ├── en_US.json           # English
│   └── de_DE.json           # Deutsch
```

---

## وابستگی‌ها

### Core Dependencies
- `anthropic` - Claude API
- `openai` - OpenAI API
- `PySide6` - UI Framework
- `python-dotenv` - Environment management

### Optional Dependencies
- `pytest` - Testing
- `black` - Code formatting
- `mypy` - Type checking

---

## تست

### استراتژی تست

1. **Unit Tests**: تست هر ماژول به صورت مستقل
2. **Integration Tests**: تست تعامل ماژول‌ها
3. **E2E Tests**: تست سناریوهای کامل کاربری

### اجرای تست‌ها
```bash
pytest tests/ -v
```

---

*آخرین به‌روزرسانی: 2025-07-05*
