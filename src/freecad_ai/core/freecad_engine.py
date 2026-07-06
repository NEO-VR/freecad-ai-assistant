"""
FreeCAD AI Assistant - FreeCAD Engine Core
این ماژول مسئول ترجمه دستورات طبیعی به عملیات واقعی CAD در FreeCAD است.
شامل ساخت Body, Sketch, Constraint و Featureها.
"""

import FreeCAD
import FreeCADGui as Gui
import Part
from PartGeom import Point, Line, Circle
import math

def get_active_document():
    """دریافت سند فعال یا ساخت سند جدید"""
    doc = FreeCAD.ActiveDocument
    if not doc:
        doc = FreeCAD.newDocument("AI_Design")
        FreeCAD.ActiveDocument = doc
    return doc

def create_body(name="Body"):
    """
    ساخت یک بدنه جدید (PartDesign Body) در FreeCAD 1.1+
    """
    doc = get_active_document()
    
    # در FreeCAD 1.1 از PartDesign Workbench استفاده می‌کنیم
    try:
        # تلاش برای ساخت Body استاندارد
        body = doc.addObject("PartDesign::Body", name)
        doc.recompute()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(body)
        return {"success": True, "object": body, "name": body.Label}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_sketch_on_xy(body, name="Sketch"):
    """
    ساخت یک اسکچ روی صفحه XY بدنهِ داده شده
    """
    if not body:
        return {"success": False, "error": "No active body"}
    
    doc = body.Document
    try:
        sketch = doc.addObject("Sketcher::SketchObject", name)
        body.addObject(sketch)
        
        # تنظیم صفحه نقشه‌کشی روی XY (0,0,1)
        sketch.MapMode = "FlatFace"
        sketch.Support = [(body.Origin.OriginFeatures[0], "")] # XY Plane
        
        doc.recompute()
        return {"success": True, "object": sketch}
    except Exception as e:
        return {"success": False, "error": str(e)}

def add_rectangle_to_sketch(sketch, width=10, height=10, center_x=0, center_y=0):
    """
    افزودن یک مستطیل به اسکچ با قیدهای ابعادی
    """
    try:
        doc = sketch.Document
        half_w = width / 2.0
        half_h = height / 2.0
        
        # تعریف ۴ نقطه گوشه
        p1 = Point(-half_w + center_x, -half_h + center_y, 0)
        p2 = Point(half_w + center_x, -half_h + center_y, 0)
        p3 = Point(half_w + center_x, half_h + center_y, 0)
        p4 = Point(-half_w + center_x, half_h + center_y, 0)
        
        # ایجاد خطوط
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p1)
        
        geo_list = [l1, l2, l3, l4]
        geo_indices = []
        for g in geo_list:
            idx = sketch.addGeometry(g)
            geo_indices.append(idx)
        
        # بستن حلقه (Constraint Coincident)
        # نقطه پایان خط ۱ به شروع خط ۲
        sketch.addConstraint(PartGeom.Constraint(geo_indices[0], 2, geo_indices[1], 1, PartGeom.Point))
        # پایان ۲ به شروع ۳
        sketch.addConstraint(PartGeom.Constraint(geo_indices[1], 2, geo_indices[2], 1, PartGeom.Point))
        # پایان ۳ به شروع ۴
        sketch.addConstraint(PartGeom.Constraint(geo_indices[2], 2, geo_indices[3], 1, PartGeom.Point))
        # پایان ۴ به شروع ۱
        sketch.addConstraint(PartGeom.Constraint(geo_indices[3], 2, geo_indices[0], 1, PartGeom.Point))
        
        # قیدهای عمودی/افقی (برای اطمینان از مستطیل بودن)
        sketch.addConstraint(PartGeom.Constraint(geo_indices[0], PartGeom.Horizontal))
        sketch.addConstraint(PartGeom.Constraint(geo_indices[1], PartGeom.Vertical))
        
        # قیدهای ابعادی (Dimensional Constraints)
        # عرض (خط ۱)
        sketch.addConstraint(PartGeom.Constraint(geo_indices[0], PartGeom.Distance, width))
        # ارتفاع (خط ۲)
        sketch.addConstraint(PartGeom.Constraint(geo_indices[1], PartGeom.Distance, height))
        
        # قید تقارن نسبت به مبدا (اختیاری اما خوب برای مرکز بودن)
        # midpoint line 1 to origin x
        # midpoint line 2 to origin y
        # (برای سادگی فعلاً حذف شده، مستطیل در مختصات داده شده رسم می‌شود)
        
        doc.recompute()
        return {"success": True, "sketch": sketch}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def pad_sketch(sketch, length=10):
    """
    عملیات Pad (اکستروژن) روی اسکچ برای ساخت حجم سه بعدی
    """
    try:
        doc = sketch.Document
        body = sketch.Parent
        if not body:
            return {"success": False, "error": "Sketch has no parent body"}
            
        pad = doc.addObject("PartDesign::Pad", "Pad")
        body.addObject(pad)
        pad.Profile = sketch
        pad.Length = length
        pad.Type = 0 # Dimension type
        
        doc.recompute()
        return {"success": True, "feature": pad}
    except Exception as e:
        return {"success": False, "error": str(e)}

def execute_command(command_type, params):
    """
    تابع اصلی فراخوانی توسط AI
    command_type: 'create_box', 'create_cylinder', etc.
    params: دیکشنری پارامترها
    """
    if command_type == "create_box":
        width = params.get("width", 10)
        height = params.get("height", 10)
        length = params.get("length", 10) # طول اکستروژن
        
        res_body = create_body("Box_Body")
        if not res_body["success"]: return res_body
        
        body = res_body["object"]
        res_sketch = create_sketch_on_xy(body, "Box_Sketch")
        if not res_sketch["success"]: return res_sketch
        
        sketch = res_sketch["object"]
        res_rect = add_rectangle_to_sketch(sketch, width, height)
        if not res_rect["success"]: return res_rect
        
        res_pad = pad_sketch(sketch, length)
        if not res_pad["success"]: return res_pad
        
        return {
            "success": True, 
            "message": f"مکعب ساخته شد: {width}x{height}x{length}",
            "object_name": body.Label
        }

    elif command_type == "get_info":
        doc = get_active_document()
        count = len(doc.Objects)
        return {
            "success": True,
            "message": f"سند '{doc.Name}' دارای {count} شیء است."
        }
    
    else:
        return {"success": False, "error": f"دستور ناشناخته: {command_type}"}

# تست سریع اگر فایل مستقیم اجرا شود (فقط برای دیباگ خارج از FreeCAD)
if __name__ == "__main__":
    print("این ماژول فقط داخل محیط FreeCAD قابل اجراست.")
