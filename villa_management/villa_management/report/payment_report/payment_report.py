# from __future__ import unicode_literals
# import frappe
# from frappe import _
# from frappe.utils import formatdate, getdate, nowdate
# from datetime import datetime

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
    
#     # Add only monthly summary (no paid/pending breakdown)
#     data = add_monthly_summary(data)
    
#     # Prepare charts
#     charts = get_charts(data)
    
#     return columns, data, None, charts

# def get_columns():
#     return [
#         {"label": _("ID"), "fieldname": "name", "width": 100},
#         {"label": _("Type"), "fieldname": "type", "width": 120},
#         {"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 100},
#         {"label": _("Payment Mode"), "fieldname": "payment_mode", "width": 120},
#         {"label": _("Resident"), "fieldname": "resident_name", "width": 150},
#         {"label": _("Status"), "fieldname": "paid", "width": 80, "fieldtype": "Check"},
#         {"label": _("Date"), "fieldname": "created", "fieldtype": "Date", "width": 100},
#         {"label": _("Month"), "fieldname": "month", "width": 100}
#     ]

# def get_data(filters):
#     conditions = get_conditions(filters)
    
#     query = """
#         SELECT 
#             name,
#             type,
#             amount,
#             payment_mode,
#             resident_name,
#             paid,
#             created,
#             DATE_FORMAT(created, '%%Y-%%m') as month
#         FROM `tabPayment`
#         WHERE docstatus < 2 {conditions}
#         ORDER BY created, name
#     """.format(conditions=conditions)
    
#     return frappe.db.sql(query, filters, as_dict=1)

# def add_monthly_summary(data):
#     if not data:
#         return data
    
#     monthly_data = {}
#     for payment in data:
#         month = payment.get("month")
#         if month not in monthly_data:
#             monthly_data[month] = {
#                 "payments": [],
#                 "total_amount": 0,
#                 "paid_count": 0,
#                 "pending_count": 0
#             }
        
#         monthly_data[month]["payments"].append(payment)
#         monthly_data[month]["total_amount"] += payment.get("amount", 0)
        
#         if payment.get("paid"):
#             monthly_data[month]["paid_count"] += 1
#         else:
#             monthly_data[month]["pending_count"] += 1
    
#     sorted_data = []
#     for month in sorted(monthly_data.keys()):
#         sorted_data.extend(monthly_data[month]["payments"])
        
#         # Add only monthly summary row
#         sorted_data.append({
#             "name": f"SUMMARY-{month}",
#             "type": f"Monthly Summary ({month})",
#             "amount": monthly_data[month]["total_amount"],
#             "payment_mode": "",
#             "resident_name": f"Paid: {monthly_data[month]['paid_count']} | Pending: {monthly_data[month]['pending_count']}",
#             "paid": "",
#             "created": "",
#             "month": month,
#             "is_summary": True,
#             "indent": 0
#         })
    
#     return sorted_data

# def get_charts(data):
#     # Filter out summary rows
#     payment_data = [d for d in data if not d.get("is_summary")]
    
#     # Chart 1: Payment Status Pie Chart
#     status_counts = {"Paid": 0, "Pending": 0}
#     for payment in payment_data:
#         if payment.get("paid"):
#             status_counts["Paid"] += 1
#         else:
#             status_counts["Pending"] += 1
    
#     status_chart = {
#         "title": "Payment Status Distribution",
#         "data": {
#             "labels": list(status_counts.keys()),
#             "datasets": [{
#                 "name": "Status",
#                 "values": list(status_counts.values())
#             }]
#         },
#         "type": "pie",
#         "height": 200,
#         "colors": ["#28a745", "#ffc107"]
#     }
    
#     # Chart 2: Payment Type Distribution
#     type_data = {}
#     for payment in payment_data:
#         payment_type = payment.get("type") or "Other"
#         if payment_type not in type_data:
#             type_data[payment_type] = 0
#         type_data[payment_type] += payment.get("amount", 0)
    
#     type_chart = {
#         "title": "Payment Amount by Type",
#         "data": {
#             "labels": list(type_data.keys()),
#             "datasets": [{
#                 "name": "Amount",
#                 "values": list(type_data.values())
#             }]
#         },
#         "type": "bar",
#         "height": 200,
#         "colors": ["#743ee2", "#7cd6fd"]
#     }
    
#     return {
#         "data": status_chart,
#         "heatmap": type_chart
#     }

# def get_conditions(filters):
#     conditions = ""
    
#     if filters.get("from_date"):
#         conditions += " AND created >= %(from_date)s"
#     if filters.get("to_date"):
#         conditions += " AND created <= %(to_date)s"
#     if filters.get("type"):
#         conditions += " AND type = %(type)s"
#     if filters.get("payment_mode"):
#         conditions += " AND payment_mode = %(payment_mode)s"
#     if filters.get("paid") is not None:
#         conditions += " AND paid = %(paid)s"
        
#     return conditions



from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import formatdate, getdate

def execute(filters=None):
    columns = get_columns()
    data = get_payment_data(filters)
    summary = get_summary(data)
    
    return columns, data, None, None, summary

def get_columns():
    return [
        {"label": _("Payment ID"), "fieldname": "name", "fieldtype": "Link", "options": "Payment", "width": 120},
        {"label": _("Date"), "fieldname": "created", "fieldtype": "Date", "width": 100},
        {"label": _("Type"), "fieldname": "type", "width": 120},
        {"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 100},
        {"label": _("Mode"), "fieldname": "payment_mode", "width": 100},
        {"label": _("Resident"), "fieldname": "resident_name", "width": 150},
        {"label": _("Status"), "fieldname": "status", "width": 80}
    ]

def get_payment_data(filters):
    conditions = get_conditions(filters)
    
    return frappe.db.sql("""
        SELECT 
            name,
            created,
            type,
            amount,
            payment_mode,
            resident_name,
            IF(paid=1, 'Paid', 'Pending') as status
        FROM `tabPayment`
        WHERE docstatus < 2 {conditions}
        ORDER BY created DESC
    """.format(conditions=conditions), filters, as_dict=1)

def get_summary(data):
    if not data:
        return []
    
    total_amount = sum(d.get('amount', 0) for d in data)
    paid_amount = sum(d.get('amount', 0) for d in data if d.get('status') == 'Paid')
    pending_amount = total_amount - paid_amount
    
    return [
        {"label": "Total Payments", "value": len(data), "indicator": "Blue"},
        {"label": "Total Amount", "value": total_amount, "indicator": "Green"},
        {"label": "Paid Amount", "value": paid_amount, "indicator": "Green"},
        {"label": "Pending Amount", "value": pending_amount, "indicator": "Red"}
    ]

def get_conditions(filters):
    conditions = []
    
    if filters.get("from_date"):
        conditions.append("created >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("created <= %(to_date)s")
    if filters.get("type"):
        conditions.append("type = %(type)s")
    if filters.get("payment_mode"):
        conditions.append("payment_mode = %(payment_mode)s")
    if filters.get("status"):
        conditions.append("paid = %(status)s")
    
    return " AND " + " AND ".join(conditions) if conditions else ""