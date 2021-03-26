# Semantic Schemas

Semantic Schemas is a universal format for specifying the structure and semantics of datasets, record, and object types. Think supercharged "CREATE TABLE" statement or JSON spec. The goal is to provide a universal library of common Schemas that all tools, libraries, researchers, analysts, databases, and APIs can use to communicate data -- a data protocol for the next 70,000 years. The current library has hundreds of standard and popular schemas, including common ones like Country, Currency, Date, Transaction, Customer, Address, PhoneNumber and popular third-party ones like StripeCharge, ShopifyOrder, EndOfDayPrice, HlocvPrice, etc.

Semantic Schemas provide a single place to summarize the properties of an abstract object and its attributes and their types, its relation to other objects, and documentation of the meaning and details of each. A basic Schema looks like this:

```yaml
name: Transaction
version: 1
description: Represents a transaction of an amount at a given time, optionally specifying the transactor, currency, item transacted as well.
unique_on:
  - id
immutable: true
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

The real power of Schemas though lies in its supporting libraries in various languages that power high-performance datatype and schema conversion, inference, and casting across dozens of formats and storage engines, such as:

- JSON
- CSV
- Pandas dataframe
- Apache Arrow table
- Database table

And storage engines such as:

- Postgres database
- Local filesystem
- In-memory
- S3
