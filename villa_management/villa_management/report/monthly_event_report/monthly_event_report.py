# # # Copyright (c) 2025, soorya and contributors
# # # For license information, please see license.txt

# # import frappe


# from __future__ import unicode_literals
# import frappe
# from frappe import _
# from frappe.utils import formatdate, getdate, nowdate
# from datetime import datetime

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {"label": _("Event ID"), "fieldname": "name", "width": 120},
#         {"label": _("Event Name"), "fieldname": "event_name", "width": 150},
#         {"label": _("Type"), "fieldname": "type", "width": 120},
#         {"label": _("Event Date"), "fieldname": "event_date", "fieldtype": "Date", "width": 100},
#         {"label": _("Total Expected"), "fieldname": "total_expected", "fieldtype": "Currency", "width": 120},
#         {"label": _("Total Actual"), "fieldname": "total_actual", "fieldtype": "Currency", "width": 120},
#         {"label": _("Month"), "fieldname": "month", "width": 100}
#     ]

# def get_data(filters):
#     conditions = get_conditions(filters)
    
#     # Main query for event headers
#     event_query = """
#         SELECT 
#             name,
#             event_name, 
#             type, 
#             event_date,
#             DATE_FORMAT(event_date, '%%Y-%%m') as month
#         FROM `tabEvents`
#         WHERE docstatus < 2 {conditions}
#         ORDER BY event_date
#     """.format(conditions=conditions)
    
#     events = frappe.db.sql(event_query, filters, as_dict=1)
    
#     # Get budget amounts from child table
#     for event in events:
#         budget_items = frappe.get_all("Budget Planning",
#             filters={"parent": event.name},
#             fields=["sum(expected_amount) as total_expected", "sum(actual_amount) as total_actual"],
#             group_by="parent"
#         )
        
#         if budget_items:
#             event.update({
#                 "total_expected": budget_items[0].total_expected or 0,
#                 "total_actual": budget_items[0].total_actual or 0
#             })
#         else:
#             event.update({
#                 "total_expected": 0,
#                 "total_actual": 0
#             })
    
#     return events

# def get_conditions(filters):
#     conditions = ""
    
#     if filters.get("from_date"):
#         conditions += " AND event_date >= %(from_date)s"
#     if filters.get("to_date"):
#         conditions += " AND event_date <= %(to_date)s"
#     if filters.get("type"):
#         conditions += " AND type = %(type)s"
        
#     return conditions


# from __future__ import unicode_literals
# import frappe
# from frappe import _
# from frappe.utils import formatdate, getdate, nowdate
# from datetime import datetime

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
    
#     # Add monthly summary rows
#     data = add_monthly_totals(data)
    
#     return columns, data

# def get_columns():
#     return [
#         {"label": _("Event ID"), "fieldname": "name", "width": 120},
#         {"label": _("Event Name"), "fieldname": "event_name", "width": 150},
#         {"label": _("Type"), "fieldname": "type", "width": 120},
#         {"label": _("Event Date"), "fieldname": "event_date", "fieldtype": "Date", "width": 100},
#         {"label": _("Expected Budget"), "fieldname": "total_expected", "fieldtype": "Currency", "width": 120},
#         {"label": _("Actual Budget"), "fieldname": "total_actual", "fieldtype": "Currency", "width": 120},
#         {"label": _("Variance"), "fieldname": "variance", "fieldtype": "Currency", "width": 120},
#         {"label": _("Month"), "fieldname": "month", "width": 100}
#     ]

# def get_data(filters):
#     conditions = get_conditions(filters)
    
#     # Main query for event headers
#     event_query = """
#         SELECT 
#             name,
#             event_name, 
#             type, 
#             event_date,
#             DATE_FORMAT(event_date, '%%Y-%%m') as month
#         FROM `tabEvents`
#         WHERE docstatus < 2 {conditions}
#         ORDER BY event_date, name
#     """.format(conditions=conditions)
    
#     events = frappe.db.sql(event_query, filters, as_dict=1)
    
