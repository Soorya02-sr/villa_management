

import frappe
from frappe.utils import escape_html
from frappe import _
from frappe.utils.password import update_password
from frappe.utils import nowdate

from frappe.utils import now


@frappe.whitelist(allow_guest=True)
def sign_up(full_name, email, contact_number, create_password, place, dob=None, gender=None):
    try:
        frappe.logger().info(f"incoming data:{full_name, email, contact_number, create_password, place, dob, gender}")
        
        # Create User
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": full_name,
            "phone": contact_number,
            "location": place,
            "gender": gender,
            "birth_date": dob,
            "new_password": create_password,
            "send_welcome_email": 0,
            "roles": [{
                "role": "Residents"
            }]
        })
        user.insert(ignore_permissions=True)
        frappe.db.commit()

        # Create Resident
        resident = frappe.get_doc({
            "doctype": "Residents Details",
            "full_name": full_name,
            "date_of_birth": dob,
            "gender": gender,
            "email": email,
            "contact_number": contact_number,
            "place": place,
            "custom_user": user.name  # Link Resident to User
        })
        resident.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Signup successful!",
            "redirect_url": "/login"
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Resident Signup Error")
        frappe.throw(f"An error occurred: {str(e)}")




# @frappe.whitelist(allow_guest=True)
# def sign_up(full_name, email, contact_number, create_password, proof, place, villa_number, community_type, dob=None, gender=None):
#     try:
#         frappe.logger().info(f"incoming data:{full_name, email, contact_number, create_password, proof, place, villa_number, community_type, dob, gender}")
#         # Create User
#         user = frappe.get_doc({
#             "doctype": "User",
#             "email": email,
#             "first_name": full_name,
#             "phone": contact_number,
#             "location":place,
#             "gender":gender,
#             "birth_date":dob,
#             "new_password": create_password,
#             "send_welcome_email": 0,
#             "roles": [{
#                 "role": "Residents"
#             }]
#         })
#         user.insert(ignore_permissions=True)
#         frappe.db.commit()

        

#         # Create Resident
#         if role:
#             resident = frappe.get_doc({
#                 "doctype": "Residents Details",
#                 "full_name": full_name,
#                 "date_of_birth": dob,
#                 "gender": gender,
#                 "email": email,
#                 "contact_number": contact_number,
#                 "proof": proof,
#                 "place": place,
#                 "villa_number": villa_number,
#                 "community_type": community_type,
#                 "custom_user": user.name  # Link Resident to User
#             })
#         resident.insert(ignore_permissions=True)


#         frappe.db.commit()

#         return {
#             "status": "success",
#             "message": "Signup successful!",
#             "redirect_url": "/login"
#         }
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Resident Signup Error")
#         frappe.throw(f"an error occurred:{str(e)}")


# @frappe.whitelist(allow_guest=True)
# def get_villa_numbers():
#     """
#     Fetch villa numbers from the Villa Details doctype.
#     """
#     try:
#         villa_numbers = frappe.get_all(
#             "Villa Details",
#             fields=["villa_no"],
#             filters={},
#             order_by="villa_no"
#         )
#         return [villa["villa_no"] for villa in villa_numbers]
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Failed to fetch villa numbers")
#         frappe.throw("Failed to fetch villa numbers. Please try again.")

def create_user_for_resident(doc, method):
    """
    Automatically create a user when a new resident is added.
    """
    if not frappe.db.exists("User", doc.email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": doc.email,
            "first_name": doc.full_name,
            "phone": doc.contact_number,
            "enabled": 1,
            "user_type": "Website User",
            "send_welcome_email": 1,
            "role_profile_name": "Resident"  # Ensure "Resident" role exists
        })
        user.flags.ignore_permissions = True
        user.insert(ignore_permissions=True)
        frappe.db.commit()




