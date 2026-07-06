"""
FreeCAD AI Assistant - UI Panel
شامل تابع ensure_dock_created برای ایجاد پنل چت
"""
import FreeCADGui as Gui
from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt

def ensure_dock_created():
    """ایجاد Dock Widget اگر وجود ندارد"""
    mw = Gui.getMainWindow()
    if not mw:
        return None
    
    # بررسی تکراری نبودن
    for dock in mw.findChildren(QDockWidget):
        if dock.objectName() == "AIAssistantDock":
            return dock
    
    # ساخت پنل جدید
    dock = QDockWidget("AI Assistant", mw)
    dock.setObjectName("AIAssistantDock")
    
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    # متن وضعیت
    status_lbl = QLabel("پنل هوشمند آماده است.\nمحیط چت بزودی آماده میشود...")
    status_lbl.setAlignment(Qt.AlignCenter)
    layout.addWidget(status_lbl)
    
    dock.setWidget(widget)
    mw.addDockWidget(Qt.RightDockWidgetArea, dock)
    return dock
