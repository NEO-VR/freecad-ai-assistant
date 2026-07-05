"""
FreeCAD AI Assistant - InitGui.py

این فایل Workbench افزونه را در FreeCAD ثبت می‌کند.
"""

import logging

logger = logging.getLogger("FreeCAD_AI")


class AIAssistantWorkbench:
    """
    کلاس Workbench دستیار هوشمند FreeCAD
    
    این کلاس یک Workbench جدید در FreeCAD ثبت می‌کند که
    شامل پنل چت و ابزارهای AI است.
    """
    
    def __init__(self):
        """راه‌اندازی Workbench"""
        self.name = "AIAssistant"
        self.iconText = "🤖"
        self.tooltip = "FreeCAD AI Assistant - Natural Language to 3D Modeling"
        
        # آیکون Workbench (در آینده اضافه می‌شود)
        self.icon = ":/icons/freecad_ai.svg"
    
    def GetClassName(self):
        """
        دریافت نام کلاس GUI
        
        Returns:
            str: نام کلاس
        """
        return "Gui::PythonWorkbench"
    
    def Initialize(self):
        """
        راه‌اندازی Workbench
        
        این تابع توسط FreeCAD فراخوانی می‌شود.
        """
        logger.info("Initializing AI Assistant Workbench")
        
        try:
            # ایمپورت ماژول‌های اصلی
            from freecad_ai.ui.panel import create_ai_dock
            from freecad_ai.core.config import get_config
            from freecad_ai.listeners.event_listeners import get_context_listener
            from freecad_ai.context.manager import get_context_manager
            
            # بارگذاری پیکربندی
            config = get_config()
            logger.info(f"Configuration loaded: {config.default_provider}")
            
            # ایجاد Dock Widget
            import FreeCADGui as Gui
            mw = Gui.getMainWindow()
            
            if mw:
                self.dock = create_ai_dock(mw)
                
                # اضافه کردن به MainWindow
                mw.addDockWidget(2, self.dock)  # Right dock area
                
                logger.info("AI Assistant Dock created and added to MainWindow")
            
            # فعال کردن Event Listeners
            context_manager = get_context_manager()
            listener = get_context_listener(context_manager)
            listener.enable()
            
            logger.info("Event listeners enabled")
            
        except Exception as e:
            logger.error(f"Failed to initialize Workbench: {e}", exc_info=True)
    
    def Activated(self):
        """
        فراخوانی هنگام فعال شدن Workbench
        
        این تابع وقتی کاربر Workbench را انتخاب می‌کند اجرا می‌شود.
        """
        logger.info("AI Assistant Workbench activated")
        
        # نمایش Dock
        try:
            import FreeCADGui as Gui
            mw = Gui.getMainWindow()
            
            if mw and hasattr(self, 'dock'):
                self.dock.show()
                
        except Exception as e:
            logger.error(f"Error in Activated: {e}")
    
    def Deactivated(self):
        """
        فراخوانی هنگام غیرفعال شدن Workbench
        
        این تابع وقتی کاربر به Workbench دیگری می‌رود اجرا می‌شود.
        """
        logger.debug("AI Assistant Workbench deactivated")
    
    def ContextMenu(self, recipient):
        """
        ایجاد منوی Context
        
        Args:
            recipient: دریافت‌کننده منو
        """
        pass
    
    def GetToolbars(self):
        """
        تعریف Toolbarها
        
        Returns:
            tuple: لیست Toolbarها
        """
        return (
            ("&AI Assistant", [
                "AI_Chat",
                "AI_Settings",
                "AI_Help"
            ])
        )
    
    def GetMenus(self):
        """
        تعریف Menuها
        
        Returns:
            tuple: لیست Menuها
        """
        return (
            ("&AI Assistant", [
                "AI_Chat",
                "AI_Settings",
                "AI_Help"
            ])
        )


# ثبت Workbench در FreeCAD
def register_workbench():
    """
    ثبت Workbench در FreeCAD
    
    این تابع باید از داخل FreeCAD فراخوانی شود.
    """
    import FreeCADGui as Gui
    
    # ایجاد نمونه Workbench
    workbench = AIAssistantWorkbench()
    
    # ثبت در FreeCAD
    Gui.addWorkbench(workbench)
    
    logger.info("AI Assistant Workbench registered successfully")


# اجرای خودکار هنگام لود شدن
if __name__ != "__main__":
    # در محیط FreeCAD
    try:
        register_workbench()
    except Exception as e:
        logger.error(f"Failed to register workbench: {e}")
