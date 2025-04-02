



import frappe
from frappe import _

# def get_context(context):
#     context.no_cache = 1
#     try:
#         user_email = frappe.session.user

#         if user_email == "Guest":
#             frappe.throw("You must be logged in to view this page.")

#         # Fetch the resident's record
#         resident = frappe.get_all("Residents Details", 
#                                   filters={"email": user_email}, 
#                                   fields=["full_name", "date_of_birth", "gender", "place", "contact_number", "job_profile"])
#         print(resident)
#         if resident:
#             context.resident = resident[0]
#             # Fetch all family members for the resident
#             family_members = frappe.get_all("Family Members", 
#                                            filters={"parent": resident[0].name}, 
#                                            fields=["family_full_name", "age", "gender", "occupation", "relation"])
#             context.resident["family_members"] = []
#             for member in family_members:
#                 context.resident["family_members"].append({
#                     "family_full_name": member.family_full_name,
#                     "age": member.age,
#                     "gender": member.gender,
#                     "occupation": member.occupation,
#                     "relation": member.relation
#                 })
#             print(family_members)
        
#         else:
#             context.resident = {}

#     except Exception as e:
#         frappe.logger().error(f"Error in get_context: {frappe.get_traceback()}")
#         frappe.throw("An error occurred while fetching data. Please try again.")


def get_context(context):
    context.no_cache = 1
    try:
        user_email = frappe.session.user

        if user_email == "Guest":
            frappe.throw("You must be logged in to view this page.")

        # Fetch the resident's record
        resident = frappe.get_all("Residents Details", 
                                filters={"email": user_email}, 
                                fields=["name", "full_name", "date_of_birth", "gender", 
                                       "place", "contact_number", "job_profile"])
        
        if resident:
            context.resident = resident[0]
            
            # Fetch family members from the child table of Residents Details
            context.resident["family_members"] = frappe.get_all("Family Members",
                                                              filters={"parent": resident[0].name, 
                                                                      "parenttype": "Residents Details"},
                                                              fields=["family_full_name", "age", 
                                                                      "gender", "occupation", "relation"])
            
            # Alternative method using get_doc if the above doesn't work
            # resident_doc = frappe.get_doc("Residents Details", resident[0].name)
            # context.resident["family_members"] = [{
            #     "family_full_name": m.family_full_name,
            #     "age": m.age,
            #     "gender": m.gender,
            #     "occupation": m.occupation,
            #     "relation": m.relation
            # } for m in resident_doc.family_members]
            
        else:
            context.resident = {}

    except Exception as e:
        frappe.logger().error(f"Error in get_context: {frappe.get_traceback()}")
        frappe.throw("An error occurred while fetching data. Please try again.")

def get_maintenance_requests():
    # Query the maintenance requests from the database
    return frappe.get_all('Maintanence', fields=['name', 'service_type', 'submitted_at'])