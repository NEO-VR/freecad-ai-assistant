"""
FreeCAD AI Assistant - UI Panel (Phase 3 Final)
پنل چت هوشمند با اتصال خودکار به LLM
"""
import logging
from PySide6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QFrame, QApplication, QScrollArea
)
from PySide6.QtCore import Qt, Signal, Slot, QThread, QTimer
from PySide6.QtGui import QFont, QColor
import sys
import os

logger = logging.getLogger("FreeCAD_AI_UI")

class WorkerThread(QThread):
    """رشته پردازش جداگانه برای جلوگیری از فریز شدن UI"""
    response_ready = Signal(str)
    error_occurred = Signal(str)
    finished_signal = Signal()

    def __init__(self, orchestrator, message, history):
        super().__init__()
        self.orchestrator = orchestrator
        self.message = message
        self.history = history

    def run(self):
        try:
            from freecad_ai.llm.abstraction import Message
            
            messages = [Message(role="system", content="You are a helpful FreeCAD assistant. Respond in the same language as the user.")]
            for role, content in self.history:
                messages.append(Message(role=role, content=content))
            messages.append(Message(role="user", content=self.message))

            provider = self.orchestrator.get_default_provider()
            if not provider:
                self.error_occurred.emit("هیچ ارائه‌دهنده‌ای پیکربندی نشده است.")
                return

            response = provider.chat(messages=messages)
            text = provider.parse_response(response)
            
            self.response_ready.emit(text)
        except Exception as e:
            logger.error(f"Error in worker thread: {e}", exc_info=True)
            self.error_occurred.emit(str(e))
        finally:
            self.finished_signal.emit()

class AIPanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_history = []
        self.orchestrator = None
        self.is_connected = False
        self.worker = None
        
        self.init_ui()
        
        # تأخیر کوتاه برای اطمینان از لود شدن کامل UI قبل از چک کردن اتصال
        QTimer.singleShot(500, self.check_connection)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        # هدر
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_frame.setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")
        
        title_label = QLabel("🤖 دستیار هوشمند FreeCAD")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        self.status_label = QLabel("⏳ در حال بررسی اتصال...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: orange; font-weight: bold; font-size: 10px;")
        header_layout.addWidget(self.status_label)

        layout.addWidget(header_frame)

        # ناحیه چت
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("پیام‌های شما و پاسخ هوش مصنوعی اینجا نمایش داده می‌شوند...")
        self.chat_display.setFont(QFont("Tahoma", 9))
        self.chat_display.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 4px;")
        layout.addWidget(self.chat_display)

        # ورودی متن
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("پیام خود را بنویسید (مثلاً: سلام)...")
        self.input_field.setFont(QFont("Tahoma", 9))
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setEnabled(False)  # پیش‌فرض غیرفعال
        layout.addWidget(self.input_field)

        # دکمه ارسال
        self.send_button = QPushButton("ارسال پیام")
        self.send_button.setFont(QFont("Tahoma", 9, QFont.Bold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white; padding: 6px;
                border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:disabled { background-color: #cccccc; color: #666666; }
        """)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setEnabled(False)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def check_connection(self):
        """بررسی اتصال به LLM و فعال‌سازی UI"""
        try:
            from freecad_ai.core.config import get_config
            from freecad_ai.llm.abstraction import LLMOrchestrator

            config = get_config()
            
            config_dict = {
                "anthropic_api_key": getattr(config, 'anthropic_api_key', None),
                "openai_api_key": getattr(config, 'openai_api_key', None),
                "openrouter_api_key": getattr(config, 'openrouter_api_key', None),
                "deepseek_api_key": getattr(config, 'deepseek_api_key', None),
                "default_provider": getattr(config, 'default_provider', 'claude'),
                "default_model": getattr(config, 'default_model', 'claude-sonnet-4-6')
            }

            has_key = any([
                config_dict.get("anthropic_api_key"),
                config_dict.get("openai_api_key"),
                config_dict.get("openrouter_api_key"),
                config_dict.get("deepseek_api_key")
            ])

            if has_key:
                self.orchestrator = LLMOrchestrator(config=config_dict)
                available = self.orchestrator.list_available_providers()
                
                if available:
                    self.is_connected = True
                    provider_name = available[0].upper()
                    self.status_label.setText(f"✅ متصل به {provider_name}")
                    self.status_label.setStyleSheet("color: green; font-weight: bold; font-size: 10px;")
                    
                    # فعال‌سازی ورودی‌ها
                    self.input_field.setEnabled(True)
                    self.send_button.setEnabled(True)
                    self.input_field.setFocus()
                    
                    msg = f"به {provider_name} متصل شد. آماده دریافت دستور هستم!"
                    self.append_to_chat("سیستم", msg)
                    logger.info(f"Connected to {provider_name}")
                else:
                    self.status_label.setText("❌ کلید API نامعتبر است")
                    self.status_label.setStyleSheet("color: red; font-weight: bold;")
                    self.append_to_chat("سیستم", "خطا: کلید API یافت شد اما معتبر نیست.")
            else:
                self.status_label.setText("❌ کلید API یافت نشد")
                self.status_label.setStyleSheet("color: red; font-weight: bold;")
                self.append_to_chat("سیستم", "خطا: لطفاً فایل .env را بررسی کنید.")

        except Exception as e:
            logger.error(f"Connection check failed: {e}", exc_info=True)
            self.status_label.setText("❌ خطا در اتصال")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.append_to_chat("سیستم", f"خطا: {str(e)}")

    def send_message(self):
        text = self.input_field.text().strip()
        if not text or not self.is_connected:
            return

        # ذخیره در تاریخچه قبل از پاک کردن
        self.chat_history.append(("user", text))
        
        self.append_to_chat("شما", text)
        self.input_field.clear()
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.status_label.setText("⏳ در حال تفکر...")
        self.status_label.setStyleSheet("color: orange; font-weight: bold;")

        self.worker = WorkerThread(self.orchestrator, text, self.chat_history)
        self.worker.response_ready.connect(self.handle_response)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.finished_signal.connect(self.reset_ui_state)
        self.worker.start()

    def handle_response(self, response_text):
        self.chat_history.append(("assistant", response_text))
        self.append_to_chat("هوش مصنوعی", response_text)

    def handle_error(self, error_msg):
        self.append_to_chat("خطا", error_msg)

    def reset_ui_state(self):
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        if self.is_connected:
            self.status_label.setText(f"✅ متصل")
            self.status_label.setStyleSheet("color: green; font-weight: bold; font-size: 10px;")
        self.input_field.setFocus()

    def append_to_chat(self, sender, message):
        color = "#000080" if sender == "شما" else ("#d32f2f" if sender == "خطا" else "#2e7d32")
        self.chat_display.append(f'<b style="color:{color};">{sender}:</b> {message}')
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

def create_ai_dock(parent=None):
    dock = QDockWidget("AI Assistant", parent)
    dock.setObjectName("AIAssistantDock")
    widget = AIPanelWidget(dock)
    dock.setWidget(widget)
    return dock
