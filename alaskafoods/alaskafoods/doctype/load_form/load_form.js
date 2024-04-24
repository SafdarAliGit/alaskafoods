// Copyright (c) 2024, techrix and contributors
// For license information, please see license.txt

frappe.ui.form.on("Load Form", {
    refresh(frm) {

    },
    sales_person: function (frm) {
        var sales_person = frm.doc.sales_person;
        var delivery_date = frm.doc.delivery_date;
        fill_load_form(frm, sales_person, delivery_date);

    },
});

function fill_load_form(frm, sales_person, delivery_date) {
    if (sales_person && delivery_date) {
        // Clear existing data before adding new entries
        frm.clear_table("load_form_items");
        frm.clear_table("load_form_invoices");

        frappe.call({
            method: "alaskafoods.alaskafoods.utils.fill_load_form.fill_load_form",
            args: {
                sales_person: sales_person,
                delivery_date: delivery_date
            },
            callback: function (response) {
                if (response.message.load_form_item_data) {
                    response.message.load_form_item_data.forEach(function (i) {
                        let entry = frm.add_child("load_form_items");
                            entry.item_code = i.item_code,
                            entry.item_name = i.item_name,
                            entry.issued_units = i.issued_units,
                            entry.free_units = i.free_units,
                            entry.total_units = i.total_units,
                            entry.carton = i.carton,
                            entry.units = i.units,
                            entry.pack_size = i.conversion_factor

                    });
                }
                frm.refresh_field('load_form_items');

                if (response.message.load_form_invoices_data) {
                    response.message.load_form_invoices_data.forEach(function (i) {
                        let entry = frm.add_child("load_form_invoices");
                            entry.invoice_no = i.invoice_no,
                            entry.customer = i.customer,
                            entry.status = i.status,
                            entry.issued_units = i.issued_units,
                            entry.free_units = i.free_units,
                            entry.total_units = i.total_units,
                            entry.amount = i.amount
                    });
                }
                frm.refresh_field('load_form_invoices');
            }
        });
    }
}
