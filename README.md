# FreeCAD AI Assistant 🤖

## معرفی پروژه

FreeCAD AI Assistant یک افزونه هوشمند (Workbench) برای FreeCAD است که به عنوان "مغز دوم" کاربر عمل می‌کند. این پروژه با استفاده از مدل‌های زبانی بزرگ (LLM)، امکان کنترل FreeCAD با زبان طبیعی، نظارت بر طراحی و تشخیص خطاها، و آموزش کاربر را فراهم می‌کند.

## ویژگی‌های کلیدی

- 🗣️ **کنترل با زبان طبیعی**: صحبت کنید، FreeCAD اجرا کند (فارسی/انگلیسی)
- 👁️ **نظارت هوشمند**: تشخیص و اصلاح خودکار خطاها در طراحی
- 🎓 **مدرس شخصی**: آموزش گام‌به‌گام FreeCAD
- 🧠 **آگاهی از Context**: درک کامل وضعیت لحظه‌ای مدل
- 🔌 **Agentهای تخصصی**: زیرساخت برای توسعه Agentهای آینده

## معماری سیستم

پروژه از ۵ ماژول اصلی تشکیل شده است:

1. **Event Listeners**: شنود رویدادهای FreeCAD
2. **Context Manager**: مدیریت وضعیت فعلی مدل
3. **LLM Orchestrator**: مغز متفکر سیستم
4. **Safe Execution Engine**: اجرای ایمن کد با Transactions
5. **UI Panel**: رابط کاربری PySide6

## استراتژی تجاری

- **مدل درآمدزایی**: Open Core (هسته رایگان + ویژگی‌های پولی)
- **رویکرد فنی**: API-Only (بدون LLM لوکال)
- **API Providers**: Claude (پیش‌فرض), OpenAI, OpenRouter, DeepSeek

## پیش‌نیازها

- FreeCAD 1.1.1 (بر پایه FreeCAD 1.0)
- Python 3.10+
- PySide6 (Qt6)

## نصب

```bash
# Clone repository
git clone https://github.com/yourusername/freecad-ai-assistant.git
cd freecad-ai-assistant

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and add your API keys
cp .env.example .env
```

## نحوه استفاده

1. FreeCAD را باز کنید
2. Workbench "AI Assistant" را انتخاب کنید
3. API key خود را در پنل تنظیمات وارد کنید
4. شروع به صحبت با دستیار کنید!

## ساختار پروژه

```
freecad-ai-assistant/
├── docs/                          # مستندات پروژه
├── src/                           # کد اصلی
│   ├── freecad_ai/                # پکیج اصلی
│   │   ├── core/                  # هسته سیستم
│   │   ├── llm/                   # LLM Abstraction Layer
│   │   ├── context/               # Context Manager
│   │   ├── executor/              # Safe Execution Engine
│   │   ├── ui/                    # PySide6 UI
│   │   └── listeners/             # Event Listeners
│   ├── Init.py                    # FreeCAD Init
│   └── InitGui.py                 # FreeCAD GUI Init
├── tests/                         # تست‌ها
├── resources/                     # آیکون‌ها، ترجمه‌ها
├── requirements.txt               # وابستگی‌های Python
├── .env.example                   # نمونه فایل محیطی
├── README.md                      # این فایل
└── LICENSE                        # MIT License
```

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## مشارکت

از مشارکت شما استقبال می‌کنیم! لطفاً قبل از ارسال PR، مستندات پروژه را مطالعه کنید.

## تماس

برای سؤالات و پیشنهادات از طریق Issues GitHub با ما در ارتباط باشید.
