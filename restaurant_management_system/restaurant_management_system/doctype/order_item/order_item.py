# Copyright (c) 2024, Hilda Baraiywo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class OrderItem(Document):
    def before_save(self):
        self.validate_item()
        self.validate_quantity_price()
        self.calculate_amount()
        
def validate_item(self):
    if not frappe.db.exists("Menu Item", self.item_name):
        frappe.throw("Menu item does not exist.")

def validate_quantity_price(self):
    if self.quantity <= 0:
        frappe.throw("Quantity must be a positive number.")
    if self.price <= 0:
        frappe.throw("Price must be a positive number.")

def calculate_amount(self):
    self.amount = self.quanity * self.price