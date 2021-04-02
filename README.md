![schemas](https://github.com/kvh/schemas/workflows/schemas-python/badge.svg)

# Semantic Schemas

# Common Schema

Semantic Schemas are a universal format for specifying the structure and semantics of data, record, and object types. Think supercharged "CREATE TABLE" statement or JSON spec. The goal of Semantic Schemas is to provide a universal library of common Schemas that tools, libraries, researchers, analysts, databases, and APIs can use to communicate data frictionlessly. Semantic Schemas are a data protocol for the next 70,000 years.

The Semantic Schema Repository has many common schemas like:

- Country
- Currency
- Date
- Transaction
- Customer
- Address
- PhoneNumber
- EndOfDayPrice

and popular third-party ones like:

- StripeCharge
- FredObservation
- ShopifyOrder
- WorldBankCountryIndicator
- MailchimpMember
- SalesforceCustomer

Semantic Schemas provide a single place to describe the properties of an abstract object, its attributes and their types, its relation to other objects, and provide documentation of the meaning and details of each. A basic Schema looks like this:

```yaml
name: Transaction
version: 1
description: |
  Represents a transaction of an amount at a given time, optionally
  specifying the buyer, seller, currency, and item transacted as well.
immutable: true
unique_on:
  - id
fields:
  id: Text NotNull
  amount: Decimal(16,2) NotNull
  transacted_at: DateTime NotNull
  buyer_id: Text
  seller_id: Text
  item_id: Text
  currency_code: Text
relations:
  Currency:
    fields:
      code: currency_code
implementations:
  TimeSeries:
    time: transacted_at
    value: amount
```

```toml
name = Transaction
version = 1
description = """\
  Represents a transaction of an amount at a given time, optionally
  specifying the buyer, seller, currency, and item transacted as well.
  """
immutable = true
unique_on = ["id"]

[fields]
id = "Text NotNull"
amount = {type = "Decimal(16,2)", validators = ["NotNull"]}
transacted_at = "DateTime NotNull"
buyer_id = "Text"
seller_id = "Text"

[relations.Currency.fields]
code = "currency_code"

[implementations.TimeSeries]
time = "transacted_at"
value = "amount"
```
