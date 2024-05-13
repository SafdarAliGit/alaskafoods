// Copyright (c) 2024, Safdar Ali and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Person Wise Sales Report"] = {
    "filters": [
        {
            label: __("From Date"),
            fieldname: "from_date",
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 1
        },
        {
            label: __("To Date"),
            fieldname: "to_date",
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            label: __("Sales Person"),
            fieldname: "sales_person",
            fieldtype: "Link",
            options: "Sales Person"

        },
        {
            label: __("Warehouse"),
            fieldname: "warehouse",
            fieldtype: "Link",
            options: "Warehouse"
        }
    ]
};
