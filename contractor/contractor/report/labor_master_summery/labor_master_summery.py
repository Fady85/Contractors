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
				'name': d.name,
				'laborer': d.laborer,
				"laborer_name": d.laborer_name,
				'voucher_number': d.voucher_number,
				'project': d.project,
				'accumulated_working_days': d.accumulated_working_days,
				"voucher_amount": d.prev_days_amount + d.current_days_amount,
				"bonus_amount":d.prev_bonus_amount + d.bonus_total_amount,
				"transportation_amount":d.prev_transportation_amount + d.transportation_total_amount,
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
			'fieldname': 'name',
			'label': _('Id'),
			"fieldtype": "Link",
			"options": "Labor Voucher",
			'width': '200'
		},
		{
			'fieldname': 'laborer',
			'label': _('Laborer'),
			"fieldtype": "Link",
			"options": "Supplier",
			'width': '200'
		},
		{
			'fieldname': 'laborer_name',
			'label': _('laborer Name'),
			"fieldtype": "Data",
			'width': '200'
		},
		{
			'fieldname': 'voucher_number',
			'label': _('Voucher Number'),
			'fieldtype': 'Int',
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
			'fieldname': 'voucher_amount',
			'label': _('Acc Vouchers Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
			'precision': 1,
			'width': '150'
		},
		{
			'fieldname': 'bonus_amount',
			'label': _('Acc Bonus Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
			'precision': 1,
			'width': '150'
		},
		{
			'fieldname': 'transportation_amount',
			'label': _('Acc Transportation Amount'),
			'fieldtype': 'Currency',
			"options": "currency",
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
		fields=['name',
		  		'laborer',
		  		'laborer_name',
		  		"voucher_number",
		   		'project',
			    "accumulated_working_days",
			    "total_vouchers_amount",
				"total_payments",
			    "due_amount",
				"prev_bonus_amount",
				"bonus_total_amount",
				"prev_days_amount",
				"current_days_amount",
				"prev_transportation_amount",
				"transportation_total_amount"
				],
		filters=conditions,
		order_by='name desc'
	)
	return data

def get_conditions(filters):
	conditions = []
	if filters.get("date_from") or filters.get("date_to"):
		if filters.date_from and not filters.date_to:
			conditions.append(["transaction_date",'>=', filters.date_from])
		elif filters.date_to and not filters.date_from:
			conditions.append(["transaction_date",'<=', filters.date_to])
		else:
			conditions.append(["transaction_date",'between', [filters.date_from, filters.date_to]])

	for key, value in filters.items():
		if filters.get(key):
			if(type(value) == list):
				conditions.append([key,'in', value])
			elif(key == "date_from" or key == "date_to"):
				None
			else:
				conditions.append([key,'=', value])

	return conditions