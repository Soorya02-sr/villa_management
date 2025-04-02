import frappe


def get_context(context):
    context.no_cache = 1
    if frappe.session.user != 'Guest' and frappe.session.user != 'Administrator':
        frappe.local.flags.redirect_location = "/dashboard"
        raise frappe.Redirect
    elif frappe.session.user == 'Administrator':
        frappe.local.flags.redirect_location = "/app"
        raise frappe.Redirect


