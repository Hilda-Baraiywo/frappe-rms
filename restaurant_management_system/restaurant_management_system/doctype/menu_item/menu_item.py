# Copyright (c) 2024, Hilda Baraiywo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MenuItem(Document):
    def before_save(self):
        self.validate_item_name()
        self.validate_price()
        self.validate_category()
        
def validate_item_name(self):
	if frappe.db.exists("Menu Item", {"item_name": self.item_name, "menu_category": self.menu_category, "name": ["!=", self.name]}):
		frappe.throw("Menu item name already exists in this category.")
			
def validate_price(self):
	if self.price <= 0:
		frappe.throw("Price must be a positive number.")
			
def validat_category(self):
	if not frappe.db.exists("Menu Category", self.menu_category):
		frappe.throw("Selected menu category does not exist.")