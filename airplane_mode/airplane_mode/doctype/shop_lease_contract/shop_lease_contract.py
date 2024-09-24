# Copyright (c) 2024, Rijosh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class ShopLeaseContract(Document):


	# if the shop is not available then throw an error
	def validate(self):
		shop = frappe.get_doc("Airport Shop", self.shop)
		if not shop.status == "Available":
			frappe.throw("Shop is not available")
	

	
	def on_submit(self):
		self.update_status_and_tenant()


	def before_update_after_submit(self):
		if not self.status == "Active":
			frappe.db.set_value("Airport Shop", self.shop, "status","Available")
		else:
			frappe.db.set_value("Airport Shop", self.shop, "status","Occupied")
	

	# release shop on canceling the contract
	def on_cancel(self):
		frappe.db.set_value("Airport Shop", self.shop, "status","Available")
		


	# update shop status to Occupied and doc status to Active
	# update the tenant with the doc tenant
	def update_status_and_tenant(self):
		self.status = "Active"
		frappe.db.set_value("Airport Shop", self.shop, "status","Occupied")
		frappe.db.set_value("Airport Shop", self.shop, "tenant",self.tenant)

	pass
