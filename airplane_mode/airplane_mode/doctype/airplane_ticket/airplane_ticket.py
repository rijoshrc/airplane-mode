# Copyright (c) 2024, Rijosh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
import random


class AirplaneTicket(Document):
	def before_validate(self):
		self.remove_duplicates()
		self.calculate_total_price()
		
	
	def remove_duplicates(self):
		unique_add_ons = []
		seen_identifiers = set()
		for add_on in self.get('add_ons'):
			identifier = add_on.item
			if identifier not in seen_identifiers:
				seen_identifiers.add(identifier)
				unique_add_ons.append(add_on)
		self.set('add_ons', unique_add_ons)


	def calculate_total_price(self):
		self.total_price = 0
		for add_on in self.add_ons:
			self.total_price += add_on.amount

		self.total_amount = self.flight_price + self.total_price		
		

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("Cannot submit Airplane Ticket unless status is 'Boarded'.")


	def before_insert(self):
		self.assign_seat()
	
	def assign_seat(self):
		random_number = random.randint(1, 100)
		random_letter = random.choice(["A","B","C","D","E"])
		self.seat = f"{random_number}{random_letter}"

	def on_submit(self):
		airplane_flight = frappe.get_doc("Airplane Flight", self.flight)
		airplane_flight.status = "Completed"
		airplane_flight.save()

	def validate(self):
		airplane_capacity = 0

		flight = self.flight
		flight_doc = frappe.get_doc("Airplane Flight", flight)
		airplane = flight_doc.airplane

		if airplane:
			airplane_doc = frappe.get_doc("Airplane", airplane)
			airplane_capacity = airplane_doc.capacity

		ticket_count = frappe.db.count("Airplane Ticket", {"flight": flight})
		if ticket_count >= airplane_capacity:
			frappe.throw("Airplane is full. Please select another flight.")


	pass



		# print(self.status)
		# print(self.as_dict())
		# frappe.throw(self.status)