import frappe
from frappe.utils import add_days, today


def after_insert(doc, method):
    dn = frappe.get_doc("Delivery Note", doc.name)
    dn.submit()
    doc.reload()