#     # Get budget amounts from child table and calculate variance
#     for event in events:
#         budget_items = frappe.get_all("Budget Planning",
#             filters={"parent": event.name},
#             fields=["sum(expected_amount) as total_expected", "sum(actual_amount) as total_actual"],
#             group_by="parent"
#         )
        
#         if budget_items:
#             event.update({
#                 "total_expected": budget_items[0].total_expected or 0,
#                 "total_actual": budget_items[0].total_actual or 0,
#                 "variance": (budget_items[0].total_actual or 0) - (budget_items[0].total_expected or 0)
#             })
#         else:
#             event.update({
#                 "total_expected": 0,
#                 "total_actual": 0,
#                 "variance": 0
#             })
    
#     return events

# def add_monthly_totals(data):
#     if not data:
#         return data
    
#     # Group by month
#     monthly_data = {}
#     for event in data:
#         month = event.get("month")
#         if month not in monthly_data:
#             monthly_data[month] = {
#                 "events": [],
#                 "total_expected": 0,
#                 "total_actual": 0,
#                 "total_variance": 0
#             }
        
#         monthly_data[month]["events"].append(event)
#         monthly_data[month]["total_expected"] += event.get("total_expected", 0)
#         monthly_data[month]["total_actual"] += event.get("total_actual", 0)
#         monthly_data[month]["total_variance"] += event.get("variance", 0)
    
#     # Create new list with monthly totals
#     sorted_data = []
#     for month in sorted(monthly_data.keys()):
#         # Add all events for the month
#         sorted_data.extend(monthly_data[month]["events"])
        
#         # Add monthly total row
#         sorted_data.append({
#             "name": f"TOTAL-{month}",
#             "event_name": f"Monthly Total ({month})",
#             "type": "",
#             "event_date": "",
#             "total_expected": monthly_data[month]["total_expected"],
#             "total_actual": monthly_data[month]["total_actual"],
#             "variance": monthly_data[month]["total_variance"],
#             "month": month,
#             "is_total": True,
#             "indent": 0
#         })
    
#     return sorted_data

# def get_conditions(filters):
#     conditions = ""
    
#     if filters.get("from_date"):
#         conditions += " AND event_date >= %(from_date)s"
#     if filters.get("to_date"):
#         conditions += " AND event_date <= %(to_date)s"
#     if filters.get("type"):
#         conditions += " AND type = %(type)s"
        
#     return conditions


# from __future__ import unicode_literals
# import frappe
# from frappe import _
# from frappe.utils import formatdate, getdate, nowdate
# from datetime import datetime

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
    
#     # Add monthly summary rows
#     data = add_monthly_totals(data)
    
#     # Prepare chart data
#     chart = get_chart_data(data)
    
#     return columns, data, None, chart

# def get_columns():
#     return [
#         {"label": _("Event ID"), "fieldname": "name", "width": 120},
#         {"label": _("Event Name"), "fieldname": "event_name", "width": 150},
#         {"label": _("Type"), "fieldname": "type", "width": 120},
#         {"label": _("Event Date"), "fieldname": "event_date", "fieldtype": "Date", "width": 100},
#         {"label": _("Expected Budget"), "fieldname": "total_expected", "fieldtype": "Currency", "width": 120},
#         {"label": _("Actual Budget"), "fieldname": "total_actual", "fieldtype": "Currency", "width": 120},
#         {"label": _("Variance"), "fieldname": "variance", "fieldtype": "Currency", "width": 120},
#         {"label": _("Month"), "fieldname": "month", "width": 100}
#     ]

# def get_data(filters):
#     conditions = get_conditions(filters)
    
#     # Main query for event headers
#     event_query = """
#         SELECT 
#             name,
#             event_name, 
#             type, 
#             event_date,
#             DATE_FORMAT(event_date, '%%Y-%%m') as month
#         FROM `tabEvents`
#         WHERE docstatus < 2 {conditions}
#         ORDER BY event_date, name
#     """.format(conditions=conditions)
    
#     events = frappe.db.sql(event_query, filters, as_dict=1)
    
