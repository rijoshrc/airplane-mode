# Copyright (c) 2024, Rijosh and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator
import random
import frappe


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.status = "Completed"


	def before_validate(self):
		self.remove_duplicates()

	def before_insert(self):
		self.assign_gate_number()

	def on_submit(self):
		self.update_ticket_gate_numbers()

	def before_update_after_submit(self):
		self.update_ticket_gate_numbers()
		
	
	def update_ticket_gate_numbers(self):
		tickets = frappe.get_all("Airplane Ticket", filters={"flight": self.name})
		for ticket in tickets:
			frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", self.gate_number)
		

	def assign_gate_number(self):
		random_number = random.randint(1, 20)
		self.gate_number = f"TG-{random_number}"


	def remove_duplicates(self):
		unique_crew_members = []
		seen_identifiers = set()
		for member in self.get('crew_members'):
			identifier = member.name1
			if identifier not in seen_identifiers:
				seen_identifiers.add(identifier)
				unique_crew_members.append(member)
		self.set('crew_members', unique_crew_members)
	pass