@frappe.whitelist(methods=['PATCH'])
def update_profile(full_name, date_of_birth, gender, place, contact_number, job_profile, family_members=None):
    try:
        # Get current user's email
        user_email = frappe.session.user
        
        # Get resident document by email
        resident = frappe.get_doc("Residents Details", {"email": user_email})
        
        # Update basic fields
        resident.full_name = full_name
        resident.date_of_birth = date_of_birth
        resident.gender = gender
        resident.place = place
        resident.contact_number = contact_number
        resident.job_profile = job_profile
        
        # Clear existing family members
        resident.set("family_members", [])
        
        # Add new family members if provided
        if family_members:
            if isinstance(family_members, str):
                family_members = json.loads(family_members)
                
            for member in family_members:
                resident.append("family_members", {
                    "family_full_name": member.get("family_full_name"),
                    "age": member.get("age"),
                    "gender": member.get("gender"),
                    "occupation": member.get("occupation"),
                    "relation": member.get("relation")
                })
        
        resident.save(ignore_permissions=True)
        frappe.db.commit()
        
        return {"status": "success", "message": "Profile updated successfully"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Profile Update Error")
        return {"status": "error", "message": str(e)}




@frappe.whitelist()
def on_session_creation(login_manager):
    user = login_manager.user
    print("\n\n\n\n user : ", user)
    # Redirect only for non-admin users
    if user != "Administrator":
        frappe.local.response["home_page"] = "/dashboard"
    # else:
    #     frappe.local.response["home_page"] = "/index"        

def route_user(bootinfo):
    print("\n\ngfgfgfhghgf")
    user = frappe.session.user
    # Redirect only for non-admin users
    if user != "Administrator":
        bootinfo.route_to = "/dashboard"
    else:
        bootinfo.route_to = "/app"
        # frappe.local.response["redirect_to"] = "/dashboard"

def on_login(login_manager):
    # Check if the logged-in user is the Administrator
    if frappe.session.user == "Administrator":
        # Redirect to the custom dashboard
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/app/dashboard-view/Admin"
        frappe.local.flags.redirect_location = frappe.local.response["location"]



@frappe.whitelist()
def create_maintenance_request(service_type, description, submitted_at):
    try:
        user = frappe.session.user
        resident = frappe.db.exists("Residents Details", {"custom_user":user})
        print("HERE", resident)
        maintenance_request = frappe.new_doc("Maintanence")
        maintenance_request.service_type=service_type
        maintenance_request.resident_name=resident
        maintenance_request.issue=description
        maintenance_request.submitted_at=frappe.utils.now()
        
        maintenance_request.insert(ignore_permissions=True)  
        frappe.db.commit()  

        print("Maintenance request created successfully")  # Debugging: Confirm success
        return {"status": "success", "message": "Maintenance request created successfully"}
    except Exception as e:
        frappe.log_error(f"Error occurred while creating maintenance request: {str(e)}", e)
        print("Error:", str(e))  # Debugging: Log the error
        return {"status": "error", "message": "An error occurred while creating the maintenance request."}





@frappe.whitelist(allow_guest=True)
def get_maintenance_requests():
    try:
        user = frappe.session.user  # Get the logged-in user

        # Fetch maintenance requests for the logged-in user
        maintenance_requests = frappe.get_all(
            'Maintanence', 
            filters={'owner': user}, 
            fields=['service_type', 'submitted_at', 'name', 'workflow_state']  # Include workflow_state
        )
        # Return the data with a success status
        return {'status': 'success', 'data': maintenance_requests}
    except Exception as e:
        # Log the error for debugging
        frappe.log_error(frappe.get_traceback(), 'Error in get_maintenance_requests')
        
        # Return a user-friendly error message
        return {'status': 'error', 'message': 'An error occurred while fetching maintenance requests. Please try again later.'}


@frappe.whitelist()
def create_complaint(description, submitted_at):
    try:
        # Fetch the current logged-in user
        user = frappe.session.user
        
        # Check if the user is associated with a resident in the "Residents Details" doctype
        resident = frappe.db.exists("Residents Details", {"custom_user": user})
        
        if not resident:
            frappe.throw(_("No resident found for the current user."))
        
        # Create a new "Complaint" document
        complaint = frappe.new_doc("Complaints")
        complaint.description = description
        complaint.resident = resident  # Link the complaint to the resident
        complaint.created_at = frappe.utils.now()  # Use Frappe's utility for current timestamp
        complaint.status = "Open"  # Set default status
        
        # Insert the document into the database
        complaint.insert(ignore_permissions=True)
        frappe.db.commit()  # Commit the transaction
        
        # Log success and return a response
        frappe.log(f"Complaint created successfully by user: {user}")
        return {
            "status": "success",
            "message": "Complaint submitted successfully!",
            "complaint_id": complaint.name
        }
    except Exception as e:
        # Log the error and return an error message
        frappe.log_error(f"Error occurred while creating complaint: {str(e)}", e)
        return {
            "status": "error",
            "message": "An error occurred while submitting the complaint. Please try again."
        }

@frappe.whitelist(allow_guest=True)  # Allow guest access if needed
def get_residents():
    try:
        # Fetch all residents from the Residents DocType
        residents = frappe.get_all(
            "Residents Details",
            fields=["name", "full_name", "villa_number", "proof"]
        )
        return {"status": "success", "data": residents}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_residents")
        return {"status": "error", "message": str(e)}








@frappe.whitelist()
def get_payments():
    try:
        user_email = frappe.session.user
        
        # Get resident linked to this user
        resident = frappe.get_all(
            "Residents Details",
            filters={"custom_user": user_email},
            fields=["name"],
            limit=1
        )
        
        if not resident:
            return {
                "status": "success",
                "data": [],
                "user": user_email,
                "message": "No resident profile found"
            }
            
        resident_name = resident[0].name
        
        # Get payments for this resident
        payments = frappe.get_all(
            "Payment",
            filters={"resident": resident_name},
            fields=["name", "type", "amount", "paid", "created"],
            order_by="creation desc"
        )
        
        # Format the data
        for payment in payments:
            if payment.get("created"):
                payment["created"] = frappe.utils.format_date(payment["created"])
        
        return {
            "status": "success",
            "data": payments,
            "user": user_email
        }
        
    except Exception as e:
        frappe.log_error(title="Payment Fetch Error", message=str(e))
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist()
def get_payment_details(payment_id):
    try:
        payment = frappe.get_doc("Payment", payment_id)
        
        return {
            "status": "success",
            "message": {
                "id": payment.name,
                "type": payment.type,
                "amount": payment.amount,
                "paid": payment.paid,
                "payment_mode": payment.payment_mode,
                "created": frappe.utils.format_datetime(payment.created),
            }
        }
    except Exception as e:
        frappe.log_error(title="Payment Details Error", message=str(e))
        return {
            "status": "error",
            "message": str(e)
        }



@frappe.whitelist()
def update_payment(**kwargs):
    try:
        # Get parameters
        payment_id = kwargs.get('payment_id') or frappe.form_dict.get('payment_id')
        payment_mode = kwargs.get('payment_mode') or frappe.form_dict.get('payment_mode')
        mark_as_paid = kwargs.get('mark_as_paid') or frappe.form_dict.get('mark_as_paid')

        if not all([payment_id, payment_mode]):
            frappe.throw("Missing required parameters")

        # Get payment document
        payment = frappe.get_doc("Payment", payment_id)
        
        # Get resident linked to current user
        resident = frappe.get_all(
            "Residents Details",
            filters={"custom_user": frappe.session.user},
            fields=["name"],
            limit=1
        )
        
        # Verify resident owns this payment
        if not resident or payment.resident != resident[0].name:
            frappe.throw("You don't have permission to update this payment", frappe.PermissionError)

        # Update fields
        payment.payment_mode = payment_mode
        if mark_as_paid:
            payment.paid = 1
        
        # Save changes
        payment.save(ignore_permissions=True)  # Bypass permission checks since we've manually verified
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Payment updated successfully",
            "payment_id": payment.name
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(title="Payment Update Failed", message=str(e))
        return {
            "status": "error",
            "message": str(e)
        }
@frappe.whitelist()
def create_event(event_name, event_type, event_date, event_time):
    try:
        # Validate required fields
        if not all([event_name, event_type, event_date, event_time]):
            frappe.throw("All fields (Event Name, Type, Date, Time) are required")

        # Validate event type
        valid_types = ["Seasonal Events", "Trips", "Special Events"]
        if event_type not in valid_types:
            frappe.throw(f"Invalid event type. Must be one of: {', '.join(valid_types)}")

        # Create new Event document
        event = frappe.get_doc({
            "doctype": "Events",
            "event_name": event_name,
            "type": event_type,  # This should match your doctype field
            "event_date": event_date,
            "event_time": event_time
        })
        
        event.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": "Event created successfully",
            "name": event.name
        }
        
    except Exception as e:
        frappe.log_error("Event Creation Failed", str(e))
        frappe.db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }












