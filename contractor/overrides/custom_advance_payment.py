import frappe
from hrms.hr.doctype.employee_advance.employee_advance import (
	EmployeeAdvance
)
class CustomEmployeeAdvance(EmployeeAdvance):
    def on_submit(self):
        frappe.db.set_value('Employee Advance', self.name, 'status', 'Paid');
        frappe.db.set_value('Employee Advance', self.name, 'paid_amount', self.advance_amount);
        self.reload()
    
    