import frappe
from frappe.utils import formatdate


def get_context(context):
    context.flights = get_flights()
    return context


def get_flights():
    return frappe.get_all("Airplane Flight",fields=["airplane","source_airport_code","destination_airport_code","date_of_departure","time_of_departure","duration"])
