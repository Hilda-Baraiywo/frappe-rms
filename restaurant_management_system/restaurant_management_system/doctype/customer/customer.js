// Copyright (c) 2024, Hilda Baraiywo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
	refresh(frm) {
        frm.add_custom_button('New Customer', () => {
            frappe.new_doc('Customer', {
                customer: frm.doc.name
            })
        })
	},
});
