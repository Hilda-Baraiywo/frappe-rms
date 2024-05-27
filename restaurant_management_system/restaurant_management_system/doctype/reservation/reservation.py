# Copyright (c) 2024, Hilda Baraiywo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Reservation(Document):
    def before_save(self):
        self.validate_reservation_number()
        self.validate_customer()
        self.validate_reservation_date()
        self.validate_number_of_people()

    def validate_reservation_number(self):
        if frappe.db.exists("Reservation", {"reservation_number": self.reservation_number, "name": ["!=", self.name]}):
            frappe.throw("Reservation number already exists.")

    def validate_customer(self):
        if not frappe.db.exists("Customer",self.customer_name):
            frappe.throw("Customer name does not exist.")

    def validate_reservation_date(self):
        if self.reservation_date <= frappe.utils.nowdate():
            frappe.throw("Reservation date must be in the future.")

    def validate_number_of_people(self):
        if self.capacity <= 0:
            frappe.throw("Number of people must be a positive number.")