"""
FreeCAD AI Assistant - InitGui.py
Workbench registration for FreeCAD
"""
import FreeCAD
import FreeCADGui as Gui

class AIAssistantWorkbench(Workbench):
    """AI Assistant Workbench for FreeCAD"""
    
    MenuText = "AI Assistant"
    ToolTip = "FreeCAD AI Assistant - Natural Language to 3D Modeling"
    # استفاده از آیکون استاندارد فری‌کد برای جلوگیری از خطا
    Icon = "freecad" 

    def Initialize(self):
        """Initialize the workbench"""
        # ثبت دستورات
        from freecad_ai import commands
        
        commands_list = ["AI_Chat", "AI_Settings"]
        
        self.appendToolbar("AI Assistant", commands_list)
        self.appendMenu("AI Assistant", commands_list)
        
        FreeCAD.Console.PrintMessage("✅ AI Assistant Workbench initialized\n")

    def Activated(self):
        """Called when workbench is activated"""
        FreeCAD.Console.PrintMessage("🤖 AI Assistant Workbench activated\n")
        
        # بازگرداندن قابلیت باز شدن خودکار پنل
        try:
            from freecad_ai.ui.panel import ensure_dock_created
            dock = ensure_dock_created()
            if dock:
                dock.show()
                FreeCAD.Console.PrintMessage("✅ AI Panel opened\n")
        except Exception as e:
            FreeCAD.Console.PrintError(f"❌ Dock error: {e}\n")

    def Deactivated(self):
        """Called when workbench is deactivated"""
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"

# Register workbench
Gui.addWorkbench(AIAssistantWorkbench())
FreeCAD.Console.PrintMessage("✅ AI Assistant Workbench registered\n")