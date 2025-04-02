app_name = "villa_management"
app_title = "Villa Management"
app_publisher = "soorya"
app_description = "Villa Management"
app_email = "soorya@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "villa_management",
# 		"logo": "/assets/villa_management/logo.png",
# 		"title": "Villa Management",
# 		"route": "/villa_management",
# 		"has_permission": "villa_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/villa_management/css/villa_management.css"
# app_include_js = "/assets/villa_management/js/villa_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/villa_management/css/villa_management.css"
# web_include_js = "/assets/villa_management/js/villa_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "villa_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "villa_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "index"
# role_home_page = {
#     "Resident": "/dashboard"
# }


# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "villa_management.utils.jinja_methods",
# 	"filters": "villa_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "villa_management.install.before_install"
# after_install = "villa_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "villa_management.uninstall.before_uninstall"
# after_uninstall = "villa_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "villa_management.utils.before_app_install"
# after_app_install = "villa_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "villa_management.utils.before_app_uninstall"
# after_app_uninstall = "villa_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "villa_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"villa_management.tasks.all"
# 	],
# 	"daily": [
# 		"villa_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"villa_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"villa_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"villa_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "villa_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "villa_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "villa_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["villa_management.utils.before_request"]
# after_request = ["villa_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["villa_management.utils.before_job"]
# after_job = ["villa_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"villa_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
 
# custom_app/hooks.py
signup_form_template="villa_management/templates/signup.html"
website_routes = [
    {"from_route": "/dashboard", "to_route": "villa_management.dashboard"}
]

# doc_events = {
#     "User": {
#         "after_insert": "villa_management.user.create_employee"
#     }
# }


# doc_events = {
#     "Notifications": {
#         "after_insert": "villa_management.notification.send_notification"
#     }
# }
# socketio_port = 9000


# csrf = {
#     "enabled": True
# }

# hooks.py in your custom app
# on_session_creation = "villa_management.custom_app.on_session_creation"



# boot_session = "villa_management.custom_app.route_user"


# # Override ERPNext's login behavior to redirect Residents
on_login = "villa_management.custom_app.on_login"
app_include_css = "/assets/villa_management/public/favicon.ico"
