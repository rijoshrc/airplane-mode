import frappe

def execute(filters=None):
    columns, data = [], []
    
    # Define columns for the report
    columns = [
        {"label": "Airport", "fieldname": "airport", "fieldtype": "Link", "options": "Airport", "width": 200},
        {"label": "Total Rent Collected", "fieldname": "total_rent_collected", "fieldtype": "Currency", "width": 150}
    ]
    
    # Fetch rent collected data from Airport Shop and Rent Payment Doctypes
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

    # Append each airport's data to the report data list
    for record in rent_data:
        data.append({
            "airport": record.airport,
            "total_rent_collected": record.total_rent_collected
        })
    

    return columns, data
