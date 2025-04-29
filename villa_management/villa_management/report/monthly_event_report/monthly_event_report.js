 // // Copyright (c) 2025, soorya and contributors
 // // For license information, please see license.txt

// frappe.query_reports["Monthly Event Report"] = {
// 	"filters": [

// 		{
//             "fieldname": "from_date",
//             "label": __("From Date"),
//             "fieldtype": "Date",
//             "default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
//             "width": "80"
//         },
//         {
//             "fieldname": "to_date",
//             "label": __("To Date"),
//             "fieldtype": "Date",
//             "default": frappe.datetime.get_today()
//         },
//         {
//             "fieldname": "type",
//             "label": __("Type"),
//             "fieldtype": "Select",
//             "options": ["", "Special Events", "Seasonal Events", "Trips"] // Add your event types
//         }

// 	]
// };
frappe.query_reports["Monthly Event Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), 1),
            "reqd": 1
        },
        {
            "fieldname": "type",
            "label": __("Event Type"),
            "fieldtype": "Select",
            "options": ["", "Special Events", "Seasonal Events", "Trips"],
            "default": ""
        }
    ],
    "formatter": function(value, row, column, data) {
        if (column.fieldname == "status") {
            return value === "Completed" 
                ? `<span class="indicator blue">${value}</span>`
                : `<span class="indicator orange">${value}</span>`;
        }
        if (column.fieldname == "variance") {
            const color = value >= 0 ? "green" : "red";
            return `<span class="indicator ${color}">${value}</span>`;
        }
        return value;
    },
    "get_summary": function(data) {
        return data.summary || [];
    }
};