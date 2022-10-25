# CommonModel

**An open standard for describing structured data**

CommonModel is an open specification for describing the structure and semantics
of objects and their data representations, called `Schemas` -- a universal format for modeling the world's data.

APIs, libraries, researchers, and analysts can use CommonModel to communicate
data structure and properties when publishing api endpoints, aggregating ML training data,
curating public datasets, or building composable data components.


Some example Schemas:

- Country
- Currency
- Date
- Transaction
- Customer
- Address
- PhoneNumber
- EndOfDayPrice

and for third-party data:

- WorldBankCountryIndicator
- StripeCharge
- FredObservation
- ShopifyOrder
- MailchimpMember
- SalesforceCustomer

## Spec

A CommonModel Schema provides a single place to describe the properties of an abstract object, its data types, its relation to other objects, and provide documentation on the details of each. A basic Schema looks like this:

```yaml
commonmodel: 0.3.0

name: Transaction
description: |
  Represents a transaction of an amount at a
  given time, optionally specifying the buyer, seller, currency, and item transacted.
immutable: true
unique_on:
  - id
fields:
  id: Text
  amount: Decimal(16,2)
  transacted_at: DateTime
  buyer_id: Text
  seller_id: Text
  item_id: Text
  currency_code: Text
  metadata: Json
field_roles:
  primary_identifier: id
  created_ordering: transacted_at
  dimensions: [buyer_id, seller_id, item_id]
  measures: [amount]

documentation:
  schema: |
    A Transaction is meant to be the broadest, most base definition
    for all commercial transactions involving a buyer and a seller or a sender
    and receiver, whether that's an ecommerce order, a ACH transfer, or a real
    estate sale.
  fields:
    id: |
      Unique identifier for this transaction, required so that transactions can
      be safely de-duplicated. If data does not have a unique identifier, either
      create one, or use a more basic schema like `common.Measurement`.
```
