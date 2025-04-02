// Copyright (c) 2025, soorya and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Visitor", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Visitor', {
    refresh: function(frm) {
        // Add a custom button to the form
        frm.add_custom_button(__('Go to Email Queue'), function() {
            // Navigate to the Email Queue list
            frappe.set_route('List', 'Email Queue');
        }).addClass('btn-primary'); // Optional: Add a class for styling
    }
});