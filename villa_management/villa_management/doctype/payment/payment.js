// Copyright (c) 2025, soorya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment", {
	refresh(frm) {

	},
});
frappe.ui.form.on('Payment', {
    resident: function(frm) {
        if (frm.doc.type === 'Monthly Fund' && frm.doc.resident) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Payment',
                    filters: {
                        type: 'Monthly Fund',
                        resident: frm.doc.resident,
                        created: ['between', [get_first_day_of_month(), get_last_day_of_month()]],
                        name: ['!=', frm.doc.name || '']
                    },
                    fields: ['name', 'created']
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        let existing_payment = r.message[0];
                        let month_year = frappe.datetime.str_to_obj(existing_payment.created).toLocaleString('default', { month: 'long', year: 'numeric' });
                        
                        frappe.msgprint({
                            title: __('Validation Error'),
                            indicator: 'red',
                            message: __(
                                'A Monthly Fund payment for resident {0} already exists for {1}. Please select a different type or resident.',
                                [frm.doc.resident_name, month_year]
                            )
                        });
                        
                        // Reset the resident field
                        frm.set_value('resident', '');
                        frm.set_value('resident_name', '');
                    }
                }
            });
        }
    }
});

function get_first_day_of_month() {
    let d = new Date();
    return new Date(d.getFullYear(), d.getMonth(), 1);
}

function get_last_day_of_month() {
    let d = new Date();
    return new Date(d.getFullYear(), d.getMonth() + 1, 0);
}