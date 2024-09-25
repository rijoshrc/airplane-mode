import frappe

def get_context(context):
    
    shops = frappe.get_all(
        "Airport Shop",
        filters={"status": "Available"},
        fields=["name1 as name", "airport", "area", "rent_amount", "photo"],
        order_by="name1 asc"
    )
    
    
    context.shops = shops
    context.title = "Available Shops"
