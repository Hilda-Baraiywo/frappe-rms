# Copyright (c) 2024, Hilda Baraiywo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Attendance(Document):
	def validate(self):
		self.validate_schedule()
		self.validate_check_in_out_times()
		self.calculate_overtime()
		self.validate_break_times()
		self.check_holiday_leave()
		self.set_attendance_status()
	
	def validate_schedule(self):
		if not frappe.db.exists("Staff Schedule", {"staff_name": self.staff_name, "date": self.attendance_date}):
			frappe.throw("Staff member is not scheduled to work on this date.")
	
	def validate_check_in_out_times(self):
		if self.check_in_time < self.get_schedule_start_time():
			frappe.throw("Check-in time cannot be earlier than the scheduled start time.")
		
		if self.check_out_time > self.get_schedule_end_time():
			frappe.throw("Check-out time cannot be later than the scheduled end time.")
		
		existing_attendance = frappe.db.exists("Attendance", {"staff_name": self.staff_name, "attendance_date": self.attendance_date})
		if existing_attendance and existing_attendance != self.name:
			frappe.throw("Attendance record already exists for this date.")

	def calculate_overtime(self):
		scheduled_start_time = self.get_schedule_start_time()
		scheduled_end_time = self.get_schedule_end_time()
		scheduled_shift_duration = scheduled_end_time - scheduled_start_time

		actual_worked_hours = self.check_out_time - self.check_in_time

		if actual_worked_hours > scheduled_shift_duration:
			self.overtime_hours = actual_worked_hours - scheduled_shift_duration
		else:
			self.overtime_hours = 0

	def validate_break_times(self):
		scheduled_start_time = self.get_scheduled_start_time()
		scheduled_end_time = self.get_schedule_end_time()

		if self.break_start_time < scheduled_start_time or self.break_end_time > scheduled_end_time:
			frappe.throw("Break times must be within the scheduled shift durations")

	def check_holiday_leave(self):
		if self.is_holiday():
			frappe.throw("The attendance date falls on a holiday.")
	
	def set_attendance_status(self):
		if self.is_on_leave():
			self.status = "On Leave"
		elif not self.check_in_time:
			self.status = "Absent"
		elif self.check_in_time > self.get_schedule_start_time():
			self.status = "Late"
		elif (self.check_out_time - self.check_in_time).total_seconds() < self.get_shift_duration() * 3600:
			self.status = "Half Day"
		else:
			self.status = "Present"
	
	def get_schedule_start_time(self):
		return frappe.db.get_value("Staff Schedule", {"staff_name": self.staff_name, "date": self.attendance_date}, "start_time")
	
	def get_schedule_end_time(self):
		return frappe.db.get_value("Staff Schedule", {"staff_name": self.staff_name, "date": self.attendance_date}, "end_time")

	def get_shift_duration(self):
		start_time = self.get_schedule_start_time()
		end_time = self.get_schedule_end_time()
		shift_duration = (end_time - start_time).total_seconds() / 3600
		return shift_duration

	def is_holiday(self):
		holiday_list = frappe.db.get_value("Restaurant Staff", self.staff_name, "holiday_list")
		return frappe.db.exists("Leave Application", {
			"staff_name": self.staff_name,
			"from_date": ["<=", self.attendance_date],
			"to_date": [">=", self.attendance_date],
			"status": "Approved"
		})
	def check_cutoff_time(self):
		cutoff_time = frappe.db.get_value("Attendance Settings", None, "attendance_cutoof_time")
		if self.check_in_time() > datetime.strptime(cutoff_time, "%H:%M:%S").time():
			self.status = "Late"
