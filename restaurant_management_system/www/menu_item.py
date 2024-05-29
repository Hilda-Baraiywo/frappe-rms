import frappe

def get_context(context):
    context.items = frappe.get_all("Menu Item", fields=["name", "item_name", "description", "price", "image"])
