"""
FreeCAD AI Assistant - UI Panel (PySide6)

این ماژول رابط کاربری افزونه را با استفاده از PySide6 (Qt6) ایجاد می‌کند.
"""

import logging
from typing import Optional, Callable
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem, QDockWidget
)
from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QFont, QIcon

logger = logging.getLogger(__name__)


class ChatMessage(QFrame):
    """
    ویجت نمایش یک پیام چت
    
    Attributes:
        message_sent: سیگنال ارسال پیام
    """
    
    def __init__(self, text: str, is_user: bool = True, parent=None):
        """
        راه‌اندازی پیام چت
        
        Args:
            text: متن پیام
            is_user: آیا پیام از طرف کاربر است
            parent: والد ویجت
        """
        super().__init__(parent)
        self.is_user = is_user
        self.setup_ui(text)
    
    def setup_ui(self, text: str) -> None:
        """راه‌اندازی UI پیام"""
        # استایل‌دهی بر اساس نوع پیام
        if self.is_user:
            self.setStyleSheet("""
                QFrame {
                    background-color: #0078d4;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #f0f0f0;
                    color: black;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
        
        # لی‌اوت
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # لیبل متن
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(label)
        
        # تنظیم اندازه
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class AIPanelWidget(QWidget):
    """
    ویجت اصلی پنل AI Assistant
    
    شامل:
    - ناحیه چت
    - ورودی متن
    - دکمه ارسال
    - ورودی API Key
    """
    
    # سیگنال‌ها
    message_sent = Signal(str)
    api_key_changed = Signal(str)
    
    def __init__(self, parent=None):
        """
        راه‌اندازی پنل AI
        
        Args:
            parent: والد ویجت
        """
        super().__init__(parent)
        self.setup_ui()
        logger.info("AI Panel Widget initialized")
    
    def setup_ui(self) -> None:
        """راه‌اندازی کامل UI"""
        # لی‌اوت اصلی
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # عنوان
        title_label = QLabel("🤖 FreeCAD AI Assistant")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # ناحیه چت (Scroll Area)
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # کانتینر پیام‌ها
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.addStretch()
        
        self.chat_scroll.setWidget(self.messages_container)
        self.chat_scroll.setMinimumHeight(300)
        main_layout.addWidget(self.chat_scroll)
        
        # ورودی API Key
        api_layout = QHBoxLayout()
        api_label = QLabel("API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("sk-ant-...")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.textChanged.connect(self.api_key_changed.emit)
        
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_key_input)
        main_layout.addLayout(api_layout)
        
        # ورودی متن و دکمه ارسال
        input_layout = QHBoxLayout()
        
        # ورودی متن
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("پیام خود را بنویسید... (فارسی/انگلیسی)")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        # دکمه ارسال
        self.send_button = QPushButton("ارسال")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setMinimumWidth(80)
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)
        
        # پیام خوش‌آمدگویی
        self.add_message("سلام! من دستیار هوشمند FreeCAD هستم. چطور می‌توانم کمک کنم؟", is_user=False)
    
    @Slot()
    def send_message(self) -> None:
        """ارسال پیام کاربر"""
        text = self.message_input.text().strip()
        
        if not text:
            return
        
        # اضافه کردن پیام به چت
        self.add_message(text, is_user=True)
        
        # پاک کردن ورودی
        self.message_input.clear()
        
        # ارسال سیگنال
        self.message_sent.emit(text)
        
        logger.debug(f"User message sent: {text[:50]}...")
    
    def add_message(self, text: str, is_user: bool = True) -> None:
        """
        اضافه کردن پیام به چت
        
        Args:
            text: متن پیام
            is_user: آیا پیام از طرف کاربر است
        """
        message_widget = ChatMessage(text, is_user, self)
        
        # اضافه کردن قبل از stretch
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, message_widget)
        
        # اسکرول به پایین
        self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        )
    
    def add_assistant_message(self, text: str) -> None:
        """
        اضافه کردن پیام از طرف دستیار
        
        Args:
            text: متن پیام
        """
        self.add_message(text, is_user=False)
    
    def clear_chat(self) -> None:
        """پاک کردن تمام پیام‌های چت"""
        # حذف تمام ویجت‌ها به جز stretch
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def set_api_key(self, key: str) -> None:
        """
        تنظیم API Key
        
        Args:
            key: کلید API
        """
        self.api_key_input.setText(key)
    
    def get_api_key(self) -> str:
        """
        دریافت API Key فعلی
        
        Returns:
            str: کلید API
        """
        return self.api_key_input.text().strip()
    
    def enable_send(self, enabled: bool = True) -> None:
        """
        فعال/غیرفعال کردن دکمه ارسال
        
        Args:
            enabled: وضعیت فعال بودن
        """
        self.send_button.setEnabled(enabled)
        self.message_input.setEnabled(enabled)


class AIDockWidget(QDockWidget):
    """
    Dock Widget برای پنل AI
    
    این کلاس پنل را به عنوان یک Dock در FreeCAD ثبت می‌کند.
    """
    
    def __init__(self, parent=None):
        """
        راه‌اندازی Dock Widget
        
        Args:
            parent: والد ویجت (معمولاً MainWindow FreeCAD)
        """
        super().__init__("AI Assistant", parent)
        
        # تنظیمات Dock
        self.setObjectName("AIDockWidget")
        self.setMinimumWidth(350)
        self.setMinimumHeight(500)
        
        # ایجاد ویجت اصلی
        self.ai_panel = AIPanelWidget(self)
        self.setWidget(self.ai_panel)
        
        # اتصال سیگنال‌ها
        self.ai_panel.message_sent.connect(self._on_message_sent)
        
        logger.info("AI Dock Widget initialized")
    
    @Slot(str)
    def _on_message_sent(self, message: str) -> None:
        """
        مدیریت پیام ارسالی کاربر
        
        Args:
            message: متن پیام
        """
        logger.debug(f"Message sent from dock: {message[:50]}...")
        # اینجا باید به LLM Orchestrator متصل شود
    
    def get_panel(self) -> AIPanelWidget:
        """
        دریافت پنل AI
        
        Returns:
            AIPanelWidget: نمونه پنل
        """
        return self.ai_panel


# تابع کمکی برای ایجاد Dock
def create_ai_dock(main_window=None) -> AIDockWidget:
    """
    ایجاد Dock Widget AI Assistant
    
    Args:
        main_window: پنجره اصلی FreeCAD
        
    Returns:
        AIDockWidget: نمونه Dock
    """
    dock = AIDockWidget(main_window)
    return dock
