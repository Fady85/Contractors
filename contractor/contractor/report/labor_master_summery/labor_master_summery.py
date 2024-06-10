# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint



def execute(filters=None):
	if not filters: filters = {}
	
	data, columns = [], []

	columns = get_columns()
	cs_data = get_cs_data(filters)

	if not cs_data:
		msgprint(_('No records found'))
		return columns, cs_data

	data = []
	for d in cs_data:
		row = frappe._dict({
				'laborer': d.laborer,
				'voucher_number': d.voucher_number,
				'project': d.project,
				'accumulated_working_days': d.accumulated_working_days,
				'total_vouchers_amount':d.total_vouchers_amount,
				'total_payments': d.total_payments,
				'due_amount': d.due_amount,
			})
		

		data.append(row)
	# chart = get_chart_data(data)
	# report_summary = get_report_summary(data)
	return columns, data


def get_columns():
	return [

		{
			'fieldname': 'laborer',
			'label': _('Laborer'),
			"fieldtype": "Link",
			"options": "Supplier",
			'width': '200'
		},
		{
			'fieldname': 'voucher_number',
			'label': _('Voucher Number'),
			'fieldtype': 'Int',
			"options": "currency",
			'width': '50'
		},
		{
			'fieldname': 'project',
			'label': _('Project'),
			'fieldtype': 'Data',
			'width': '150'
		},

		{
			'fieldname': 'accumulated_working_days',
			'label': _('Acc Working Days'),
			'fieldtype': 'Float',
			'precision': 1,
			'width': '150'
		},
		{
			'fieldname': 'total_vouchers_amount',
			'label': _('Total Vouchers Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},

		{
			'fieldname': 'total_payments',
			'label': _('Payments'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},
		{
			'fieldname': 'due_amount',
			'label': _('Due Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		}
	]

def get_cs_data(filters):
	conditions = get_conditions(filters)
	data = frappe.get_all(
		doctype='Labor Voucher',
		fields=['laborer',
		  		"voucher_number",
		   		'project',
			    "accumulated_working_days",
			    "total_vouchers_amount",
				"total_payments",
			    "due_amount",
				],
		filters=conditions,
		order_by='name desc'
	)
	return data

def get_conditions(filters):
	conditions = {}
	for key, value in filters.items():
		if filters.get(key):
			if(type(value) == list):
				conditions[key] = ('in', value)
			else:
				conditions[key] = value

	return conditions