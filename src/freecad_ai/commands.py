"""
FreeCAD AI Assistant - Commands
تعریف و ثبت دستورات FreeCAD برای toolbar و menu
"""
import FreeCAD
import FreeCADGui as Gui


class AI_Chat:
    """
    دستور باز کردن پنل چت AI
    """
    
    def GetResources(self):
        """
        دریافت منابع دستور (آیکون، متن، tooltip)
        """
        return {
            'Pixmap': 'PartDesign_Body',  # آیکون موقت
            'MenuText': 'AI Chat',
            'ToolTip': 'Open AI Chat Panel'
        }
    
    def IsActive(self):
        """
        آیا دستور فعال است؟
        """
        return True
    
    def Activated(self):
        """
        وقتی دستور اجرا می‌شود
        """
        FreeCAD.Console.PrintMessage("🤖 Opening AI Chat panel...\n")
        try:
            from freecad_ai.ui.panel import ensure_dock_created
            dock = ensure_dock_created()
            if dock:
                dock.show()
                FreeCAD.Console.PrintMessage("✅ AI Chat panel opened\n")
        except Exception as e:
            FreeCAD.Console.PrintError(f"❌ Failed to open AI Chat: {e}\n")


class AI_Settings:
    """
    دستور باز کردن تنظیمات AI
    """
    
    def GetResources(self):
        """
        دریافت منابع دستور
        """
        return {
            'Pixmap': 'Preferences',
            'MenuText': 'AI Settings',
            'ToolTip': 'Open AI Settings'
        }
    
    def IsActive(self):
        """
        آیا دستور فعال است؟
        """
        return True
    
    def Activated(self):
        """
        وقتی دستور اجرا می‌شود
        """
        FreeCAD.Console.PrintMessage("⚙️ Opening AI Settings...\n")
        # TODO: پیاده‌سازی dialog تنظیمات
        FreeCAD.Console.PrintMessage("✅ AI Settings opened (placeholder)\n")


# ثبت دستورات در FreeCAD
Gui.addCommand('AI_Chat', AI_Chat())
Gui.addCommand('AI_Settings', AI_Settings())

FreeCAD.Console.PrintMessage("✅ AI Assistant commands registered\n")
