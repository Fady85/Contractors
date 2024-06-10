# Copyright (c) 2024, cltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LaborVoucher(Document):
	@frappe.whitelist()
	def laborer_number(self):
		try:
			doc = frappe.get_last_doc('Labor Voucher',
					filters={
						"laborer": self.laborer,
						"project": self.project,
						"docstatus": 1
					},
					order_by="voucher_number desc"
				);
			return doc;
		except Exception as error :
			return None;
	@frappe.whitelist()
	def laborer_payments(self):
		payments = frappe.db.get_list('Payment Entry', 
				filters={
				"party": self.laborer,
				"project": self.project,
				"docstatus": 1
			},
			fields=["name", "posting_date", "paid_from", "bank_account", "paid_amount", "paid_from_account_currency"]
		);
		return payments;

	@frappe.whitelist()
	def get_laborer_name(self):
		laborer_data = frappe.db.get_value('Employee', str(self.laborer), 'employee_name')
		self.laborer_name = laborer_data
		return
	# @frappe.whitelist()
	# def entry_account(self):
	# 	try:
	# 		laborer_data = frappe.get_doc('Labor Settings');
	# 		return laborer_data.labor_due_account;
	# 	except Exception as ex:
	# 		return
	@frappe.whitelist()
	def labor_cost_center(self):
		# projectDoc = frappe.get_doc("Project", self.project);
		projectCostCenter = frappe.db.get_value('Project', str(self.project), 'cost_center');
		self.cost_center = projectCostCenter
		return ;

	def before_submit(self):
		voucherCount = frappe.db.count('Labor Voucher',
				   {
					'laborer': self.laborer,
					"project": self.project,
					"docstatus": 1,
					"voucher_number": self.voucher_number
					})
		if(voucherCount):
			frappe.throw("there is an invoice with this number please create a new one")
		if self.voucher_number != 1:
			lastDoc = frappe.get_last_doc('Labor Voucher', filters={
			"laborer":self.laborer,
			"project": self.project,
			"docstatus": 1
			}, order_by="voucher_number desc");
			lastDoc.is_master = 0;
			lastDoc.save()
		self.is_master = 1;
		self.status = "Submitted"	
		def create_gl_entry():
			accountingSettings = frappe.get_doc('Labor Settings')
			if(not accountingSettings.labor_due_account):
				frappe.throw("please set labor due account in labor settings first before submit")
			if(not accountingSettings.labor_expense_account):
				frappe.throw("please set Labor Expense Account in labor settings first before submit")	
			expense_account = accountingSettings.labor_expense_account;
			due_account = accountingSettings.labor_due_account;
			voucher_type = self.doctype
			voucher_number = self.name;
			party = self.laborer;
			party_type = "Employee";
			project = self.project;
			cost_center = self.cost_center;
			day = frappe.utils.today();
			
			currentNumber = self.current_voucher_amount;
			firstDoc = frappe.new_doc('GL Entry')
			secondDoc = frappe.new_doc('GL Entry')
			
			firstDoc.account = expense_account if currentNumber > 0 else due_account
			firstDoc.posting_date = frappe.utils.today()
			firstDoc.account_currency= "EGP"
			firstDoc.against= party if currentNumber > 0 else expense_account
			firstDoc.debit= abs(currentNumber)
			firstDoc.debit_in_account_currency= abs(currentNumber)
			firstDoc.credit=0
			firstDoc.credit_in_account_currency= 0 
			firstDoc.voucher_type= voucher_type
			firstDoc.voucher_no= voucher_number
			firstDoc.party_type = party_type
			firstDoc.party = party
			firstDoc.project = project
			firstDoc.cost_center = cost_center
			
			secondDoc.account = due_account if currentNumber > 0 else expense_account
			secondDoc.posting_date = frappe.utils.today()
			secondDoc.account_currency= "EGP"
			secondDoc.against= expense_account if currentNumber > 0 else party
			secondDoc.debit= 0
			secondDoc.debit_in_account_currency= 0
			secondDoc.credit= abs(currentNumber)
			secondDoc.credit_in_account_currency= abs(currentNumber)
			secondDoc.voucher_type = voucher_type
			secondDoc.voucher_no = voucher_number
			secondDoc.party_type = party_type
			secondDoc.party = party
			secondDoc.project = project
			secondDoc.cost_center = cost_center
			
			firstDoc.insert(ignore_permissions=True)
			secondDoc.insert(ignore_permissions=True)

		create_gl_entry()
	def before_cancel(self):
		# frappe.db.delete("Invoice Item")
		# frappe.throw(str(frappe.db.get_value('Company', self.company, 'default_currency')))
  		# frappe.throw(str(frappe.db.get_list("Invoice Item", fields="*")))
		lastDoc = frappe.get_last_doc('Labor Voucher', filters={
			"laborer":self.laborer,
			"project": self.project,
			"docstatus": 1
			}, order_by="voucher_number desc");
		if(lastDoc.voucher_number != self.voucher_number):
			frappe.throw("there is one or more invoices after this one please cancel them first")

		if self.voucher_number != 1:
			lastNotCanceledDoc = frappe.get_last_doc('Labor Voucher', filters={
			"laborer":self.laborer,
			"project": self.project,
			"voucher_number": self.voucher_number - 1,
			"docstatus": 1
			}, order_by="voucher_number desc");
			lastNotCanceledDoc.is_master = 1;
			lastNotCanceledDoc.save();
		self.is_master = 0;
		self.status = "Canceled";
		entriesList = frappe.db.get_list('GL Entry',
						filters={
							"voucher_type": self.doctype,
							"voucher_no": self.name
						}
					);
		
		for docName in entriesList :
			entryDoc = frappe.get_doc("GL Entry", docName.name)
			frappe.db.set_value('GL Entry', docName.name, 'is_cancelled', 1)
			if(entryDoc.debit):
				frappe.db.set_value('GL Entry', docName.name, {
					'credit': entryDoc.debit,
					'credit_in_account_currency':entryDoc.debit_in_account_currency
				})
			elif (entryDoc.credit):
				frappe.db.set_value('GL Entry', docName.name, {
					'debit': entryDoc.credit,
					'debit_in_account_currency':entryDoc.credit_in_account_currency
				})
	def on_trash(self):
		frappe.db.delete("GL Entry", {
		"voucher_type": self.doctype,
		"voucher_no": self.name
	})	