from frappe import whitelist
from frappe import get_all
from frappe import _

@whitelist(allow_guest=True)
def get_notifications():
    """Fetch all notifications to display in resident portal"""
    try:
        notifications = get_all(
            "Notifications",  # Changed to match your actual doctype name (lowercase)
            fields=["name", "type", "message", "created_at"],
            filters={
                "docstatus": 1  # Only submitted documents
            },
            order_by="creation desc",
            limit=50
        )

        return {
            "status": "success",
            "data": notifications
        }

    except Exception as e:
        from frappe import log_error
        log_error("Failed to fetch notifications")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def get_security_team():
    try:
        security_team = []
        
        # Get active security employees
        security_employees = frappe.get_all("Employee",
            filters={
                "status": "Active",
                "user_id": ["!=", ""]  # Ensure user_id is not empty
            },
            fields=["name", "first_name", "custom_contact_number", "user_id"]
        )
        
        frappe.logger().debug(f"Found {len(security_employees)} security employees")
        
        for employee in security_employees:
            # Check if user has "Security" role
            user_roles = frappe.get_roles(employee["user_id"])
            if "Security" not in user_roles:
                continue
                
            # Get active shift assignments using employee_name (not employee ID)
            shifts = frappe.get_all("Shift Assignment",
                filters={
                    "employee_name": employee["first_name"],  # Changed to employee_name
                    "status": "Active"
                },
                fields=["shift_type"],
                order_by="creation desc",
                limit=1
            )
            
            if shifts:
                security_team.append({
                    "employee_name": employee["first_name"],
                    "shift_type": shifts[0]["shift_type"],
                    "custom_contact_number": employee["custom_contact_number"],
                    "status": "Active"
                })
        
        return {
            "status": "success" if security_team else "empty",
            "data": security_team
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to fetch security team")
        return {
            "status": "error",
            "message": str(e)
        }


# payment.py
import frappe
from frappe.utils import getdate, get_first_day, get_last_day

@frappe.whitelist()
def check_existing_monthly_fund(resident, posting_date):
    posting_date = getdate(posting_date)
    first_day = get_first_day(posting_date)
    last_day = get_last_day(posting_date)
    
    existing = frappe.db.exists('Payment', {
        'type': 'Monthly Fund',
        'resident': resident,
        'posting_date': ['between', [first_day, last_day]],
        'docstatus': ['<', 2]  # 0=Draft, 1=Submitted
    })
    
    return bool(existing)