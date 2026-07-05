"""
FreeCAD AI Assistant - InitGui.py
Workbench registration for FreeCAD

این فایل Workbench افزونه را در FreeCAD ثبت می‌کند.
نسخه ساده‌سازی شده برای جلوگیری از خطاهای startup
"""

import FreeCAD
import FreeCADGui as Gui


class AIAssistantWorkbench(Workbench):
    """
    AI Assistant Workbench for FreeCAD
    
    This workbench provides a natural language interface to FreeCAD,
    allowing users to create and modify 3D models using AI.
    
    کلاس Workbench دستیار هوشمند FreeCAD
    این کلاس یک Workbench جدید در FreeCAD ثبت می‌کند که
    شامل پنل چت و ابزارهای AI است.
    """
    
    ClassName = "AIAssistantWorkbench"
    Icon = """
        /* XPM */
        static char * icon_xpm[] = {
        "16 16 4 1",
        "c None",
        ". #A0A0A0",
        "X #404040",
        "o #FFFFFF",
        "                ",
        "   .XXXXXXX.    ",
        "  .XXXXXXXXX.   ",
        " .XXXXXXXXXXX.  ",
        " .XXXXXXXXXXX.  ",
        " .XXXoXXXoXXX.  ",
        " .XXXXXXXXXXX.  ",
        " .XXXXXXXXXXX.  ",
        " .XXXXXXXXXXX.  ",
        " .XXXXXXXXXXX.  ",
        " .XXXXXXXXXXX.  ",
        " .XXXXXXXXXXX.  ",
        "  'XXXXXXXXX'   ",
        "    'XXXXX'     ",
        "                ",
        "                "};
    """
    MenuText = "AI Assistant"
    ToolTip = "FreeCAD AI Assistant - Natural Language to 3D Modeling"
    
    def Initialize(self):
        """
        Initialize the workbench
        
        This method is called when FreeCAD starts up.
        We keep it minimal to avoid startup errors.
        
        راه‌اندازی Workbench - این تابع توسط FreeCAD فراخوانی می‌شود.
        """
        # Define commands (will be implemented in future steps)
        # For now, we just define placeholders
        # تعریف دستورها (در مراحل بعدی پیاده‌سازی می‌شوند)
        commands = [
            "AI_Chat",
            "AI_Settings"
        ]
        
        # Create toolbar
        # ایجاد نوار ابزار
        self.appendToolbar("AI Assistant", commands)
        
        # Create menu
        # ایجاد منو
        self.appendMenu("AI Assistant", commands)
        
        FreeCAD.Console.PrintMessage("AI Assistant Workbench initialized\n")
    
    def Activated(self):
        """
        Called when workbench is activated
        
        This is the best place to initialize the UI panel lazily.
        
        فراخوانی هنگام فعال شدن Workbench
        این تابع وقتی کاربر Workbench را انتخاب می‌کند اجرا می‌شود.
        """
        FreeCAD.Console.PrintMessage("AI Assistant Workbench activated\n")
        
        # Lazy loading of the UI panel to avoid import errors at startup
        # بارگذاری تنبلانه پنل UI برای جلوگیری از خطاهای ایمپورت هنگام startup
        try:
            from freecad_ai.ui.panel import ensure_dock_created
            ensure_dock_created()
        except Exception as e:
            FreeCAD.Console.PrintError(f"Failed to create AI Assistant dock: {e}\n")
    
    def Deactivated(self):
        """
        Called when workbench is deactivated
        
        فراخوانی هنگام غیرفعال شدن Workbench
        این تابع وقتی کاربر به Workbench دیگری می‌رود اجرا می‌شود.
        """
        FreeCAD.Console.PrintMessage("AI Assistant Workbench deactivated\n")
    
    def GetClassName(self):
        """
        Return the class name
        
        Returns:
            str: The GUI class name
            
        دریافت نام کلاس GUI
        """
        return "Gui::PythonWorkbench"
    
    def ContextMenu(self, recipient):
        """
        Create context menu
        
        Args:
            recipient: The recipient of the menu ("view" or "tree")
            
        ایجاد منوی Context
        """
        # Add context menu items if needed
        pass
    
    def GetToolbars(self):
        """
        Return list of toolbars
        
        Returns:
            tuple: List of toolbars
            
        تعریف Toolbarها
        """
        return (
            ("&AI Assistant", [
                "AI_Chat",
                "AI_Settings"
            ])
        )
    
    def GetMenus(self):
        """
        Return list of menus
        
        Returns:
            tuple: List of menus
            
        تعریف Menuها
        """
        return (
            ("&AI Assistant", [
                "AI_Chat",
                "AI_Settings"
            ])
        )


# Register workbench
# ثبت Workbench در FreeCAD
# این کد بلافاصله پس از ایمپورت فایل اجرا می‌شود
Gui.addWorkbench(AIAssistantWorkbench())
FreeCAD.Console.PrintMessage("AI Assistant Workbench registered\n")
