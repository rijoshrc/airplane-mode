# Airport Shop Management

## Doctypes

1. Airport Shop

   Naming: Expression - SHOP-{Airport Code}-{###}

   - Name: Data, Mandatory
   - Area (sq ft): Float, Mandatory
   - Airport: Link, Airport
   - Tenant: Link, Tenant
   - Status: Select, (Available, Occupied)
   - Rent Amount: Currency, Mandatory
   - Contract: Link, Shop Lease Contract
   - Contract Start Date: Date, Read only, fetch from Contract
   - Contract Expiry Date: Date, Read only, fetch from Contract

2. Tenant

   Naming: User select

   - Name: Data, Mandatory
   - Email: Data, Email
   - Phone Number: Data, Phone
   - Address: Data
   - Image

3. Rent Payment - Submittable

   Naming: Expression {mm-yy}-{####}

   - Payment Date: Date, Mandatory
   - Tenant: Link, Tenant
   - Shop: Link, Shop
   - Rent Amount: Currency, Fetch from Shop
   - Status: Select, (Pending, Paid)

4. Shop Lease Contract

   Naming: Expression CT-{shop}-{YY}-{###}

   - Shop: Link, Shop, Mandatory
   - Tenant: Link, Tenant, Mandatory
   - Contract Start Date: Date
   - Contract Expiry Date: Date
   - Monthly Rent: Currency, fetch from Shop
   - Status: Select (Active, Expired, Terminated)

5. Shop Rent Config - Single

   - Rent Amount: Currency
   - Enable Reminder: Checkbox
