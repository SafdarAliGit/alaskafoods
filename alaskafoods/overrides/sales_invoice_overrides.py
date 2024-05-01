from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from frappe.utils import add_days, today


class SalesInvoiceOverrides(SalesInvoice):
    def before_save(self):
        self.set_posting_time = 1
        self.set("posting_date", add_days(today(), 1))
        self.save()
