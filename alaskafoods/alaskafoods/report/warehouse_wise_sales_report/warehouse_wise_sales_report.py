from decimal import Decimal
import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def pcs_to_carton(qty=0, item_code=None):
    carton = 0
    units = 0
    if qty > 0 and item_code:
        conversion_factor = frappe.db.get_value("UOM Conversion Detail",
                                                {"parent": item_code, "uom": "Carton"},
                                                "conversion_factor") or 1
        carton = qty // conversion_factor
        units = int(qty % conversion_factor)
    return {"carton": carton, "units": units}


def group_data_by_sales_person(data):
    grouped_data = {}
    for entry in data:
        warehouse = entry['set_warehouse']
        if warehouse not in grouped_data:
            grouped_data[warehouse] = {
                'src_carton': 0,
                'src_qty': 0,
                'conv_carton': 0,
                'tot_carton': 0,
                'conv_qty': 0,
                'amount': 0,
                'unique_customers': 0,
                'invoices': 0,
                'drop_size': 0,
                'sku': 0
            }
        grouped_data[warehouse]['src_carton'] += entry['src_carton']
        grouped_data[warehouse]['src_qty'] += entry['src_qty']
        grouped_data[warehouse]['conv_carton'] += entry['conv_carton']
        grouped_data[warehouse]['tot_carton'] += entry['conv_carton'] + entry['src_carton']
        grouped_data[warehouse]['conv_qty'] += entry['conv_qty']
        grouped_data[warehouse]['amount'] += entry['amount']
        grouped_data[warehouse]['item_code'] = entry['item_code']
        grouped_data[warehouse]['unique_customers'] += entry['unique_customers']
        grouped_data[warehouse]['invoices'] += entry['invoices']
        grouped_data[warehouse]['drop_size'] += entry['drop_size']
        grouped_data[warehouse]['sku'] += entry['sku']
    return grouped_data


def get_columns():
    return [
        {"label": "<b>Warehouse</b>", "fieldname": "set_warehouse", "fieldtype": "Link", "options": "Sales Person",
         "width": 120},
        # {"label": "<b>Src. Carton</b>", "fieldname": "src_carton", "fieldtype": "Data", "width": 120},
        # {"label": "<b>Src. Qty</b>", "fieldname": "src_qty", "fieldtype": "Data", "width": 120},
        # {"label": "<b>Conv. Carton</b>", "fieldname": "conv_carton", "fieldtype": "Data", "width": 120},
        {"label": "<b>Tot. Carton</b>", "fieldname": "tot_carton", "fieldtype": "Data", "width": 120},
        {"label": "<b>Qty</b>", "fieldname": "conv_qty", "fieldtype": "Data", "width": 120},
        {"label": "<b> No. Of Customers</b>", "fieldname": "unique_customers", "fieldtype": "Data", "width": 120},
        {"label": "<b>No. of Invoices</b>", "fieldname": "invoices", "fieldtype": "Data", "width": 120},
        {"label": "<b>Drop Size</b>", "fieldname": "drop_size", "fieldtype": "Data", "width": 120},
        {"label": "<b>SKU Per Call</b>", "fieldname": "sku", "fieldtype": "Data", "width": 120},
        {"label": "<b>Amount</b>", "fieldname": "amount", "fieldtype": "Currency", "width": 120}
    ]


def get_conditions(filters):
    conditions = []
    if filters.get("from_date"):
        conditions.append("inv.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("inv.posting_date <= %(to_date)s")
    return " AND ".join(conditions)


def get_data(filters):
    sales_query = """
        SELECT 
            inv.set_warehouse,
            inv_item.item_code,
            SUM(CASE WHEN inv_item.uom='Carton' THEN inv_item.qty ELSE 0 END) AS src_carton,
            SUM(CASE WHEN inv_item.uom !='Carton' THEN inv_item.qty ELSE 0 END) AS src_qty,
            COUNT(DISTINCT inv.customer) AS unique_customers,
            COUNT(DISTINCT inv.name) AS invoices,
            ROUND(SUM(inv_item.amount)/COUNT(DISTINCT inv.name),2) AS drop_size,
            ROUND(COUNT(DISTINCT inv_item.item_code)/COUNT(DISTINCT inv.name),2) AS sku,
            SUM(inv_item.amount) AS amount  
        FROM 
            `tabSales Invoice` AS inv
        LEFT JOIN `tabSales Invoice Item` AS inv_item ON inv_item.parent = inv.name
        WHERE 
            inv.docstatus = 1 
            AND inv.is_return = 0
            AND {conditions}
        GROUP BY
            inv.set_warehouse
    """.format(conditions=get_conditions(filters))

    sales_result = frappe.db.sql(sales_query, filters, as_dict=True)

    data = []
    totals = {'set_warehouse': 'TOTAL', 'tot_carton': 0, 'conv_qty': 0, 'unique_customers': 0, 'invoices': 0,
              'drop_size': 0, 'sku': 0, 'amount': 0}
    for row in sales_result:
        row['conv_carton'], row['conv_qty'] = pcs_to_carton(row['src_qty'], row['item_code']).values()
        row['tot_carton'] = row['conv_carton'] + row['src_carton']
        data.append(row)

    grouped_data = group_data_by_sales_person(data)
    gd = [{'set_warehouse': k, **v} for k, v in grouped_data.items()]
    for i in gd:
        totals['tot_carton'] += i['tot_carton']
        totals['conv_qty'] += i['conv_qty']
        totals['unique_customers'] += i['unique_customers']
        totals['invoices'] += i['invoices']
        totals['drop_size'] += i['drop_size']
        totals['sku'] += i['sku']
        totals['amount'] += i['amount']
    totals['drop_size'] = round(totals['drop_size'] / len(gd), 2)
    totals['sku'] = round(totals['sku'] / len(gd), 2)
    # make bolder
    keys = list(totals.keys())
    for k in keys[1:-1]:
        totals[k] = f"<b>{totals[k]}</b>"
    gd.append(totals)

    return gd
