# Copyright (c) 2024, Rijosh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import Field
from frappe.query_builder.functions import Sum


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	chart = get_chart(data)
      
	if not data:
		chart = None

	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
		},
		{
			"label": _("Revenue"),
			"fieldname": "revenue",
			"fieldtype": "Currency",
		},
	]


def get_data() -> list[dict]:
    """Return data for the report."""
    airlines = frappe.get_all("Airline", fields=["name"])

    data = []

    # Define the DocTypes
    AirplaneTicket = frappe.qb.DocType("Airplane Ticket")
    AirplaneFlight = frappe.qb.DocType("Airplane Flight")
    Airplane = frappe.qb.DocType("Airplane")

    # Use a dictionary to store total revenue per airline to avoid duplication
    airline_revenue = {}

    for airline in airlines:
        # Construct the revenue query using frappe query builder
        revenue_query = (
            frappe.qb.from_(AirplaneTicket)
            .join(AirplaneFlight)
            .on(AirplaneTicket.flight == AirplaneFlight.name)
            .join(Airplane)
            .on(AirplaneFlight.airplane == Airplane.name)
            .where(Airplane.airline == airline["name"])
            .select(Sum(AirplaneTicket.total_amount).as_("total_revenue"))
        )

        # Execute the query using frappe.db.sql
        revenue_result = frappe.db.sql(revenue_query.get_sql(), as_dict=True)
        revenue = revenue_result[0].total_revenue if revenue_result and revenue_result[0].total_revenue else 0

        # Append each row to data
        data.append({
            "airline": airline["name"],
            "revenue": revenue
        })

        # Store the revenue for total calculation
        airline_revenue[airline["name"]] = revenue


    return data


def get_chart(data):
    chart = {
        "data": {
            "labels": [row["airline"] for row in data],
            "datasets": [{"values": [row["revenue"] for row in data]}],
        },
        "type": "donut",  # Set chart type as donut
        "height": 300,
    }
    return chart


def get_report_summary(data):
	total_revenue = sum([row["revenue"] for row in data])
	return [{
        "value": total_revenue,
        "indicator": "Green",
        "label": _("Total Revenue"),
        "datatype": "Currency",
	}]