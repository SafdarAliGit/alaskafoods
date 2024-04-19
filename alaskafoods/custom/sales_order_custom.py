import frappe


def after_insert(doc, method):
    try:
        # Submit the Sales Order
        doc.submit()
        # ------Delivery Note--------
        so = frappe.get_doc("Sales Order", doc.name)
        dn = frappe.new_doc("Delivery Note")
        dn.custom_sales_person = so.custom_sales_person
        dn.posting_date = so.transaction_date
        dn.customer = so.customer
        dn.custom_so = so.name
        dn.set_warehouse = so.set_warehouse

        for items in so.items:
            it = dn.append("items", {})
            it.against_sales_order = so.name
            it.item_code = items.item_code
            it.item_name = items.item_name
            it.qty = items.qty
            it.rate = items.rate
            it.amount = items.amount
            it.so_detail = items.name
            it.uom = items.uom
        dn.submit()
        # ------Sales Invoice--------

        si = frappe.new_doc("Sales Invoice")
        si.custom_sales_person = so.custom_sales_person
        si.posting_date = so.transaction_date
        si.customer = so.customer
        si.custom_so = so.name
        si.set_warehouse = so.set_warehouse
        si.order_type = so.order_type

        for items in so.items:
            it = si.append("items", {})
            it.sales_order = so.name
            it.item_code = items.item_code
            it.item_name = items.item_name
            it.qty = items.qty
            it.rate = items.rate
            it.amount = items.amount
            it.so_detail = items.name
            it.uom = items.uom
        si.submit()

    except Exception as e:
        frappe.throw(f"An error occurred: {e}")

# def on_update(doc, method):
#     try:
#         # ------Sales Invoice--------
#         so = frappe.get_doc("Sales Order", doc.name)
#         si = frappe.db.get_value("Sales Invoice", {"custom_so": doc.name}, "name")
#         si_obj = frappe.get_doc("Sales Invoice", si)
#         si_obj.custom_sales_person = so.custom_sales_person
#         si_obj.posting_date = so.transaction_date
#         si_obj.customer = so.customer
#         si_obj.custom_so = so.name
#         si_obj.set_warehouse = so.set_warehouse
#         si_obj.order_type = so.order_type
#
#         for items in so.items:
#             it = si_obj.append("items", {})
#             it.sales_order = so.name
#             it.item_code = items.item_code
#             it.item_name = items.item_name
#             it.qty = items.qty
#             it.rate = items.rate
#             it.amount = items.amount
#         si_obj.save()
#         # ------Delivery Note--------
#         so = frappe.get_doc("Sales Order", doc.name)
#         dn = frappe.db.get_value("Delivery Note", {"custom_so": doc.name}, "name")
#         dn_obj = frappe.get_doc("Delivery Note", dn)
#         dn_obj.custom_sales_person = so.custom_sales_person
#         dn_obj.posting_date = so.transaction_date
#         dn_obj.customer = so.customer
#         dn_obj.custom_so = so.name
#         dn_obj.set_warehouse = so.set_warehouse
#
#         for items in so.items:
#             it = dn_obj.append("items", {})
#             it.against_sales_order = so.name
#             it.item_code = items.item_code
#             it.item_name = items.item_name
#             it.qty = items.qty
#             it.rate = items.rate
#             it.amount = items.amount
#         dn_obj.save()
#
#     except Exception as e:
#         frappe.throw(e)
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
