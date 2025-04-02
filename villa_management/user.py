import frappe

def create_employee_for_user(doc, method):
    # Ensure an employee is not already created for the user
    if not frappe.db.exists("Employee", {"custom_email_id": doc.email}):
        employee = frappe.get_doc({
            "doctype": "Employee",
            "full_name": f"{doc.first_name} {doc.last_name}" if doc.last_name else doc.first_name,
            "gender": doc.gender,  # Modify if gender data is available
            "date_of_birth": doc.birth_date,
            "contact_number": doc.phone,
            "custom_email_id": doc.email,
            "status": "Active",
            "company": frappe.defaults.get_global_default("company")  # Assign a default company
        })
        employee.insert(ignore_permissions=True)
        frappe.db.commit()
