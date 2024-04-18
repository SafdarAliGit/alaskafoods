import frappe


def after_insert(doc, method):
    try:
        if doc.docstatus == 0:
            # Submit the Sales Order
            doc.submit()
            # ------Sales Invoice--------
            so = frappe.get_doc("Sales Order", doc.name)
            si = frappe.new_doc("Sales Invoice")
            si.custom_sales_person = so.custom_sales_person
            si.posting_date = so.transaction_date
            si.customer = so.customer
            si.custom_so = so.name

            for items in so.items:
                it = si.append("items", {})
                it.sales_order = so.name
                it.item_code = items.item_code
                it.qty = items.qty
                it.rate = items.rate
                it.amount = items.amount
            si.submit()
            # ------Delivery Note--------
            so = frappe.get_doc("Sales Order", doc.name)
            dn = frappe.new_doc("Delivery Note")
            dn.custom_sales_person = so.custom_sales_person
            dn.posting_date = so.transaction_date
            dn.customer = so.customer
            dn.custom_so = so.name

            for items in so.items:
                it = dn.append("items", {})
                it.against_sales_order = so.name
                it.item_code = items.item_code
                it.qty = items.qty
                it.rate = items.rate
                it.amount = items.amount
            dn.submit()

    except Exception as e:
        frappe.throw(e)


# def on_cancel(doc, method):
#     try:
#         if doc.docstatus == 1:
#             doc.cancel()
#             # ------Sales Invoice--------
#             si = frappe.db.get_value("Sales Invoice", {"custom_so": doc.name}, "name")
#             si_obj = frappe.get_doc("Sales Invoice", si)
#             si_obj.cancel()
#             # ------Delivery Note--------
#             dn = frappe.db.get_value("Delivery Note", {"custom_so": doc.name}, "name")
#             dn_obj = frappe.get_doc("Delivery Note", dn)
#             dn_obj.cancel()
#     except Exception as e:
#         frappe.throw(e)


