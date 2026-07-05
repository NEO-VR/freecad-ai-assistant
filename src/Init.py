"""
FreeCAD AI Assistant - Init.py

این فایل توسط FreeCAD هنگام بارگذاری ماژول اجرا می‌شود.
"""

# نسخه افزونه
__version__ = "0.1.0"

# متادیتا
__title__ = "FreeCAD AI Assistant"
__author__ = "FreeCAD AI Team"
__license__ = "MIT"

def Initialize():
    """
    تابع راه‌اندازی اولیه ماژول
    
    این تابع توسط FreeCAD فراخوانی می‌شود.
    """
    import logging
    
    # تنظیم logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger("FreeCAD_AI")
    logger.info("FreeCAD AI Assistant module loaded")
    
    # ایمپورت پکیج اصلی برای اطمینان از در دسترس بودن
    try:
        import freecad_ai
        logger.info(f"freecad_ai package imported successfully (v{freecad_ai.__version__})")
    except ImportError as e:
        logger.error(f"Failed to import freecad_ai: {e}")


# ثبت تابع Initialize برای FreeCAD
__all__ = ['Initialize']
