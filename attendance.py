import frappe

def create_employee(doc, method):
    """Automatically creates an Employee when a User is created."""

    # Check if Employee already exists
    if frappe.db.exists("Employee", {"user_id": doc.name}):
        return  # Employee already exists, so exit

    # Fetch Date of Birth from User (if it exists)
    date_of_birth = doc.get("date_of_birth") or None
    contact_number=doc.get("phone") of None

    # If no date_of_birth is available, set a default or handle the missing value
    if not date_of_birth:
        frappe.msgprint("⚠️ Warning: Date of Birth is missing. Please update it manually.", alert=True)

    # Create Employee record
    employee = frappe.get_doc({
        "doctype": "Employee",
        "first_name": f"{doc.first_name} {doc.last_name}" if doc.last_name else doc.first_name,
        "user_id": doc.name,  # Link User to Employee
        "custom_email_id": doc.email,
        "contact_number":doc.phone,
        "status": "Active",  # Default status
        "date_of_birth": date_of_birth,  # Ensure DOB is filled
        "gender": doc.get("gender") or "Other",  # Default gender if missing
        "date_of_joining": frappe.utils.today()  # Set joining date as today
    })

    employee.insert(ignore_permissions=True)
    
    frappe.msgprint(f"✅ Employee record created for {doc.first_name}")
