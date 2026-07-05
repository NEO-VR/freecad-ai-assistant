# 📊 وضعیت پروژه: FreeCAD AI Assistant

## اطلاعات کلی
- **نام پروژه**: FreeCAD AI Assistant
- **نسخه فعلی**: 0.1.0 (Phase 1 - Setup)
- **وضعیت**: در حال توسعه
- **تاریخ شروع**: 2026-07-05

## 🎯 اهداف پروژه

### هدف اصلی
ساخت یک افزونه هوشمند (Workbench) برای FreeCAD که به عنوان "مغز دوم" کاربر عمل کند.

### اهداف جزئی
1. کنترل FreeCAD با زبان طبیعی (فارسی/انگلیسی)
2. نظارت بر طراحی کاربر و تشخیص/اصلاح خودکار خطاها
3. نقش مدرس و آموزش‌دهنده FreeCAD
4. آگاهی کامل از Context (وضعیت لحظه‌ای مدل)
5. زیرساخت برای Agentهای تخصصی آینده

## 🏗️ معماری سیستم

### ماژول‌های اصلی
1. **Event Listeners** (چشم و گوش)
   - شنود رویدادهای FreeCAD
   - استفاده از Observer Pattern

2. **Context Manager** (حافظه کوتاه‌مدت)
   - تبدیل وضعیت FreeCAD به JSON فشرده
   - ارسال به LLM

3. **LLM Orchestrator** (مغز متفکر)
   - مدیریت پرامپت‌ها
   - Function Calling
   - Tool Use

4. **Safe Execution Engine** (دست‌های ایمن)
   - اجرای ایمن با Transactions
   - Abort در صورت خطا

5. **UI Panel** (رابط کاربری)
   - PySide6 Dockable Widget
   - چت‌باکس + Quick Actions

## 💼 استراتژی تجاری

- **مدل درآمدزایی**: Open Core
- **رویکرد فنی**: API-Only (بدون LLM لوکال)
- **Providers**: Claude (پیش‌فرض), OpenAI, OpenRouter, DeepSeek

## 🛠️ استک فنی

- **زبان**: Python 3.10+
- **محیط**: FreeCAD 1.1.1
- **UI**: PySide6 (Qt6)
- **LLM**: API-Only Abstraction Layer

## 📋 وضعیت فعلی

### ✅ انجام‌شده
- [x] ساختار پوشه‌بندی پروژه
- [x] فایل‌های __init__.py
- [x] مستندات اولیه (README, PROJECT_STATE, DECISIONS_LOG, ARCHITECTURE, CHALLENGES)
- [x] فایل requirements.txt
- [x] فایل .env.example
- [x] ماژول config.py
- [x] ماژول abstraction.py (LLM Layer)
- [x] ماژول manager.py (Context)
- [x] ماژول safe_executor.py
- [x] ماژول panel.py (UI)
- [x] ماژول event_listeners.py
- [x] فایل‌های Init.py و InitGui.py
- [x] تست اولیه

### 🔄 در حال انجام
- [ ] تکمیل قابلیت‌های LLM
- [ ] پیاده‌سازی Event Listeners پیشرفته
- [ ] بهبود UI

### ⏳ برنامه‌ریزی‌شده
- [ ] Agentهای تخصصی
- [ ] پشتیبانی از زبان فارسی
- [ ] مستندات کامل API

## 🔗 لینک‌های مرتبط

- [GitHub Repository](https://github.com/yourusername/freecad-ai-assistant)
- [FreeCAD Documentation](https://wiki.freecad.org/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)

## 📝 یادداشت‌ها

- پروژه کاملاً API-Only است (بدون Ollama یا LLM لوکال)
- تمرکز بر روی FreeCAD 1.x با PySide6
- استفاده از Transactions برای ایمنی

---
*آخرین به‌روزرسانی: 2026-07-05*
