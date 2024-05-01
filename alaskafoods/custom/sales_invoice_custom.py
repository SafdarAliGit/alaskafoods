import frappe
from frappe.utils import add_days, today


def after_insert(doc, method):
    si = frappe.get_doc("Sales Invoice", doc.name)
    si.submit()
    doc.reload()
