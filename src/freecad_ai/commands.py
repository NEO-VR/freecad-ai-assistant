"""
FreeCAD AI Assistant - Commands
"""
import FreeCAD
import FreeCADGui as Gui


class AI_Chat:
    """دستور باز کردن پنل چت AI"""
    
    def GetResources(self):
        return {
            'Pixmap': 'Std_OnlineHelp',  # آیکون استاندارد راهنما
            'MenuText': 'AI Chat',
            'ToolTip': 'Open AI Chat Panel'
        }
    
    def IsActive(self):
        return True
    
    def Activated(self):
        FreeCAD.Console.PrintMessage("🤖 AI Chat activated\n")
        try:
            from freecad_ai.ui.panel import ensure_dock_created
            dock = ensure_dock_created()
            if dock:
                dock.show()
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error: {e}\n")


class AI_Settings:
    """دستور باز کردن تنظیمات AI"""
    
    def GetResources(self):
        return {
            'Pixmap': 'Std_DlgPreferences',  # آیکون استاندارد تنظیمات
            'MenuText': 'AI Settings',
            'ToolTip': 'Open AI Settings'
        }
    
    def IsActive(self):
        return True
    
    def Activated(self):
        FreeCAD.Console.PrintMessage("⚙️ AI Settings activated\n")


# ثبت دستورات در FreeCAD
Gui.addCommand('AI_Chat', AI_Chat())
Gui.addCommand('AI_Settings', AI_Settings())

FreeCAD.Console.PrintMessage("✅ AI Assistant commands registered\n")