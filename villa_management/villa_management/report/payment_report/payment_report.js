// Copyright (c) 2025, soorya and contributors
// For license information, please see license.txt

// frappe.query_reports["Payment Report"] = {
// 	"filters": [

// 	]
// };

// frappe.query_reports["Payment Report"] = {
//     "filters": [
//         {
//             "fieldname": "from_date",
//             "label": __("From Date"),
//             "fieldtype": "Date",
//             "default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
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
//             "options": ["", "Monthly Fund", "Other"]
//         },
//         {
//             "fieldname": "payment_mode",
//             "label": __("Payment Mode"),
//             "fieldtype": "Select",
//             "options": ["", "Cash", "UPI"]
//         },
//         {
//             "fieldname": "paid",
//             "label": __("Status"),
//             "fieldtype": "Select",
//             "options": ["", "Paid", "Pending"],
//             "default": "",
//             "map": {
//                 "Paid": 1,
//                 "Pending": 0
//             }
//         }
//     ],
//     "formatter": function(value, row, column, data, defaultFormatter) {
//         value = defaultFormatter(value, row, column, data);
        
//         if (data.is_summary) {
//             return `<strong>${value}</strong>`;
//         }
//         if (data.is_breakdown) {
//             return `<span style="margin-left: ${data.indent * 15}px">${value}</span>`;
//         }
//         return value;
//     }
// };
frappe.query_reports["Payment Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "type",
            "label": __("Payment Type"),
            "fieldtype": "Select",
            "options": ["", "Monthly Fund", "Other"],
            "default": ""
        },
        {
            "fieldname": "payment_mode",
            "label": __("Payment Mode"),
            "fieldtype": "Select",
            "options": ["", "Cash", "UPI", "Bank Transfer"],
            "default": ""
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": ["", "Paid", "Pending"],
            "default": ""
        }
    ],
    "formatter": function(value, row, column, data) {
        if (column.fieldname == "status") {
            return value === "Paid" 
                ? `<span class="indicator green">${value}</span>`
                : `<span class="indicator red">${value}</span>`;
        }
        return value;
    },
    "get_summary": function(data) {
        // This will use the summary returned from Python
        return data.summary || [];
    }
};