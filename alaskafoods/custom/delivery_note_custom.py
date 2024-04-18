def after_insert(doc, method):
    if doc.docstatus == 0:
        # Submit the Sales Order
        doc.submit()
