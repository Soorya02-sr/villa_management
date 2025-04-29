# Copyright (c) 2025, soorya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today
from datetime import timedelta

class Payment(Document):
    def validate(self):
        self.validate_monthly_fund_duplicate()
    
    def validate_monthly_fund_duplicate(self):
        """Validate that a resident doesn't have duplicate Monthly Fund in the same month"""
        if self.type == "Monthly Fund" and self.resident:
            # Get the first and last day of the current month
            current_date = getdate(self.created or today())
            first_day = current_date.replace(day=1)
            last_day = (current_date.replace(day=1, month=current_date.month+1) - 
                       timedelta(days=1))
            
            # Check for existing payments
            existing_payment = frappe.db.exists("Payment", {
                "type": "Monthly Fund",
                "resident": self.resident,
                "created": ["between", [first_day, last_day]],
                "name": ["!=", self.name or ""]
            })
            
            if existing_payment:
                frappe.throw(_(
                    "A Monthly Fund payment for resident {0} already exists for {1} ({2}). "
                    "Please select a different type or resident."
                ).format(
                    frappe.bold(self.resident_name),
                    current_date.strftime("%B %Y"),
                    frappe.bold(existing_payment)
                ))