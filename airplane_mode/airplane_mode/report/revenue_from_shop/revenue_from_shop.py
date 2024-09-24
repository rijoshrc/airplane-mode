import frappe

def execute(filters=None):
    columns, data = [], []
    
    columns = [
        {"label": "Airport Code", "fieldname": "airport_code", "fieldtype": "Data", "width": 120},
        {"label": "Airport", "fieldname": "airport", "fieldtype": "Link", "options": "Airport", "width": 180},
        {"label": "Shop", "fieldname": "shop", "fieldtype": "Link", "options": "Airport Shop", "width": 120},
        {"label": "Shop Name", "fieldname": "shop_name", "fieldtype": "Data", "width": 180},
        {"label": "Monthly Rent Amount", "fieldname": "rent_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Total Rent Collected", "fieldname": "total_rent_collected", "fieldtype": "Currency", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

    rent_data = frappe.db.sql("""
        SELECT 
            shop.airport_code AS airport_code,
            shop.airport AS airport,
            shop.name AS shop,  -- Using 'name' as the link to the shop
            shop.name1 AS shop_name,  -- Fetching the shop name field
            shop.rent_amount AS rent_amount,
            shop.status AS status,
            IFNULL(SUM(payment.rent_amount), 0) AS total_rent_collected
        FROM 
            `tabAirport Shop` AS shop
        LEFT JOIN 
            `tabRent Payment` AS payment ON payment.shop = shop.name AND payment.status = 'Paid'
        GROUP BY 
            shop.airport, shop.name
        ORDER BY 
            shop.airport, shop.name
    """, as_dict=True)

    
    for record in rent_data:
        data.append({
            "airport_code": record.airport_code,
            "airport": record.airport,
            "shop": record.shop,
            "shop_name": record.shop_name,
            "rent_amount": record.rent_amount,
            "total_rent_collected": record.total_rent_collected,
            "status": record.status
        })

    return columns, data
