# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import cint, flt

Filters = frappe._dict


def execute(filters: Filters | None = None) -> tuple:
	filters = filters or frappe._dict()

	if filters.from_date and filters.to_date and filters.to_date < filters.from_date:
		frappe.throw(_('"From Date" can not be greater than "To Date"'))

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	return [
		{
			"label": _("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120,
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Department"),
			"fieldname": "department",
			"fieldtype": "Link",
			"options": "Department",
			"width": 150,
		},
		{
			"label": _("Leave Type"),
			"fieldname": "leave_type",
			"fieldtype": "Link",
			"options": "Leave Type",
			"width": 150,
		},
		{
			"label": _("Leave Application"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Leave Application",
			"width": 150,
		},
		{
			"label": _("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": _("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": _("Half Day"),
			"fieldname": "half_day",
			"fieldtype": "Check",
			"width": 80,
		},
		{
			"label": _("Leaves Taken"),
			"fieldname": "total_leave_days",
			"fieldtype": "Float",
			"width": 110,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Reason"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 200,
		},
	]


def get_data(filters: Filters) -> list[dict]:
	LeaveApplication = frappe.qb.DocType("Leave Application")
	Employee = frappe.qb.DocType("Employee")

	query = (
		frappe.qb.from_(LeaveApplication)
		.inner_join(Employee)
		.on(LeaveApplication.employee == Employee.name)
		.select(
			LeaveApplication.name,
			LeaveApplication.employee,
			LeaveApplication.employee_name,
			Employee.department,
			LeaveApplication.leave_type,
			LeaveApplication.from_date,
			LeaveApplication.to_date,
			LeaveApplication.half_day,
			LeaveApplication.total_leave_days,
			LeaveApplication.status,
			LeaveApplication.description,
		)
		.where(LeaveApplication.docstatus == 1)
		.orderby(LeaveApplication.employee)
		.orderby(LeaveApplication.from_date)
	)

	if filters.get("from_date"):
		query = query.where(LeaveApplication.to_date >= filters.from_date)

	if filters.get("to_date"):
		query = query.where(LeaveApplication.from_date <= filters.to_date)

	if filters.get("company"):
		query = query.where(LeaveApplication.company == filters.company)

	if filters.get("department"):
		query = query.where(Employee.department == filters.department)

	if filters.get("employee"):
		query = query.where(LeaveApplication.employee == filters.employee)

	if filters.get("leave_type"):
		query = query.where(LeaveApplication.leave_type == filters.leave_type)

	if filters.get("employee_status"):
		query = query.where(Employee.status == filters.employee_status)

	query = query.where(LeaveApplication.status == (filters.get("status") or "Approved"))

	data = query.run(as_dict=True)

	precision = cint(frappe.db.get_single_value("System Settings", "float_precision"))
	for row in data:
		row.total_leave_days = flt(row.total_leave_days, precision)

	return add_total_row(data)


def add_total_row(data: list[dict]) -> list[dict]:
	if not data:
		return data

	total_row = frappe._dict(
		{
			"employee_name": _("Total"),
			"total_leave_days": sum(flt(row.total_leave_days) for row in data),
		}
	)
	data.append(total_row)

	return data
