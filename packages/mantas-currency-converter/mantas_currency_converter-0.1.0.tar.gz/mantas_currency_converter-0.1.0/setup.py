from setuptools import setup, find_packages

setup(
    name="mantas_currency_converter",
    version="0.1.0",
    author="Meskenaz",
    email="m.jankauskas123@gmail.com",
    packages=find_packages(),
    install_requires=[
        'CurrencyConverter==0.17.34'
    ],
    python_requires=">=3.9"
)