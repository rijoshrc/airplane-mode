import frappe

def execute(filters=None):
    columns, data = [], []
    
    
    columns = [
        {"label": "Airport", "fieldname": "airport", "fieldtype": "Link", "options": "Airport", "width": 200},
        {"label": "Total Rent Collected", "fieldname": "total_rent_collected", "fieldtype": "Currency", "width": 150}
    ]
    
    
    rent_data = frappe.db.sql("""
        SELECT 
            shop.airport AS airport,
            IFNULL(SUM(payment.rent_amount), 0) AS total_rent_collected
        FROM 
            `tabAirport Shop` AS shop
        LEFT JOIN 
            `tabRent Payment` AS payment ON payment.shop = shop.name AND payment.status = 'Paid'
        GROUP BY 
            shop.airport
        ORDER BY 
            shop.airport
    """, as_dict=True)

    
    for record in rent_data:
        data.append({
            "airport": record.airport,
            "total_rent_collected": record.total_rent_collected
        })

    
    chart_data = {
        "data": {
            "labels": [record['airport'] for record in rent_data],
            "datasets": [
                {
                    "name": "Total Rent Collected",
                    "values": [record['total_rent_collected'] for record in rent_data]
                }
            ]
        },
        "type": "bar",  # You can change this to 'line' or 'pie' based on your preference
        "title": "Rent Collected from Each Airport",
        "colors": ["#3498db"]  # Customize the bar color if needed
    }

    return columns, data, None, chart_data
