from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote
from frappe.utils import add_days, today


class DeliveryNoteOverrides(DeliveryNote):
    def before_save(self):
        self.set_posting_time = 1
        self.set("posting_date", add_days(today(), 1))
        self.save()
