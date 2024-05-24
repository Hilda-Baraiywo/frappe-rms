# Copyright (c) 2024, Hilda Baraiywo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address
from frappe.model.docstatus import DocStatus


class Customer(Document):
		def before_save(self):
			self.validate_email()
			self.validate_phone_number()
			self.check_duplicate_email()
			
		def validate_email(self):
			if not validate_email_address(self.email_address):
				frappe.throw("Invalid email address format.")
			
		def validate_phone_number(self):
					if not self.phone_number.isdigit() or len(self.phone_number) not in [10, 12]:
						frappe.throw("Invalid phone number format.")
			
		def check_duplicate_email(self):
					if frappe.db.exists("Customer", {"email_address": self.email_address, "name": ["!=", self.name]}):
						frappe.throw("Email address already exists.")
			
		def before_submit(self):
			exists = frappe.db.exists(
				{
					"doctype":"Customer",
					"email_address": self.email_address,
					"docstatus": DocStatus.submitted
				}
			)
			if exists:
				frappe.throw("There is an active membership for this customer.")