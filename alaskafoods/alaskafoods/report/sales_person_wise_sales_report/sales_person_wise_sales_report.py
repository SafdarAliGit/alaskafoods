# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
from decimal import Decimal

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def pcs_to_carton(qty=0, item_code=None):
    carton = 0
    units = 0
    conversion_factor = frappe.db.get_value("UOM Conversion Detail",
                                            {"parent": item_code, "uom": "Carton"},
                                            "conversion_factor")
    if qty > 0 and item_code:
        carton = qty // conversion_factor
        result = qty / conversion_factor
        decimal_portion = result % 1
        units = int(decimal_portion * conversion_factor)
    return {
        "carton": carton,
        "units": units
    }


def group_data_by_sales_person(data):
    grouped_data = {}

    for entry in data:
        sales_person = entry['sales_person']
        if sales_person not in grouped_data:
            # Initialize the grouped data for the sales person
            grouped_data[sales_person] = {
                'carton': 0,
                'qty': 0,
                'amount': 0
            }

        # Sum up the carton, qty, and amount for the current sales person
        grouped_data[sales_person]['carton'] += entry['carton']
        grouped_data[sales_person]['qty'] += entry['qty']
        grouped_data[sales_person]['amount'] += entry['amount']

    return grouped_data


def get_columns():
    columns = [
        {
            "label": "<b>Sales Person</b>",
            "fieldname": "sales_person",
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 120
        },
        {
            "label": "<b>Item Code</b>",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 120
        },
        {
            "label": "<b>Carton</b>",
            "fieldname": "carton",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "<b>Qty</b>",
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "<b>Amount</b>",
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        }
    ]
    return columns


def get_conditions(filters):
    conditions = []
    if filters.get("from_date"):
        conditions.append(f"inv.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"inv.posting_date <= %(to_date)s")
    if filters.get("sales_person"):
        conditions.append(f"inv.custom_sales_person = %(sales_person)s")
    if filters.get("warehouse"):
        conditions.append(f"inv.set_warehouse = %(warehouse)s")
    return " AND ".join(conditions)


def get_data(filters):
    data = []

    sales_query = """
            SELECT 
                inv.custom_sales_person AS sales_person,
                inv_item.item_code AS item_code,
                'Carton' AS carton,
                SUM(inv_item.qty) AS qty,
                SUM(inv_item.amount) AS amount 
            FROM 
                `tabSales Invoice` AS inv
            LEFT JOIN `tabSales Invoice Item` AS inv_item ON inv_item.parent = inv.name
            WHERE 
                inv.docstatus = 1 
                AND {conditions}
            GROUP BY
                inv_item.item_code


    """.format(conditions=get_conditions(filters))

    sales_result = frappe.db.sql(sales_query, filters, as_dict=1)
    for i in sales_result:
        i['carton'] = pcs_to_carton(i['qty'], i['item_code']).get('carton')

    grouped_data = group_data_by_sales_person(sales_result)

    grouped_data_list = [{'sales_person': k, **v} for k, v in grouped_data.items()]
    data.extend(grouped_data_list)
    return data
