// Copyright (c) 2024, Hilda Baraiywo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Menu Item", {
	refresh(frm) {
        frm.add_custom_button('New Item', () => {
            frappe.new_doc('Menu Item', {
                menu_item: frm.doc.name
            })
        })
	},
});
