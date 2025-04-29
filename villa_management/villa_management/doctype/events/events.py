# Copyright (c) 2025, soorya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class Events(Document):
    def validate(self):
        """Automatically calculate Expected and Actual Budget when the document is saved."""
        self.calculate_budget()

    def calculate_budget(self):
        """Compute total expected and actual budget from budget planning child table."""
        expected_total = 0
        actual_total = 0

        if self.budget_planning:
            for row in self.budget_planning:
                expected_total += row.expected_amount if row.expected_amount else 0
                actual_total += row.actual_amount if row.actual_amount else 0

        # Set the values in the main document
        self.expected_budget = expected_total
        self.actual_budget = actual_total



    

