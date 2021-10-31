from .field_types import *

key_lookup = {
    "alphavantage.AlphavantageCompanyOverview": "../schemas/alphavantage/AlphavantageCompanyOverview.yml",
    "alphavantage.AlphavantageEodPrice": "../schemas/alphavantage/AlphavantageEodPrice.yml",
    "core.Any": "../schemas/core/Any.yml",
    "crunchbase.CrunchbaseFundingRound": "../schemas/crunchbase/CrunchbaseFundingRound.yml",
    "crunchbase.CrunchbasePerson": "../schemas/crunchbase/CrunchbasePerson.yml",
    "crunchbase.CrunchbaseOrganization": "../schemas/crunchbase/CrunchbaseOrganization.yml",
    "mailchimp.MailchimpMember": "../schemas/mailchimp/MailchimpMember.yml",
    "square.SquareCustomer": "../schemas/square/SquareCustomer.yml",
    "square.SquareOrder": "../schemas/square/SquareOrder.yml",
    "square.SquarePayment": "../schemas/square/SquarePayment.yml",
    "square.SquareCatalogObject": "../schemas/square/SquareCatalogObject.yml",
    "square.SquareLoyaltyAccount": "../schemas/square/SquareLoyaltyAccount.yml",
    "bigcommerce.BigCommerceOrderProduct": "../schemas/bigcommerce/BigCommerceOrderProduct.yml",
    "bigcommerce.BigCommerceOrder": "../schemas/bigcommerce/BigCommerceOrder.yml",
    "fred.FredSeries": "../schemas/fred/FredSeries.yml",
    "fred.FredObservation": "../schemas/fred/FredObservation.yml",
    "shopify.ShopifyOrder": "../schemas/shopify/ShopifyOrder.yml",
    "stocks.Ticker": "../schemas/stocks/Ticker.yml",
    "stocks.EodPrice": "../schemas/stocks/EodPrice.yml",
    "bi.Transaction": "../schemas/bi/Transaction.yml",
    "stripe.StripeCharge": "../schemas/stripe/StripeCharge.yml",
    "stripe.StripeRefund": "../schemas/stripe/StripeRefund.yml",
    "stripe.StripeSubscription": "../schemas/stripe/StripeSubscription.yml",
    "stripe.StripeInvoice": "../schemas/stripe/StripeInvoice.yml",
    "stripe.StripeSubscriptionItem": "../schemas/stripe/StripeSubscriptionItem.yml",
}
namespace_lookup = {
    "AlphavantageCompanyOverview": ["alphavantage.AlphavantageCompanyOverview"],
    "AlphavantageEodPrice": ["alphavantage.AlphavantageEodPrice"],
    "Any": ["core.Any"],
    "CrunchbaseFundingRound": ["crunchbase.CrunchbaseFundingRound"],
    "CrunchbasePerson": ["crunchbase.CrunchbasePerson"],
    "CrunchbaseOrganization": ["crunchbase.CrunchbaseOrganization"],
    "MailchimpMember": ["mailchimp.MailchimpMember", "mailchimp.MailchimpMember"],
    "SquareCustomer": ["square.SquareCustomer"],
    "SquareOrder": ["square.SquareOrder"],
    "SquarePayment": ["square.SquarePayment"],
    "SquareCatalogObject": ["square.SquareCatalogObject"],
    "SquareLoyaltyAccount": ["square.SquareLoyaltyAccount"],
    "BigCommerceOrderProduct": ["bigcommerce.BigCommerceOrderProduct"],
    "BigCommerceOrder": ["bigcommerce.BigCommerceOrder"],
    "FredSeries": ["fred.FredSeries"],
    "FredObservation": ["fred.FredObservation"],
    "ShopifyOrder": ["shopify.ShopifyOrder"],
    "Ticker": ["stocks.Ticker"],
    "EodPrice": ["stocks.EodPrice"],
    "Transaction": ["bi.Transaction"],
    "StripeCharge": ["stripe.StripeCharge"],
    "StripeRefund": ["stripe.StripeRefund"],
    "StripeSubscription": ["stripe.StripeSubscription"],
    "StripeInvoice": ["stripe.StripeInvoice"],
    "StripeSubscriptionItem": ["stripe.StripeSubscriptionItem"],
}
