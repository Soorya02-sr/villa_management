import frappe
from frappe import _

def get_context(context):
    if not frappe.session.user or frappe.session.user == "Guest":
        # frappe.local.response["redirect_to"] = "/index.html"
        frappe.throw(_("You are not permitted to access this page."), frappe.PermissionError)
    return context



def get_context(context):
    # Fetch resident details based on logged-in user
    user_email = frappe.session.user
    resident = frappe.get_all("Residents Details", 
                              filters={"email":user_email},
                              
                              fields=["full_name", "date_of_birth", "gender", "place", "contact_number"])

    # If resident data exists, pass the first entry to context
    context.resident = resident[0] if resident else {}


