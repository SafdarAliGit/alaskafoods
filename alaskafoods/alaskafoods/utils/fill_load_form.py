import frappe


@frappe.whitelist()
def fill_load_form(**args):
    sales_person = args.get('sales_person')
    delivery_date = args.get('delivery_date')

    sales_invoice_items = """
    SELECT
        sii.item_code,
        sii.item_name,
        sii.uom,
        SUM(CASE WHEN sii.qty > 0 AND sii.uom = 'Pcs' THEN sii.qty ELSE 0 END) AS issued_units,
        SUM(CASE WHEN sii.qty > 0 AND sii.uom = 'Carton' THEN sii.qty ELSE 0 END) AS carton,
        SUM(CASE WHEN sii.qty < 0 THEN ABS(sii.qty) ELSE 0 END) AS free_units,
        (SUM(CASE WHEN sii.qty > 0 AND sii.uom = 'Pcs' THEN sii.qty ELSE 0 END) + SUM(CASE WHEN sii.qty < 0 THEN ABS(sii.qty) ELSE 0 END)) AS total_units,
        sii.conversion_factor,
        CASE WHEN sii.conversion_factor = 0 THEN 1 ELSE sii.conversion_factor END AS pack_size,
        0 AS units
    FROM
        `tabSales Invoice` AS si
    INNER JOIN 
        `tabSales Invoice Item` AS sii ON si.name = sii.parent
    WHERE
        si.docstatus = 1 AND
        si.custom_sales_person = %s AND 
        DATE(si.posting_date) = %s
    GROUP BY
        sii.item_code,sii.conversion_factor,sii.item_name
    """
    load_form_item_data = frappe.db.sql(sales_invoice_items, (sales_person, delivery_date,), as_dict=True)
    for i in load_form_item_data:
        if i['uom'] == 'Pcs':
            i['carton'] = pcs_to_carton(i['total_units'], i['item_code']).get('carton')
            i['units'] = pcs_to_carton(i['total_units'], i['item_code']).get('units')

    return {
        "load_form_item_data": load_form_item_data
    }


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