#     # Get budget amounts from child table and calculate variance
#     for event in events:
#         budget_items = frappe.get_all("Budget Planning",
#             filters={"parent": event.name},
#             fields=["sum(expected_amount) as total_expected", "sum(actual_amount) as total_actual"],
#             group_by="parent"
#         )
        
#         if budget_items:
#             event.update({
#                 "total_expected": budget_items[0].total_expected or 0,
#                 "total_actual": budget_items[0].total_actual or 0,
#                 "variance": (budget_items[0].total_actual or 0) - (budget_items[0].total_expected or 0)
#             })
#         else:
#             event.update({
#                 "total_expected": 0,
#                 "total_actual": 0,
#                 "variance": 0
#             })
    
#     return events

# def add_monthly_totals(data):
#     if not data:
#         return data
    
#     # Group by month
#     monthly_data = {}
#     for event in data:
#         month = event.get("month")
#         if month not in monthly_data:
#             monthly_data[month] = {
#                 "events": [],
#                 "total_expected": 0,
#                 "total_actual": 0,
#                 "total_variance": 0
#             }
        
#         monthly_data[month]["events"].append(event)
#         monthly_data[month]["total_expected"] += event.get("total_expected", 0)
#         monthly_data[month]["total_actual"] += event.get("total_actual", 0)
#         monthly_data[month]["total_variance"] += event.get("variance", 0)
    
#     # Create new list with monthly totals
#     sorted_data = []
#     for month in sorted(monthly_data.keys()):
#         # Add all events for the month
#         sorted_data.extend(monthly_data[month]["events"])
        
#         # Add monthly total row
#         sorted_data.append({
#             "name": f"TOTAL-{month}",
#             "event_name": f"Monthly Total ({month})",
#             "type": "",
#             "event_date": "",
#             "total_expected": monthly_data[month]["total_expected"],
#             "total_actual": monthly_data[month]["total_actual"],
#             "variance": monthly_data[month]["total_variance"],
#             "month": month,
#             "is_total": True,
#             "indent": 0
#         })
    
#     return sorted_data

# def get_chart_data(data):
#     # Filter out the monthly total rows
#     event_data = [d for d in data if not d.get("is_total")]
    
#     # Group by event type
#     type_data = {}
#     for event in event_data:
#         event_type = event.get("type") or "Uncategorized"
#         if event_type not in type_data:
#             type_data[event_type] = 0
#         type_data[event_type] += 1
    
#     # Prepare chart data
#     chart = {
#         "data": {
#             "labels": list(type_data.keys()),
#             "datasets": [{
#                 "name": "Event Types",
#                 "values": list(type_data.values())
#             }]
#         },
#         "type": "pie",
#         "height": 300,
#         "colors": ["#7cd6fd", "#743ee2", "#ff5858", "#ffa00a", "#feef72", "#28a745", "#98d85b"],
#         "title": "Distribution of Events by Type"
#     }
    
#     return chart

# def get_conditions(filters):
#     conditions = ""
    
#     if filters.get("from_date"):
#         conditions += " AND event_date >= %(from_date)s"
#     if filters.get("to_date"):
#         conditions += " AND event_date <= %(to_date)s"
#     if filters.get("type"):
#         conditions += " AND type = %(type)s"
        
#     return conditions


from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_event_data(filters)
    data = add_monthly_summary(data)
    chart = get_chart_data(data)
    summary = get_report_summary(data)
    
    return columns, data, None, chart, summary

def get_columns():
    return [
        {"label": _("Event ID"), "fieldname": "name", "fieldtype": "Link", "options": "Events", "width": 120},
        {"label": _("Event Name"), "fieldname": "event_name", "width": 150},
        {"label": _("Type"), "fieldname": "type", "width": 120},
        {"label": _("Date"), "fieldname": "event_date", "fieldtype": "Date", "width": 100},
        {"label": _("Expected"), "fieldname": "expected_budget", "fieldtype": "Currency", "width": 100},
        {"label": _("Actual"), "fieldname": "actual_budget", "fieldtype": "Currency", "width": 100},
        {"label": _("Variance"), "fieldname": "variance", "fieldtype": "Currency", "width": 100},
        {"label": _("Status"), "fieldname": "status", "width": 80}
    ]

