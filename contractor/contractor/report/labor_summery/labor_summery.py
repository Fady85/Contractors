# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint



def execute(filters=None):
	if not filters: filters = {}
	# frappe.throw(str(filters))

	data, columns = [], []

	columns = get_columns()
	cs_data = get_cs_data(filters)

	if not cs_data:
		msgprint(_('No records found'))
		return columns, cs_data

	data = []
	for d in cs_data:
		row = frappe._dict({
				'laborer':d.laborer,
				'voucher_number':d.voucher_number,
				'transaction_date':d.transaction_date,
				'project': d.project,
				'current_working_days': d.current_working_days,
				'current_daily_rate': d.current_daily_rate,
				'current_days_amount':d.current_days_amount,
				'transportation_total_amount': d.transportation_total_amount,
				'bonus_total_amount': d.bonus_total_amount,
				'current_voucher_amount':d.current_voucher_amount,
			})
		

		data.append(row)
	# chart = get_chart_data(data)
	# report_summary = get_report_summary(data)
	return columns, data


def get_columns():
	return [
		# {
		# 	'fieldname': 'name',
		# 	'label': _('Id'),
		# 	'fieldtype': 'Link',
		# 	"options": "Contractor Invoice",
		# 	'width': '200'
		# },transaction_date
		{
			'fieldname': 'laborer',
			'label': _('Laborer'),
			'fieldtype': 'Link',
			'options':'Employee',
			'width': '150'
		},
		{
			'fieldname': 'voucher_number',
			'label': _('Voucher Number'),
			"fieldtype": "Int",
			'width': '50'
		},
		{
			'fieldname': 'transaction_date',
			'label': _('Date'),
			"fieldtype": "Date",
			'width': '100'
		},

		{
			'fieldname': 'project',
			'label': _('Project'),
			'fieldtype': 'Data',
			'width': '150'
		},
		{
			'fieldname': 'current_working_days',
			'label': _('Working Days'),
			'fieldtype': 'Float',
			'Precision':1,
			'width': '150'
		},
		{
			'fieldname': 'current_daily_rate',
			'label': _('Daily Rate'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},
		{
			'fieldname': 'current_days_amount',
			'label': _('Days Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},
		{
			'fieldname': 'transportation_total_amount',
			'label': _('Transportation Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},
		{
			'fieldname': 'bonus_total_amount',
			'label': _('Bonus Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},
		{
			'fieldname': 'current_voucher_amount',
			'label': _('Voucher Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},

	]

def get_cs_data(filters):
	conditions = get_conditions(filters)
	data = frappe.get_all(
		doctype='Labor Voucher',
		fields=["laborer",
		  		"voucher_number",
				"transaction_date",
				"project",
			    "current_working_days",
				"current_daily_rate",
				"current_days_amount",
				"transportation_total_amount",
				"bonus_total_amount",
				"current_voucher_amount"
				],
		filters=conditions,
		order_by='voucher_number'
	)
	return data

def get_conditions(filters):
	conditions = {}
	for key, value in filters.items():
		if filters.get(key):
			conditions[key] = ('in',value) 

	return conditions


