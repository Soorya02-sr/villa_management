# import frappe

# def send_notification(type, message, recipient_type, recipient_doctype, recipient, created_at, specific_user=None):
#     """
#     Send a notification to residents, security, both, or a specific user.
#     """

#     # Create a new notification entry
#     notification = frappe.get_doc({
#         "doctype": "Notifications",
#         "type":type,
#         "message": message,
#         "recipient_type": recipient_type,
#         "recipient_doctype": recipient_doctype if recipient_type == "Personalized" else None,
#         "recipient": specific_user if recipient_type == "Personalized" else None,
#           # Default as unread
#         "created_at": frappe.utils.nowdate()
#     })
#     notifications.insert(ignore_permissions=True)

#     # Determine recipients
#     recipients = []
    
#     if recipient_type == "Residents":
#         recipients = frappe.get_all("User", filters={"role": "Residents"}, pluck="name")
#     elif recipient_type == "Security":
#         recipients = frappe.get_all("User", filters={"role": "Security"}, pluck="name")
#     elif recipient_type == "All":
#         residents = frappe.get_all("User", filters={"role": "Residents"}, pluck="name")
#         security = frappe.get_all("User", filters={"role": "Security"}, pluck="name")
#         recipients = residents + security
#     elif recipient_type == "Personalized" and specific_user:
#         recipients = [specific_user]

#     # Send real-time notifications
#     for user in recipients:
#         frappe.publish_realtime(
#             event="notifications",
#             message={"text": message},
#             user=user
#         )

