import frappe


def after_insert(doc, method):
    si = frappe.get_doc("Sales Invoice", doc.name)
    si.submit()
    doc.reload()








