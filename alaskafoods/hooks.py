app_name = "alaskafoods"
app_title = "alaskafoods"
app_publisher = "techrix"
app_description = "alaskafoods"
app_email = "safdar211@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/alaskafoods/css/alaskafoods.css"
# app_include_js = "/assets/alaskafoods/js/alaskafoods.js"

# include js, css files in header of web template
# web_include_css = "/assets/alaskafoods/css/alaskafoods.css"
# web_include_js = "/assets/alaskafoods/js/alaskafoods.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "alaskafoods/public/scss/website"

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
# app_include_icons = "alaskafoods/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

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
# 	"methods": "alaskafoods.utils.jinja_methods",
# 	"filters": "alaskafoods.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "alaskafoods.install.before_install"
# after_install = "alaskafoods.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "alaskafoods.uninstall.before_uninstall"
# after_uninstall = "alaskafoods.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "alaskafoods.utils.before_app_install"
# after_app_install = "alaskafoods.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "alaskafoods.utils.before_app_uninstall"
# after_app_uninstall = "alaskafoods.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "alaskafoods.notifications.get_notification_config"

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

doc_events = {
    "*": {
        "Sales Invoice": {
            "after_save": "alaskafoods.custom.sales_order_custom.after_save"
        }
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"alaskafoods.tasks.all"
# 	],
# 	"daily": [
# 		"alaskafoods.tasks.daily"
# 	],
# 	"hourly": [
# 		"alaskafoods.tasks.hourly"
# 	],
# 	"weekly": [
# 		"alaskafoods.tasks.weekly"
# 	],
# 	"monthly": [
# 		"alaskafoods.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "alaskafoods.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "alaskafoods.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "alaskafoods.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["alaskafoods.utils.before_request"]
# after_request = ["alaskafoods.utils.after_request"]

# Job Events
# ----------
# before_job = ["alaskafoods.utils.before_job"]
# after_job = ["alaskafoods.utils.after_job"]

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
# 	"alaskafoods.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
doc_events = {
    "Sales Invoice": {
        "after_insert": "alaskafoods.custom.sales_invoice_custom.after_insert"
    },
    "Sales Order": {
        "after_insert": "alaskafoods.custom.sales_order_custom.after_insert"
    },
    "Delivery Note": {
        "after_insert": "alaskafoods.custom.delivery_note_custom.after_insert"
    },
    "Payment Entry": {
        "after_insert": "alaskafoods.custom.payment_entry_custom.after_insert"
    }
}

# override_doctype_class = {
#     "Sales Invoice": "alaskafoods.overrides.sales_invoice_overrides.SalesInvoiceOverrides",
#     "Delivery Note": "alaskafoods.overrides.delivery_note_overrides.DeliveryNoteOverrides",
# }

required_apps = [
    'erpnext'
]
