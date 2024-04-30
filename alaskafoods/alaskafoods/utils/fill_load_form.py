import frappe


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


@frappe.whitelist()
def fill_load_form(**args):
    sales_invoice_items_totals = {"item_code": "", "item_name": "Total", "issued_units": 0, "carton": 0,
                                  "free_units": 0, "total_units": 0, "conversion_factor": 0, "pack_size": 0, "units": 0}
    sales_invoices_totals = {"invoice_no": "", "customer": "", "status": "Total", "issued_units": 0, "free_units": 0,
                             "total_units": 0, "amount": 0}
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
        0 AS units,
        IFNULL(SUM(ABS(ret_si_item.qty)), 0) AS returned

    FROM
        `tabSales Invoice` AS si
    INNER JOIN 
        `tabSales Invoice Item` AS sii ON si.name = sii.parent
    LEFT JOIN
        `tabSales Invoice Item` AS ret_si_item ON si.name = ret_si_item.parent AND si.is_return = 1
    LEFT JOIN
        `tabSales Invoice` AS ret_si ON ret_si_item.parent = ret_si.name AND ret_si.return_against = si.name 
    WHERE
        si.docstatus = 1 AND
        si.custom_sales_person = %s AND 
        si.posting_date = %s
    GROUP BY
        sii.item_code,sii.conversion_factor,sii.item_name
    """
    load_form_item_data = frappe.db.sql(sales_invoice_items, (sales_person, delivery_date,), as_dict=True)

    sales_invoices = """
        SELECT
            si.name AS invoice_no,
            si.customer,
            si.status,
            SUM(CASE WHEN sii.qty > 0 AND sii.uom = 'Carton' THEN sii.qty*sii.conversion_factor ELSE sii.qty END) AS issued_units,
            SUM(CASE WHEN sii.qty < 0 THEN ABS(sii.qty) ELSE 0 END) AS free_units,
            ((SUM(CASE WHEN sii.qty > 0 AND sii.uom = 'Carton' THEN sii.qty*sii.conversion_factor ELSE sii.qty END)) + SUM(CASE WHEN sii.qty < 0 THEN ABS(sii.qty) ELSE 0 END)) AS total_units,
            si.grand_total AS amount,
            IFNULL(SUM(ABS(ret_si_item.qty)), 0) AS returned
        FROM
            `tabSales Invoice` AS si
        INNER JOIN 
            `tabSales Invoice Item` AS sii ON si.name = sii.parent
        LEFT JOIN
            `tabSales Invoice Item` AS ret_si_item ON si.name = ret_si_item.parent AND si.is_return = 1
        LEFT JOIN
            `tabSales Invoice` AS ret_si ON ret_si_item.parent = ret_si.name AND ret_si.return_against = si.name 
        WHERE
            si.docstatus = 1 AND
            si.custom_sales_person = %s AND 
            si.posting_date = %s
        GROUP BY
            si.name
        """
    load_form_invoices_data = frappe.db.sql(sales_invoices, (sales_person, delivery_date,), as_dict=True)
    # CONVERSION FROM PCS TO CARTON
    for i in load_form_item_data:
        if i['uom'] == 'Pcs':
            i['carton'] = pcs_to_carton(i['total_units'], i['item_code']).get('carton')
            i['units'] = pcs_to_carton(i['total_units'], i['item_code']).get('units')

    # TOTALS
    sum_issued_units = 0
    sum_carton = 0
    sum_free_units = 0
    sum_total_units = 0
    sum_units = 0
    for item in load_form_item_data:
        sum_issued_units += item['issued_units'] if item['issued_units'] else 0
        sum_carton += item['carton'] if item['carton'] else 0
        sum_free_units += item['free_units'] if item['free_units'] else 0
        sum_total_units += item['total_units'] if item['total_units'] else 0
        sum_units += item['units'] if item['units'] else 0

    sales_invoice_items_totals['issued_units'] = sum_issued_units
    sales_invoice_items_totals['carton'] = sum_carton
    sales_invoice_items_totals['free_units'] = sum_free_units
    sales_invoice_items_totals['total_units'] = sum_total_units
    sales_invoice_items_totals['units'] = sum_units

    sum_issued_units = 0
    sum_free_units = 0
    sum_total_units = 0
    sum_amount = 0
    for item in load_form_invoices_data:
        sum_issued_units += item['issued_units'] if item['issued_units'] else 0
        sum_free_units += item['free_units'] if item['free_units'] else 0
        sum_total_units += item['total_units'] if item['total_units'] else 0
        sum_amount += item['amount'] if item['amount'] else 0

    sales_invoices_totals['issued_units'] = sum_issued_units
    sales_invoices_totals['free_units'] = sum_free_units
    sales_invoices_totals['total_units'] = sum_total_units
    sales_invoices_totals['amount'] = sum_amount

    # TOTALS END

    return {
        "load_form_item_data": load_form_item_data + [sales_invoice_items_totals],
        "load_form_invoices_data": load_form_invoices_data + [sales_invoices_totals]
    }
