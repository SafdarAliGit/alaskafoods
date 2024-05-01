import frappe
from frappe.utils import add_days, today


def after_insert(doc, method):
    try:
        # Submit the Sales Order after update
        spo = doc.append("sales_team", {})
        spo.sales_person = doc.custom_sales_person
        spo.allocated_percentage = 100

        doc.submit()
        # ------Delivery Note--------
        so = frappe.get_doc("Sales Order", doc.name)
        dn = frappe.new_doc("Delivery Note")
        dn.custom_sales_person = so.custom_sales_person
        dn.set_posting_time = 1
        dn.posting_date = so.delivery_date
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
        for si_sp in so.sales_team:
            spd = dn.append("sales_team", {})
            spd.sales_person = si_sp.sales_person
            spd.allocated_percentage = si_sp.allocated_percentage
            spd.allocated_amount = si_sp.allocated_amount
        dn.submit()
        # ------Sales Invoice--------

        si = frappe.new_doc("Sales Invoice")
        si.custom_sales_person = so.custom_sales_person
        si.set_posting_time = 1
        si.posting_date = so.delivery_date
        si.customer = so.customer
        si.custom_so = so.name
        si.set_warehouse = so.set_warehouse
        si.order_type = so.order_type
        si.update_stock = 1

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
        for si_sp in so.sales_team:
            sps = si.append("sales_team", {})
            sps.sales_person = si_sp.sales_person
            sps.allocated_percentage = si_sp.allocated_percentage
            sps.allocated_amount = si_sp.allocated_amount
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
