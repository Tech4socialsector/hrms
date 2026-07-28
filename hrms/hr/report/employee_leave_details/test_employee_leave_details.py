# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe.utils import add_days, getdate

from erpnext.setup.doctype.employee.test_employee import make_employee

from hrms.hr.doctype.holiday_list_assignment.test_holiday_list_assignment import assign_holiday_list
from hrms.hr.doctype.leave_application.test_leave_application import make_allocation_record
from hrms.hr.report.employee_leave_details.employee_leave_details import execute
from hrms.payroll.doctype.salary_slip.test_salary_slip import make_holiday_list, make_leave_application
from hrms.tests.test_utils import get_first_sunday
from hrms.tests.utils import HRMSTestSuite

test_records = frappe.get_test_records("Leave Type")


class TestEmployeeLeaveDetails(HRMSTestSuite):
	def setUp(self):
		for dt in ["Leave Application", "Leave Allocation", "Leave Ledger Entry", "Leave Type"]:
			frappe.db.delete(dt)

		frappe.set_user("Administrator")

		self.employee_id = make_employee("test_emp_leave_details@example.com", company="_Test Company")

		self.date = getdate()
		self.year_start = getdate(f"{self.date.year}-01-01")
		self.year_end = getdate(f"{self.date.year}-12-31")

		self.holiday_list = make_holiday_list(
			"_Test Emp Leave Details Holiday List", self.year_start, self.year_end
		)

	@assign_holiday_list("_Test Emp Leave Details Holiday List", "_Test Company")
	def test_employee_leave_details(self):
		frappe.get_doc(test_records[0]).insert()

		make_allocation_record(
			employee=self.employee_id, from_date=self.year_start, to_date=self.year_end
		)

		first_sunday = get_first_sunday(self.holiday_list, for_date=self.year_start)
		leave_application = make_leave_application(
			self.employee_id, add_days(first_sunday, 1), add_days(first_sunday, 4), "_Test Leave Type"
		)
		leave_application.reload()

		filters = frappe._dict(
			{
				"from_date": self.year_start,
				"to_date": self.year_end,
				"company": "_Test Company",
				"employee": self.employee_id,
			}
		)

		report = execute(filters)
		data = report[1]

		self.assertEqual(len(data), 1)
		self.assertEqual(data[0].employee, self.employee_id)
		self.assertEqual(data[0].leave_type, "_Test Leave Type")
		self.assertEqual(data[0].total_leave_days, leave_application.total_leave_days)
		self.assertEqual(data[0].status, "Approved")

	@assign_holiday_list("_Test Emp Leave Details Holiday List", "_Test Company")
	def test_leave_type_filter_excludes_other_types(self):
		frappe.get_doc(test_records[0]).insert()
		other_leave_type = "_Test Leave Type 1"
		if not frappe.db.exists("Leave Type", other_leave_type):
			frappe.get_doc(test_records[1]).insert()

		make_allocation_record(
			employee=self.employee_id, from_date=self.year_start, to_date=self.year_end
		)
		make_allocation_record(
			employee=self.employee_id,
			from_date=self.year_start,
			to_date=self.year_end,
			leave_type=other_leave_type,
		)

		first_sunday = get_first_sunday(self.holiday_list, for_date=self.year_start)
		leave_application = make_leave_application(
			self.employee_id, add_days(first_sunday, 1), add_days(first_sunday, 2), "_Test Leave Type"
		)
		leave_application.reload()

		filters = frappe._dict(
			{
				"from_date": self.year_start,
				"to_date": self.year_end,
				"company": "_Test Company",
				"employee": self.employee_id,
				"leave_type": other_leave_type,
			}
		)

		report = execute(filters)
		self.assertEqual(len(report[1]), 0)

	@assign_holiday_list("_Test Emp Leave Details Holiday List", "_Test Company")
	def test_date_range_excludes_out_of_range_applications(self):
		frappe.get_doc(test_records[0]).insert()

		make_allocation_record(
			employee=self.employee_id, from_date=self.year_start, to_date=self.year_end
		)

		first_sunday = get_first_sunday(self.holiday_list, for_date=self.year_start)
		leave_application = make_leave_application(
			self.employee_id, add_days(first_sunday, 1), add_days(first_sunday, 2), "_Test Leave Type"
		)
		leave_application.reload()

		filters = frappe._dict(
			{
				"from_date": add_days(leave_application.to_date, 1),
				"to_date": self.year_end,
				"company": "_Test Company",
				"employee": self.employee_id,
			}
		)

		report = execute(filters)
		self.assertEqual(len(report[1]), 0)
