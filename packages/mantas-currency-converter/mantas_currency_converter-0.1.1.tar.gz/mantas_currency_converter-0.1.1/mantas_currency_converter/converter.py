from currency_converter import CurrencyConverter

def convert_currency(total, from_currency, to_currency):
    converter = CurrencyConverter()
    return converter.convert(total, from_currency, to_currency)