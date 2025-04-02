# Copyright (c) 2025, soorya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VillaDetails(Document):
    def on_update(self):
        if self.resident:
            resident = frappe.get_doc("Residents Details", self.resident)
            resident.villa_number = self.name
            resident.save()
            
        self.update_resident_community_type()

    def update_resident_community_type(self):
        if self.resident:
            resident = frappe.get_doc("Residents Details", self.resident)
            if self.status == "Rented":
                resident.community_type = "Renter"
            elif self.status == "Sold":
                resident.community_type = "Villa Owner"
            else:
                # Handle other statuses if needed
                resident.community_type = None  # or set a default value

            resident.save()