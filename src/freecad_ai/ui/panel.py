"""
FreeCAD AI Assistant - UI Panel
ایجاد Dock Widget با قابلیت اطمینان بالا
"""
import logging
from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt

logger = logging.getLogger("FreeCAD_AI_UI")

_dock_instance = None

def ensure_dock_created(parent=None):
    """
    ایجاد یا بازیابی Dock Widget
    تضمین می‌کند که فقط یک نمونه از Dock وجود داشته باشد.
    """
    global _dock_instance
    
    if _dock_instance is not None:
        return _dock_instance
        
    try:
        import FreeCADGui as Gui
        mw = Gui.getMainWindow()
        if not mw:
            logger.error("MainWindow not found")
            return None
            
        # بررسی是否存在 قبلی
        for dock in mw.findChildren(QDockWidget):
            if dock.objectName() == "AIAssistantDock":
                _dock_instance = dock
                return dock
        
        # ایجاد جدید
        _dock_instance = QDockWidget("AI Assistant", mw)
        _dock_instance.setObjectName("AIAssistantDock")
        
        # ویجت ساده برای تست
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("🤖 پنل هوشمند آماده است!"))
        
        chat_display = QTextEdit()
        chat_display.setPlaceholderText("محیط چت به زودی فعال می‌شود...")
        chat_display.setReadOnly(True)
        layout.addWidget(chat_display)
        
        _dock_instance.setWidget(widget)
        mw.addDockWidget(Qt.RightDockWidgetArea, _dock_instance)
        
        logger.info("AI Assistant Dock created successfully")
        return _dock_instance
        
    except Exception as e:
        logger.error(f"Failed to create dock: {e}", exc_info=True)
        return None
