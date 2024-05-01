import frappe


def after_insert(doc, method):
    dn = frappe.get_doc("Delivery Note", doc.name)
    dn.submit()
    doc.reload()
