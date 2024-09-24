# Copyright (c) 2024, Rijosh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):

	def before_submit(self):
		self.status = "Paid"



	def on_submit(self):
		if not self.status == "Paid":
			frappe.throw("Update the status to Paid")

	pass
