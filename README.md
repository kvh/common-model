![commonmodel-python](https://github.com/kvh/commonmodel/workflows/commonmodel-python/badge.svg)

# Common Model

**A data protocol for the next 70,000 years.**

Common Model is a shared specification for describing the structure and semantics
of objects and their data representations -- a "lingua franca"
of data. In practice, think supercharged "CREATE TABLE" statement or JSON spec.

Anyone can contribute Schemas to the Common Model Repository and help build
a shared global model of data that tools, libraries, researchers, analysts, databases,
and apis can use to communicate data frictionlessly.

Whether it's publishing
or consuming API endpoints, aggregating ML training data, or curating public
research datasets, Common Model enables global collaboration on data.

The Common Model Repository has core Schemas like:

- Country
- Currency
- Date
- Transaction
- Customer
- Address
- PhoneNumber
- EndOfDayPrice

and popular third-party ones like:

- WorldBankCountryIndicator
- StripeCharge
- FredObservation
- ShopifyOrder
- MailchimpMember
- SalesforceCustomer

A Common Model Schema provides a single place to describe the properties of an abstract object, its attributes and their types, its relation to other objects, and provide documentation on the details of each. A basic Schema looks like this:

```yaml
commonmodel: 0.3.0

name: Transaction
namespace: common
version: 0.1.0
description: |
  Represents any commercial transaction of a set amount at a given time, optionally
  specifying the buyer, seller, currency, and item transacted.
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
  metadata: Json
relations:
  common.Currency:
    fields:
      code: currency_code
implementations:
  common.TimeSeries:
    time: transacted_at
    value: amount

documentation:
  schema: |
    A Transaction is meant to be the broadest, most base definition
    for all commercial transactions involving a buyer and a seller or a sender
    and receiver, whether that's an ecommerce order, a ACH transfer, or a real
    estate sale.
  fields:
    id: |
      Unique identifier for this transaction, required so that transactions can
      be deduped accurately. If data does not have a unique identifier, either
      create one, or use a more basic schema like `common.TimeSeries`.
```

## Versioning

Schemas follow semantic versioning conventions, meaning that breaking (backwards
incompatible) changes require a major version bump, new backwards
compatible features require a minor version bump, and bug fixes can be a patch
version bump.

Examples of backwards **incompatible** changes requiring major version bump:

- Add a new NotNull field
- Change an existing field type to a more restrictive type (Float -> Integer)
- Rename a field
- Change unique fields
- Remove or change relations or implementations
- Make immutable

Examples of backwards **compatible** changes requiring minor version bump:

- Add a new nullable field
- Change an existing field type to a less restrictive type (Text -> LongText, Integer -> Decimal)
- Change the semantic meaning of a field or schema
- Add new relations or implementations

Examples of fixes requiring a patch version bump:

- Edit the documentation or description
- Fix typo or other bug
