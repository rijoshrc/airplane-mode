# Copyright (c) 2024, Rijosh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShop(Document):
	def validate(self):
		if not self.rent_amount:
			rent_config = frappe.get_doc("Shop Rent Configuration")
			self.rent_amount = rent_config.default_rent_amount

			
	pass
