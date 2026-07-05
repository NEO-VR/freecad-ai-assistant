"""
FreeCAD AI Assistant - Safe Execution Engine

این ماژول اجرای ایمن کد را با استفاده از FreeCAD Transactions مدیریت می‌کند.
"""

import logging
from typing import Optional, Callable, Any
import traceback

logger = logging.getLogger(__name__)


class TransactionError(Exception):
    """خطای مربوط به Transaction"""
    pass


class SafeExecutor:
    """
    موتور اجرای ایمن کد
    
    این کلاس تضمین می‌کند که تمام عملیات‌های تغییر مدل
    داخل Transaction اجرا شده و در صورت خطا بازگشت می‌شوند.
    
    مکانیزم:
    1. قبل از اجرا Transaction باز می‌شود
    2. کد اجرا می‌شود
    3. در صورت موفقیت: Commit
    4. در صورت خطا: Abort
    """
    
    def __init__(self):
        """راه‌اندازی Safe Executor"""
        self._freecad = None
        self._transaction_depth = 0
        self._current_transaction_name: Optional[str] = None
        self._initialize_freecad()
    
    def _initialize_freecad(self) -> None:
        """
        راه‌اندازی اتصال به FreeCAD
        
        سعی می‌کند FreeCAD را import کند.
        """
        try:
            import FreeCAD as App
            self._freecad = App
            logger.info("FreeCAD initialized in Safe Executor")
        except ImportError:
            logger.warning("FreeCAD not available - running in mock mode")
            self._freecad = None
    
    def execute(
        self, 
        code: str, 
        transaction_name: str = "AI Assistant Operation",
        context: Optional[dict] = None
    ) -> bool:
        """
        اجرای ایمن کد Python
        
        Args:
            code: کد Python برای اجرا
            transaction_name: نام Transaction
            context: دیکشنری context برای exec
            
        Returns:
            bool: True اگر اجرا موفق بود، False در صورت خطا
        """
        if not self._freecad:
            logger.warning("FreeCAD not available - simulating execution")
            return self._mock_execute(code)
        
        doc = self._freecad.ActiveDocument
        if not doc:
            logger.error("No active document")
            return False
        
        try:
            # باز کردن Transaction فقط اگر تو در تو نیست
            if self._transaction_depth == 0:
                doc.openTransaction(transaction_name)
                self._current_transaction_name = transaction_name
                logger.debug(f"Transaction opened: {transaction_name}")
            
            self._transaction_depth += 1
            
            # آماده‌سازی context
            exec_context = context if context else {}
            
            # اضافه کردن دسترسی به FreeCAD
            exec_context['App'] = self._freecad
            exec_context['doc'] = doc
            
            # اجرای کد
            exec(code, exec_context)
            
            # کاهش عمق Transaction
            self._transaction_depth -= 1
            
            # Commit فقط اگر به سطح ۰ رسیدیم
            if self._transaction_depth == 0:
                doc.commitTransaction()
                logger.info(f"Transaction committed: {transaction_name}")
                self._current_transaction_name = None
            
            return True
            
        except Exception as e:
            # کاهش عمق Transaction
            self._transaction_depth -= 1
            
            # Abort فقط اگر به سطح ۰ رسیدیم
            if self._transaction_depth == 0:
                doc.abortTransaction()
                logger.error(f"Transaction aborted: {transaction_name}")
                self._current_transaction_name = None
            
            # لاگ خطا
            error_msg = f"Execution failed: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            
            return False
    
    def execute_function(
        self,
        func: Callable,
        *args,
        transaction_name: str = "AI Assistant Operation",
        **kwargs
    ) -> Any:
        """
        اجرای ایمن یک تابع
        
        Args:
            func: تابع برای اجرا
            *args: آرگومان‌های تابع
            transaction_name: نام Transaction
            **kwargs: آرگومان‌های کلیدی
            
        Returns:
            Any: خروجی تابع یا None در صورت خطا
        """
        if not self._freecad:
            logger.warning("FreeCAD not available - simulating function execution")
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Mock execution failed: {e}")
                return None
        
        doc = self._freecad.ActiveDocument
        if not doc:
            logger.error("No active document")
            return None
        
        try:
            # باز کردن Transaction
            if self._transaction_depth == 0:
                doc.openTransaction(transaction_name)
                self._current_transaction_name = transaction_name
            
            self._transaction_depth += 1
            
            # اجرای تابع
            result = func(*args, **kwargs)
            
            # کاهش عمق
            self._transaction_depth -= 1
            
            # Commit
            if self._transaction_depth == 0:
                doc.commitTransaction()
                self._current_transaction_name = None
            
            return result
            
        except Exception as e:
            # کاهش عمق
            self._transaction_depth -= 1
            
            # Abort
            if self._transaction_depth == 0:
                doc.abortTransaction()
                self._current_transaction_name = None
            
            logger.error(f"Function execution failed: {e}")
            logger.error(traceback.format_exc())
            
            return None
    
    def _mock_execute(self, code: str) -> bool:
        """
        اجرای ساختگی برای حالت تست
        
        Args:
            code: کد Python
            
        Returns:
            bool: همیشه True برمی‌گرداند
        """
        logger.info(f"Mock execution: {code[:50]}...")
        return True
    
    def is_in_transaction(self) -> bool:
        """
        بررسی اینکه آیا درون Transaction هستیم
        
        Returns:
            bool: True اگر در Transaction باشیم
        """
        return self._transaction_depth > 0
    
    def get_current_transaction(self) -> Optional[str]:
        """
        دریافت نام Transaction فعلی
        
        Returns:
            Optional[str]: نام Transaction یا None
        """
        return self._current_transaction_name
    
    def validate_code(self, code: str) -> tuple[bool, str]:
        """
        اعتبارسنجی کد قبل از اجرا
        
        Args:
            code: کد Python
            
        Returns:
            tuple[bool, str]: (معتبر است, پیام)
        """
        # بررسی‌های امنیتی
        dangerous_patterns = [
            'import os',
            'import sys',
            '__import__',
            'eval(',
            'exec(',
            'open(',
            'subprocess',
            'os.system',
            'shutil'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                return False, f"کد حاوی الگوی خطرناک است: {pattern}"
        
        # بررسی طول کد
        if len(code) > 10000:
            return False, "کد بسیار طولانی است"
        
        return True, "کد معتبر است"


# نمونه جهانی
_executor: Optional[SafeExecutor] = None


def get_executor() -> SafeExecutor:
    """
    دریافت نمونه جهانی Safe Executor
    
    Returns:
        SafeExecutor: نمونه executor
    """
    global _executor
    
    if _executor is None:
        _executor = SafeExecutor()
    
    return _executor


def safe_execute(code: str, **kwargs) -> bool:
    """
    تابع کمکی برای اجرای ایمن کد
    
    Args:
        code: کد Python
        **kwargs: آرگومان‌های اضافی برای execute
        
    Returns:
        bool: نتیجه اجرا
    """
    executor = get_executor()
    return executor.execute(code, **kwargs)
