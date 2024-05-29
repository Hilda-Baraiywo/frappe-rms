# Copyright (c) 2024, Hilda Baraiywo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Order(Document):
    def before_save(self):
        self.validate_order_number()
        self.validate_order_date()
        self.calculate_total_amount()

    def validate_order_number(self):
        if frappe.db.exists("Order", {"order_number": self.order_number, "name": ["!=", self.name]}):
            frappe.throw("Order number already exists.")

    def validate_order_date(self):
        if self.order_date > frappe.utils.nowdate():
            frappe.throw("Order date cannot be in the future.")

    def calculate_total_amount(self):
        total_amount = sum(item.amount for item in self.order_item)
        self.total_amount = total_amount
