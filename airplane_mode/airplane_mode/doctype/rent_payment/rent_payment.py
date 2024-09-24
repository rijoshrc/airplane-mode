# Copyright (c) 2024, Rijosh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):

	
	def validate(self):
		if self.shop:
			shop = frappe.get_doc("Airport Shop", self.shop)
			if not shop.status == "Occupied":
				frappe.throw("Shop is not occupied")


		if not self.tenant:
			frappe.throw("Tenant is required")
		

	def before_submit(self):
		self.status = "Paid"



	def on_submit(self):
		if not self.status == "Paid":
			frappe.throw("Update the status to Paid")

	pass
