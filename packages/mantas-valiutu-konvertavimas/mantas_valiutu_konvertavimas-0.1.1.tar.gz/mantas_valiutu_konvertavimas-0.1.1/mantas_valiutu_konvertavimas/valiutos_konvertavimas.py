from currency_converter import CurrencyConverter

c = CurrencyConverter()

def eur_to_usd(amount):
    return c.convert(amount, "EUR", "USD")