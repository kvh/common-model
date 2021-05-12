![commonmodel-python](https://github.com/kvh/common-model/workflows/commonmodel-python/badge.svg)

# CommonModel

**A taxonomy of everything**

CommonModel is a shared specification for describing the structure and semantics
of objects and their data representations -- a "lingua franca"
for modeling the world's data. In practice, think supercharged
"CREATE TABLE" statement.

APIs, libraries, researchers, and analysts can use CommonModel to communicate
data frictionlessly when publishing api endpoints, aggregating ML training data,
curating public datasets, or building composable data components.

<!--
As an example, the Common Model Repository defines a `WorldBankCountryIndicator` schema
that conforms to data from the Worldbank api endpoint for country indicators. Here is
an abbreviated snippet of that schema -->

Some example common Schemas:

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
namespace: common
version: 0.1.0
description: |
  Represents any uniquely identified commercial transaction of a set amount at a
  given time, optionally specifying the buyer, seller, currency, and item transacted.
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
field_roles:
  creation_ordering: transacted_at
  primary_dimensions: [buyer_id, seller_id, item_id]
  primary_measures: [amount]

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

Examples of changes that are not allowed as a version and will be a new Schema:

- Change the name of a schema
- Change the namespace of a schema

Each CommonModel Schema is a folder with the current / default version
at the top level and a 'versions' folder with previous versions suffixed
with their version number:

- ExampleSchema/
  - ExampleSchema.yml
  - versions/
    - ExampleSchema-1.5.2.yml
    - ExampleSchema-0.3.0.yml
    - ExampleSchema-0.0.1.yml
