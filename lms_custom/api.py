import frappe

@frappe.whitelist()
def get_my_training_courses():
    user = frappe.session.user
    roles = frappe.get_roles(user)
    
    if "Administrator" in roles or "System Manager" in roles:
        return frappe.get_all("Training Course", fields=["*"], order_by="creation desc")
        
    # We will build a list of course names the user has access to
    accessible_courses = set()
    
    # 1. Check if user is the Lecturer (teacher_email)
    teacher_matches = frappe.get_all("Training Course", 
        filters={"teacher_email": user},
        fields=["name"]
    )
    for d in teacher_matches:
        accessible_courses.add(d.name)
        
    # 2. Check if user is a Student in the child table
    # We try different possible child table names based on common conventions
    possible_tables = ["Training Course Student", "Training Course Student Email", "Training Course Session"]
    for table in possible_tables:
        try:
            # We look for any child table where the user's email exists
            # This is a bit generic but helpful since we don't have the site's metadata
            matches = frappe.db.get_all(table, 
                filters={"student_email": user}, 
                fields=["parent"]
            )
            for m in matches:
                accessible_courses.add(m.parent)
        except Exception:
            continue
            
    if not accessible_courses:
        return []
        
    return frappe.get_all("Training Course", 
        filters={"name": ["in", list(accessible_courses)]},
        fields=["*"],
        order_by="creation desc"
    )

@frappe.whitelist()
def get_course_details(route_or_name):
    if frappe.db.exists("Training Course", route_or_name):
        return frappe.get_doc("Training Course", route_or_name).as_dict()
    
    doc_name = frappe.db.get_value("Training Course", {"route": route_or_name}, "name")
    if doc_name:
        return frappe.get_doc("Training Course", doc_name).as_dict()
        
    frappe.throw(f"Training Course {route_or_name} not found", frappe.DoesNotExistError)

