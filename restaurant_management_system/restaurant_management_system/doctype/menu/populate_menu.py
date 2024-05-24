import frappe

def create_menus():
    menus = [
        {
            "menu_name": "Breakfast Specials",
            "description": "A variety of breakfast options to start your day.",
            "is_available": 1
        },
        {
            "menu_name": "Lunch Favorites",
            "description": "Delicious and hearty meals perfect for lunchtime.",
            "is_available": 1
        },
        {
            "menu_name": "Dinner Delights",
            "description": "Satisfying dinner options to end your day.",
            "is_available": 1
        },
        {
            "menu_name": "Vegan Options",
            "description": "A selection of tasty vegan dishes.",
            "is_available": 1
        },
        {
            "menu_name": "Kid's Menu",
            "description": "Specially curated meals for kids.",
            "is_available": 1
        },
        {
            "menu_name": "Desserts",
            "description": "Sweet treats to finish your meal.",
            "is_available": 1
        },
        {
            "menu_name": "Beverages",
            "description": "Refreshing drinks to complement your meal.",
            "is_available": 1
        }
    ]

    for menu in menus:
        if not frappe.db.exists("Menu", {"menu_name": menu["menu_name"]}):
            frappe.get_doc({
                "doctype": "Menu",
                "menu_name": menu["menu_name"],
                "description": menu["description"],
                "is_available": menu["is_available"]
            }).insert()

# Execute the function
create_menus()