import frappe
from frappe.utils import getdate, add_months, today, formatdate

def send_rent_reminders():
    # Get the first day of the current month
    current_date = today()
    start_date = getdate(current_date).replace(day=1)
    
    # Fetch tenants with active contracts
    tenants = frappe.db.sql("""
        SELECT 
            tenant.email AS email,
            tenant.phone_number AS phone_number,
            tenant.address AS address,
            shop.name1 AS shop_name,
            shop.rent_amount AS rent_amount,
            shop.contract_expiry_date AS contract_expiry_date,
            shop.airport AS airport
        FROM 
            `tabTenant` tenant
        JOIN 
            `tabAirport Shop` shop ON tenant.name = shop.tenant
        WHERE 
            shop.status = 'Occupied'
            AND (shop.contract_expiry_date IS NULL OR shop.contract_expiry_date >= %s)
    """, (start_date,), as_dict=True)
    
    
    # Check if there are any tenants to notify
    if not tenants:
        return
    
    # Loop through each tenant and send a reminder email
    for tenant in tenants:
        # Construct the email message
        email_subject = f"Monthly Rent Reminder for Shop {tenant.shop_name} at {tenant.airport}"
        email_message = f"""
            <p>Dear Tenant,</p>
            <p>This is a friendly reminder that your rent payment for the shop <b>{tenant.shop_name}</b> at <b>{tenant.airport}</b> is due for this month.</p>
            <p>The monthly rent amount is <b>{frappe.utils.fmt_money(tenant.rent_amount)}</b>.</p>
            <p>Please ensure the payment is made before the end of this month.</p>
            <p>If you have any questions, feel free to contact us.</p>
            <p>Best regards,</p>
            <p>Airport Management</p>
        """
        
        # Send the email
        # frappe.sendmail(
        #     recipients=[tenant.email],
        #     subject=email_subject,
        #     message=email_message
        # )

        print(tenant.email)

        frappe.log_error(f"Rent reminder sent to {tenant.email}", "Rent Reminder")

    frappe.msgprint(f"Sent rent reminders to {len(tenants)} tenants.")
