"""
FreeCAD AI Assistant - Context Manager

این ماژول وضعیت فعلی FreeCAD را جمع‌آوری و به JSON تبدیل می‌کند.
"""

import logging
from typing import Dict, Any, List, Optional
import json

logger = logging.getLogger(__name__)


class ContextManager:
    """
    مدیریت Context (وضعیت فعلی) FreeCAD
    
    این کلاس اطلاعات زیر را جمع‌آوری می‌کند:
    - سند فعال
    - اشیاء انتخاب‌شده
    - Sketch فعال
    - واحدهای مدل
    - لیست اشیاء سند
    """
    
    def __init__(self):
        """راه‌اندازی Context Manager"""
        self._freecad = None
        self._initialize_freecad()
    
    def _initialize_freecad(self) -> None:
        """
        راه‌اندازی اتصال به FreeCAD
        
        سعی می‌کند FreeCAD را import کند.
        """
        try:
            import FreeCAD as App
            self._freecad = App
            logger.info("FreeCAD initialized in Context Manager")
        except ImportError:
            logger.warning("FreeCAD not available - running in mock mode")
            self._freecad = None
    
    def get_context(self) -> Dict[str, Any]:
        """
        دریافت وضعیت فعلی FreeCAD
        
        Returns:
            Dict[str, Any]: دیکشنری JSON-compatible از وضعیت
        """
        if not self._freecad:
            return self._get_mock_context()
        
        context = {
            "active_document": self._get_active_document_name(),
            "selected_objects": self._get_selected_objects(),
            "active_sketch": self._get_active_sketch(),
            "model_units": self._get_model_units(),
            "document_objects": self._get_document_objects(),
            "workbench": self._get_current_workbench()
        }
        
        logger.debug(f"Context collected: {json.dumps(context, indent=2)}")
        return context
    
    def _get_active_document_name(self) -> Optional[str]:
        """
        دریافت نام سند فعال
        
        Returns:
            Optional[str]: نام سند یا None
        """
        if not self._freecad:
            return None
        
        doc = self._freecad.ActiveDocument
        return doc.Name if doc else None
    
    def _get_selected_objects(self) -> List[str]:
        """
        دریافت لیست اشیاء انتخاب‌شده
        
        Returns:
            List[str]: لیست نام اشیاء
        """
        if not self._freecad:
            return []
        
        selection = self._freecad.Gui.getSelection()
        return [obj.Name for obj in selection]
    
    def _get_active_sketch(self) -> Optional[str]:
        """
        دریافت Sketch فعال
        
        Returns:
            Optional[str]: نام Sketch یا None
        """
        if not self._freecad:
            return None
        
        # بررسی اشیاء انتخاب‌شده برای Sketch
        selection = self._freecad.Gui.getSelection()
        for obj in selection:
            if hasattr(obj, "TypeId"):
                # بررسی نوع Sketch
                if "Sketcher::SketchObject" in str(obj.TypeId):
                    return obj.Name
        
        return None
    
    def _get_model_units(self) -> str:
        """
        دریافت واحدهای مدل
        
        Returns:
            str: واحد اندازه‌گیری (mm/inch)
        """
        if not self._freecad:
            return "mm"
        
        # در FreeCAD واحدها معمولاً mm هستند
        # می‌توان از Document.Meta برای ذخیره واحد استفاده کرد
        doc = self._freecad.ActiveDocument
        if doc:
            unit = doc.Meta.get("Unit", "mm")
            return unit
        
        return "mm"
    
    def _get_document_objects(self) -> List[Dict[str, str]]:
        """
        دریافت لیست تمام اشیاء سند فعال
        
        Returns:
            List[Dict[str, str]]: لیست اشیاء با نام و نوع
        """
        if not self._freecad:
            return []
        
        doc = self._freecad.ActiveDocument
        if not doc:
            return []
        
        objects = []
        for obj in doc.Objects:
            objects.append({
                "name": getattr(obj, 'Name', 'Unknown'),
                "label": getattr(obj, 'Label', ''),
                "type": str(getattr(obj, 'TypeId', ''))
            })
        
        return objects
    
    def _get_current_workbench(self) -> Optional[str]:
        """
        دریافت Workbench فعلی
        
        Returns:
            Optional[str]: نام Workbench
        """
        if not self._freecad:
            return None
        
        try:
            # دسترسی به Gui برای دریافت Workbench فعال
            if hasattr(self._freecad, 'Gui'):
                return self._freecad.Gui.activeWorkbench().name()
        except Exception:
            pass
        
        return None
    
    def _get_mock_context(self) -> Dict[str, Any]:
        """
        دریافت Context ساختگی برای حالت تست
        
        Returns:
            Dict[str, Any]: Context ساختگی
        """
        return {
            "active_document": "MockDocument",
            "selected_objects": [],
            "active_sketch": None,
            "model_units": "mm",
            "document_objects": [],
            "workbench": "PartDesign"
        }
    
    def format_for_llm(self, context: Dict[str, Any]) -> str:
        """
        فرمت‌دهی Context برای ارسال به LLM
        
        Args:
            context: دیکشنری Context
            
        Returns:
            str: متن فرمت‌شده
        """
        formatted = [
            "=== Current FreeCAD Context ===",
            f"Active Document: {context.get('active_document', 'None')}",
            f"Selected Objects: {', '.join(context.get('selected_objects', [])) or 'None'}",
            f"Active Sketch: {context.get('active_sketch') or 'None'}",
            f"Model Units: {context.get('model_units', 'mm')}",
            f"Current Workbench: {context.get('workbench') or 'Unknown'}",
            "",
            "Document Objects:"
        ]
        
        for obj in context.get('document_objects', []):
            formatted.append(f"  - {obj['name']} ({obj['type']})")
        
        return "\n".join(formatted)
    
    def get_context_summary(self) -> str:
        """
        دریافت خلاصه Context برای ارسال به LLM
        
        Returns:
            str: خلاصه متنی Context
        """
        context = self.get_context()
        return self.format_for_llm(context)


# نمونه جهانی
_context_manager: Optional[ContextManager] = None


def get_context_manager() -> ContextManager:
    """
    دریافت نمونه جهانی Context Manager
    
    Returns:
        ContextManager: نمونه مدیریت Context
    """
    global _context_manager
    
    if _context_manager is None:
        _context_manager = ContextManager()
    
    return _context_manager
