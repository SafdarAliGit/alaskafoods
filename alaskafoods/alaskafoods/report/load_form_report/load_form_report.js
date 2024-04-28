// Copyright (c) 2024, techrix and contributors
// For license information, please see license.txt

frappe.query_reports["Load Form Report"] = {
	"filters": [
		{
			"fieldname": "sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person",
			reqd: 1

		},
		{
			"fieldname": "delivery_date",
			"label": __("Delivery Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.nowdate(),
			reqd: 1
		}

	]
};
