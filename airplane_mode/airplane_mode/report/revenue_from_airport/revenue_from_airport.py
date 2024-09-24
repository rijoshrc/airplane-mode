import frappe
from datetime import datetime

def execute(filters=None):
    print(filters)
    columns, data = [], []
    
    # Define the filter for the report
    if not filters:
        filters = {}
        
    current_year = datetime.now().year
    
    # Set the year filter from the filters dictionary, or default to the current year
    selected_year = filters.get("year", current_year)
    
    # Define the filters for the report UI
    filters_meta = [
        {
            "fieldname": "year",
            "label": "Year",
            "fieldtype": "Int",
            "default": current_year,
            "reqd": 1  # Make it mandatory if required
        }
    ]
    
    # Define the columns for the report
    columns = [
        {"label": "Airport", "fieldname": "airport", "fieldtype": "Link", "options": "Airport", "width": 200},
        {"label": "Total Rent Collected", "fieldname": "total_rent_collected", "fieldtype": "Currency", "width": 150}
    ]
    
    # Fetch rent collected data for the specified year
    rent_data = frappe.db.sql("""
        SELECT 
            shop.airport AS airport,
            IFNULL(SUM(payment.rent_amount), 0) AS total_rent_collected
        FROM 
            `tabAirport Shop` AS shop
        LEFT JOIN 
            `tabRent Payment` AS payment ON payment.shop = shop.name 
            AND payment.status = 'Paid' 
            AND YEAR(payment.payment_date) = %s
        GROUP BY 
            shop.airport
        ORDER BY 
            shop.airport
    """, (selected_year,), as_dict=True)

    # Append each airport's data to the report data list
    for record in rent_data:
        data.append({
            "airport": record.airport,
            "total_rent_collected": record.total_rent_collected
        })

    # Generate chart data from the same rent_data results
    chart_data = {
        "data": {
            "labels": [record['airport'] for record in rent_data],
            "datasets": [
                {
                    "name": f"Total Rent Collected ({selected_year})",
                    "values": [record['total_rent_collected'] for record in rent_data]
                }
            ]
        },
        "type": "bar",  # You can change this to 'line' or 'pie' based on your preference
        "title": f"Rent Collected from Each Airport in {selected_year}",
        "colors": ["#3498db"]  # Customize the bar color if needed
    }

    return columns, data, filters_meta, chart_data
