import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import (
	PaymentEntry
)
from frappe.utils import flt
class CustomPaymentEntry(PaymentEntry):
	# //////////////////////////////////////////
	# /////////// Start Custom Code ///////////
	# ////////////////////////////////////////

	def before_submit(self):
		
		if(self.party_type == "Supplier"):
			try:
				invoiceDoc = frappe.get_last_doc('Contractor Invoice', filters={
						"contractor": self.party,
						"project": self.project,
						"docstatus": 1,
						"is_master": 1,
					})
				invoiceDoc.append("payments_list", {
					"payment_id" : self.name,
					"date" : self.posting_date,
					"pay_account" : self.paid_from,
					"bank_account" : self.bank_account,
					"amount" : self.paid_amount,
					"currency" : self.paid_from_account_currency,
				});
				
				invoiceDoc.total_payments = invoiceDoc.total_payments + self.paid_amount;
				invoiceDoc.due_amount = invoiceDoc.due_amount - self.paid_amount;
				invoiceDoc.save(ignore_permissions=True);
			except:
				None;
		elif(self.party_type == "Employee"):		
			try:
				invoiceDoc = frappe.get_last_doc('Labor Voucher', filters={
						"laborer": self.party,
						"project": self.project,
						"docstatus": 1,
						"is_master": 1,
					})
				invoiceDoc.append("labor_payments_list", {
					"payment_id" : self.name,
					"date" : self.posting_date,
					"pay_account" : self.paid_from,
					"bank_account" : self.bank_account,
					"amount" : self.paid_amount,
					"currency" : self.paid_from_account_currency,
				});
				invoiceDoc.total_payments = invoiceDoc.total_payments + self.paid_amount;
				invoiceDoc.due_amount = invoiceDoc.due_amount - self.paid_amount;
				invoiceDoc.save(ignore_permissions=True);
			except Exception as err:
				frappe.throw(str(err))
				print(f"message: {err}")
				None;
	def before_cancel(self):
		if(self.party_type == "Supplier"):
			try:	
				invoiceDoc = frappe.get_last_doc('Contractor Invoice', filters={
						"contractor": self.party,
						"project": self.project,
						"docstatus": 1,
						"is_master": 1,
					})
				invoiceDoc.append("payments_list", {
					"payment_id" : self.name,
					"date" : self.posting_date,
					"pay_account" : self.paid_from,
					"bank_account" : self.bank_account,
					"amount" : self.paid_amount * -1,
					"currency" : self.paid_from_account_currency,
				});
				invoiceDoc.total_payments = invoiceDoc.total_payments - self.paid_amount;
				invoiceDoc.due_amount = invoiceDoc.due_amount + self.paid_amount;
				invoiceDoc.save(ignore_permissions=True);
			except:
				None;
		elif(self.party_type == "Employee"):	
			try:	
				invoiceDoc = frappe.get_last_doc('Labor Voucher', filters={
						"laborer": self.party,
						"project": self.project,
						"docstatus": 1,
						"is_master": 1,
					})
				invoiceDoc.append("labor_payments_list", {
					"payment_id" : self.name,
					"date" : self.posting_date,
					"pay_account" : self.paid_from,
					"bank_account" : self.bank_account,
					"amount" : self.paid_amount * -1,
					"currency" : self.paid_from_account_currency,
				});
				invoiceDoc.total_payments = invoiceDoc.total_payments - self.paid_amount;
				invoiceDoc.due_amount = invoiceDoc.due_amount + self.paid_amount;
				invoiceDoc.save(ignore_permissions=True);
			except:
				None;

	# //////////////////////////////////////////
	# /////////// end Custom Code /////////////
	# ////////////////////////////////////////