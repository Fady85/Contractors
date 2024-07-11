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
	accWorkingDays = 0;
	accDaysAmount = 0;
	accTransportationDays = 0;
	accTrAmount = 0;
	accBonusHours = 0;
	accBonusAmount = 0;
	accVoucherAmount = 0;
	for d in cs_data:
		accWorkingDays += d.current_working_days;
		accDaysAmount += d.current_days_amount;
		accTransportationDays += d.transportation_days;
		accTrAmount += d.transportation_total_amount;
		accBonusHours += d.bonus_hours;
		accBonusAmount += d.bonus_total_amount;
		accVoucherAmount += d.current_voucher_amount;
		row = frappe._dict({
				'name':d.name,
				'laborer':d.laborer,
				"laborer_name": d.laborer_name,
				'voucher_number':d.voucher_number,
				'transaction_date':d.transaction_date,
				'project': d.project,
				'current_working_days': d.current_working_days,
				'current_daily_rate': d.current_daily_rate,
				'current_days_amount':d.current_days_amount,
				"transportation_days":d.transportation_days,
				"transportation_rate":d.transportation_rate,
				"transportation_fixed_amount":d.transportation_fixed_amount,
				'transportation_total_amount': d.transportation_total_amount,
				"bonus_hours":d.bonus_hours,
				"hour_rate":d.hour_rate,
				"bonus_fixed_amount":d.bonus_fixed_amount,
				'bonus_total_amount': d.bonus_total_amount,
				'current_voucher_amount':d.current_voucher_amount,
			})
		data.append(row)
	data.append(frappe._dict({
				'current_working_days': accWorkingDays,
				'current_days_amount':accDaysAmount,
				"transportation_days": accTransportationDays,
				"bonus_hours": accBonusHours,
				'transportation_total_amount': accTrAmount,
				'bonus_total_amount': accBonusAmount,
				'current_voucher_amount':accVoucherAmount,
			}))
	# chart = get_chart_data(data)
	# report_summary = get_report_summary(data)
	return columns, data


def get_columns():
	return [
		{
			'fieldname': 'name',
			'label': _('Id'),
			'fieldtype': 'Link',
			"options": "Labor Voucher",
			'width': '200'
		},
		{
			'fieldname': 'laborer',
			'label': _('Laborer'),
			'fieldtype': 'Link',
			'options':'Employee',
			'width': '150'
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
			'precision': 1,
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
			'fieldname': 'transportation_days',
			'label': _('Transportation Days'),
			'fieldtype': 'Float',
			'precision': 1,
			'width': '150'
		},
		{
			'fieldname': 'transportation_rate',
			'label': _('Transportation Rate'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},
		{
			'fieldname': 'transportation_fixed_amount',
			'label': _('Transportation Fixed Amount'),
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
			'fieldname': 'bonus_hours',
			'label': _('Bonus Hours'),
			'fieldtype': 'Float',
			'precision': 1,
			'width': '150'
		},
		{
			'fieldname': 'hour_rate',
			'label': _('Bonus Hour Rate'),
			'fieldtype': 'Currency',
			"options": "currency",
			'width': '150'
		},
		{
			'fieldname': 'bonus_fixed_amount',
			'label': _('Bonus Fixed Amount'),
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
		fields=["name",
		  		"laborer",
				"laborer_name",
		  		"voucher_number",
				"transaction_date",
				"project",
			    "current_working_days",
				"current_daily_rate",
				"current_days_amount",
				"transportation_days",
				"transportation_rate",
				"transportation_fixed_amount",
				"transportation_total_amount",
				"bonus_hours",
				"hour_rate",
				"bonus_fixed_amount",
				"bonus_total_amount",
				"current_voucher_amount"
				],
		filters=conditions,
		order_by='voucher_number'
	)
	return data

def get_conditions(filters):
	conditions = []
	frappe.msgprint(str(filters.get("date_to")))
	if filters.get("date_from") or filters.get("date_to"):
		if filters.date_from and not filters.date_to:
			conditions.append(["transaction_date",'>=', filters.date_from])
		elif filters.date_to and not filters.date_from:
			conditions.append(["transaction_date",'<=', filters.date_to])
		else:
			conditions.append(["transaction_date",'between', [filters.date_from, filters.date_to]])

	for key, value in filters.items():
		if filters.get(key):
			if(key == "date_from" or key == "date_to"):
				None
			else:
				conditions.append([key,'in', value])

	return conditions


