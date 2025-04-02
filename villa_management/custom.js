frappe.call({
    method: 'villa_management.custom_app.get_villa_numbers',
    callback: function(response) {
        if (response.message) {
            console.log(response.message);
        }
    },
    error: function(error) {
        console.error('Error:', error);
    }
});
