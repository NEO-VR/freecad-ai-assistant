"""
FreeCAD AI Assistant - Event Listeners

این ماژول رویدادهای FreeCAD را شنود و پردازش می‌کند.
"""

import logging
from typing import Callable, Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class EventType(Enum):
    """انواع رویدادهای FreeCAD"""
    DOCUMENT_CREATED = "DocumentCreated"
    DOCUMENT_CLOSED = "DocumentClosed"
    OBJECT_ADDED = "ObjectAdded"
    OBJECT_REMOVED = "ObjectRemoved"
    SELECTION_CHANGED = "SelectionChanged"
    SKETCH_MODIFIED = "SketchModified"
    PROPERTY_CHANGED = "PropertyChanged"
    TRANSACTION_COMMIT = "TransactionCommit"
    TRANSACTION_ABORT = "TransactionAbort"


@dataclass
class Event:
    """
    ساختار یک رویداد
    
    Attributes:
        type: نوع رویداد
        data: داده‌های رویداد
        timestamp: زمان وقوع
    """
    type: EventType
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__('time').time())


class EventListener:
    """
    شنونده رویدادهای FreeCAD
    
    این کلاس از Observer Pattern برای شنود رویدادها استفاده می‌کند.
    """
    
    def __init__(self):
        """راه‌اندازی Event Listener"""
        self._freecad = None
        self._callbacks: Dict[EventType, List[Callable]] = {}
        self._enabled = False
        self._initialize_freecad()
    
    def _initialize_freecad(self) -> None:
        """
        راه‌اندازی اتصال به FreeCAD
        
        سعی می‌کند FreeCAD را import کند.
        """
        try:
            import FreeCAD as App
            self._freecad = App
            logger.info("FreeCAD initialized in Event Listener")
        except ImportError:
            logger.warning("FreeCAD not available - running in mock mode")
            self._freecad = None
    
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        """
        ثبت callback برای یک نوع رویداد
        
        Args:
            event_type: نوع رویداد
            callback: تابع callback
        """
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []
        
        self._callbacks[event_type].append(callback)
        logger.debug(f"Subscribed to {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        """
        حذف callback از یک نوع رویداد
        
        Args:
            event_type: نوع رویداد
            callback: تابع callback
        """
        if event_type in self._callbacks:
            try:
                self._callbacks[event_type].remove(callback)
                logger.debug(f"Unsubscribed from {event_type.value}")
            except ValueError:
                pass
    
    def enable(self) -> None:
        """فعال کردن شنود رویدادها"""
        if self._enabled:
            return
        
        if not self._freecad:
            logger.warning("Cannot enable - FreeCAD not available")
            return
        
        # ثبت callbackهای FreeCAD
        self._register_freecad_callbacks()
        self._enabled = True
        logger.info("Event listener enabled")
    
    def disable(self) -> None:
        """غیرفعال کردن شنود رویدادها"""
        if not self._enabled:
            return
        
        if self._freecad:
            self._unregister_freecad_callbacks()
        
        self._enabled = False
        logger.info("Event listener disabled")
    
    def _register_freecad_callbacks(self) -> None:
        """ثبت callbackها در FreeCAD"""
        if not self._freecad:
            return
        
        try:
            # Document Created
            self._freecad.addEvent(
                "DocumentCreated",
                lambda doc: self._on_event(EventType.DOCUMENT_CREATED, {"document": doc.Name})
            )
            
            # Document Closed
            self._freecad.addEvent(
                "DocumentClosed",
                lambda doc: self._on_event(EventType.DOCUMENT_CLOSED, {"document": doc.Name})
            )
            
            # Object Added
            self._freecad.addEvent(
                "ObjectAdded",
                lambda obj: self._on_event(EventType.OBJECT_ADDED, {
                    "object": obj.Name,
                    "type": str(obj.TypeId),
                    "document": obj.Document.Name if hasattr(obj, 'Document') else None
                })
            )
            
            # Object Removed
            self._freecad.addEvent(
                "ObjectRemoved",
                lambda obj: self._on_event(EventType.OBJECT_REMOVED, {
                    "object": obj.Name
                })
            )
            
            # Selection Changed
            self._freecad.addEvent(
                "SelectionChanged",
                lambda: self._on_event(EventType.SELECTION_CHANGED, {
                    "selected": self._get_selected_objects()
                })
            )
            
            logger.debug("FreeCAD callbacks registered")
            
        except Exception as e:
            logger.error(f"Failed to register FreeCAD callbacks: {e}")
    
    def _unregister_freecad_callbacks(self) -> None:
        """حذف callbackها از FreeCAD"""
        # در حال حاضر FreeCAD API برای unregister مستقیم ندارد
        # با disable کردن، دیگر پردازش نمی‌کنیم
        pass
    
    def _on_event(self, event_type: EventType, data: Dict[str, Any]) -> None:
        """
        مدیریت رویداد داخلی
        
        Args:
            event_type: نوع رویداد
            data: داده‌های رویداد
        """
        if not self._enabled:
            return
        
        event = Event(type=event_type, data=data)
        
        # فراخوانی callbackها
        if event_type in self._callbacks:
            for callback in self._callbacks[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in callback for {event_type.value}: {e}")
        
        logger.debug(f"Event processed: {event_type.value}")
    
    def _get_selected_objects(self) -> List[str]:
        """
        دریافت لیست اشیاء انتخاب‌شده
        
        Returns:
            List[str]: لیست نام اشیاء
        """
        if not self._freecad:
            return []
        
        try:
            selection = self._freecad.Gui.getSelection()
            return [obj.Name for obj in selection]
        except Exception:
            return []
    
    def is_enabled(self) -> bool:
        """
        بررسی وضعیت فعال بودن
        
        Returns:
            bool: True اگر فعال باشد
        """
        return self._enabled


class ContextAwareListener(EventListener):
    """
    شنونده رویدادهای آگاه از Context
    
    این کلاس علاوه بر شنود رویدادها، Context را نیز به‌روز می‌کند.
    """
    
    def __init__(self, context_manager=None):
        """
        راه‌اندازی Context Aware Listener
        
        Args:
            context_manager: نمونه Context Manager
        """
        super().__init__()
        self._context_manager = context_manager
        self._context_history: List[Dict[str, Any]] = []
        self._max_history = 100
    
    def set_context_manager(self, context_manager) -> None:
        """
        تنظیم Context Manager
        
        Args:
            context_manager: نمونه Context Manager
        """
        self._context_manager = context_manager
    
    def _on_event(self, event_type: EventType, data: Dict[str, Any]) -> None:
        """
        مدیریت رویداد با به‌روزرسانی Context
        
        Args:
            event_type: نوع رویداد
            data: داده‌های رویداد
        """
        # فراخوانی parent
        super()._on_event(event_type, data)
        
        # به‌روزرسانی Context
        if self._context_manager and event_type in [
            EventType.OBJECT_ADDED,
            EventType.OBJECT_REMOVED,
            EventType.SELECTION_CHANGED,
            EventType.DOCUMENT_CREATED,
            EventType.DOCUMENT_CLOSED
        ]:
            self._update_context()
    
    def _update_context(self) -> None:
        """به‌روزرسانی Context"""
        if not self._context_manager:
            return
        
        try:
            context = self._context_manager.get_context()
            self._context_history.append(context)
            
            # محدود کردن تاریخچه
            if len(self._context_history) > self._max_history:
                self._context_history.pop(0)
            
            logger.debug(f"Context updated: {len(self._context_history)} entries")
            
        except Exception as e:
            logger.error(f"Failed to update context: {e}")
    
    def get_context_history(self) -> List[Dict[str, Any]]:
        """
        دریافت تاریخچه Context
        
        Returns:
            List[Dict[str, Any]]: لیست Contextها
        """
        return self._context_history.copy()
    
    def clear_context_history(self) -> None:
        """پاک کردن تاریخچه Context"""
        self._context_history.clear()
        logger.debug("Context history cleared")


# نمونه جهانی
_listener: Optional[EventListener] = None
_context_listener: Optional[ContextAwareListener] = None


def get_listener() -> EventListener:
    """
    دریافت نمونه جهانی Event Listener
    
    Returns:
        EventListener: نمونه listener
    """
    global _listener
    
    if _listener is None:
        _listener = EventListener()
    
    return _listener


def get_context_listener(context_manager=None) -> ContextAwareListener:
    """
    دریافت نمونه جهانی Context Aware Listener
    
    Args:
        context_manager: نمونه Context Manager
        
    Returns:
        ContextAwareListener: نمونه listener
    """
    global _context_listener
    
    if _context_listener is None:
        _context_listener = ContextAwareListener(context_manager)
    elif context_manager:
        _context_listener.set_context_manager(context_manager)
    
    return _context_listener
