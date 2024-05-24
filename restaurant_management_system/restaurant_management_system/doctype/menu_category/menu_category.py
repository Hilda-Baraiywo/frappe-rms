# Copyright (c) 2024, Hilda Baraiywo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MenuCategory(Document):
    def before_save(self):
        if frappe.db.exists("Menu Category", {"category": self.category, "name": ["!=", self.name]}):
            frappe.throw("Menu category name already exists.")