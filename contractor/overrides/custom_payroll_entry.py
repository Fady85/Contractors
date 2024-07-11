import frappe
from hrms.payroll.doctype.payroll_entry.payroll_entry import (
	PayrollEntry
)
class CustomPayrollEntry(PayrollEntry):
    def on_trash(self):
        try:
            frappe.db.delete("GL Entry", {
				"against_voucher": self.name,
			})
        except Exception as ex:
            frappe.throw(str(ex))