def get_event_data(filters):
    conditions = get_conditions(filters)
    
    # Get all events with their budget data in a single query
    events = frappe.db.sql(f"""
        SELECT 
            e.name,
            e.event_name,
            e.type,
            e.event_date,
            DATE_FORMAT(e.event_date, '%%Y-%%m') as month,
            IF(e.event_date >= CURDATE(), 'Upcoming', 'Completed') as status,
            COALESCE(SUM(b.expected_amount), 0) as expected_budget,
            COALESCE(SUM(b.actual_amount), 0) as actual_budget,
            COALESCE(SUM(b.actual_amount - b.expected_amount), 0) as variance
        FROM `tabEvents` e
        LEFT JOIN `tabBudget Planning` b ON b.parent = e.name
        WHERE e.docstatus < 2 {conditions}
        GROUP BY e.name
        ORDER BY e.event_date DESC
    """.format(conditions=conditions), filters, as_dict=1)
    
    return events

def add_monthly_summary(data):
    if not data:
        return data
    
    monthly_data = {}
    for event in data:
        month = event.get("month")
        if month not in monthly_data:
            monthly_data[month] = {
                "events": [],
                "total_expected": 0,
                "total_actual": 0,
                "total_variance": 0
            }
        
        monthly_data[month]["events"].append(event)
        monthly_data[month]["total_expected"] += event.get("expected_budget", 0)
        monthly_data[month]["total_actual"] += event.get("actual_budget", 0)
        monthly_data[month]["total_variance"] += event.get("variance", 0)
    
    sorted_data = []
    for month in sorted(monthly_data.keys()):
        sorted_data.extend(monthly_data[month]["events"])
        
        sorted_data.append({
            "name": f"TOTAL-{month}",
            "event_name": f"Monthly Total ({month})",
            "expected_budget": monthly_data[month]["total_expected"],
            "actual_budget": monthly_data[month]["total_actual"],
            "variance": monthly_data[month]["total_variance"],
            "is_total": True,
            "indent": 0
        })
    
    return sorted_data

def get_chart_data(data):
    # Filter out summary rows
    event_data = [d for d in data if not d.get("is_total")]
    
    type_data = {}
    for event in event_data:
        event_type = event.get("type") or "Uncategorized"
        if event_type not in type_data:
            type_data[event_type] = 0
        type_data[event_type] += event.get("expected_budget", 0)
    
    return {
        "data": {
            "labels": list(type_data.keys()),
            "datasets": [{
                "name": "Budget by Type",
                "values": list(type_data.values())
            }]
        },
        "type": "pie",
        "height": 300,
        "colors": ["#7cd6fd", "#743ee2", "#ff5858", "#ffa00a", "#28a745"],
        "title": "Budget Distribution by Event Type"
    }

def get_report_summary(data):
    if not data:
        return []
    
    event_data = [d for d in data if not d.get("is_total")]
    total_events = len(event_data)
    total_expected = sum(d.get("expected_budget", 0) for d in event_data)
    total_actual = sum(d.get("actual_budget", 0) for d in event_data)
    total_variance = total_actual - total_expected
    
    return [
        {"label": "Total Events", "value": total_events, "indicator": "Blue"},
        {"label": "Total Expected", "value": total_expected, "indicator": "Green"},
        {"label": "Total Actual", "value": total_actual, "indicator": "Green" if total_actual >= total_expected else "Red"},
        {"label": "Total Variance", "value": total_variance, "indicator": "Green" if total_variance >= 0 else "Red"}
    ]

def get_conditions(filters):
    conditions = []
    
    if filters.get("from_date"):
        conditions.append("e.event_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("e.event_date <= %(to_date)s")
    if filters.get("type"):
        conditions.append("e.type = %(type)s")
    
    return " AND " + " AND ".join(conditions) if conditions else ""