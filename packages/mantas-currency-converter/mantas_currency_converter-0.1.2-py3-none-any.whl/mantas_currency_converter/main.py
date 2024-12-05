from mantas_currency_converter.converter import convert_currency

total = float(input("Enter the amount: "))
from_currency = input("Enter the currency you want to convert from (e.g., 'EUR'): ")
to_currency = input("Enter the currency you want to convert to (e.g., 'USD'): ")
converted_amount = convert_currency(total, from_currency, to_currency)
print(f"{total} {from_currency} is equal to {converted_amount:.2f} {to_currency}.")
