from setuptools import setup, find_packages

setup(
    name="currency_converter_devworld",
    version="0.1.0",
    author="kalined",
    author_email="edgar.kalinovski@gmail.com",
    description="A simple currency converter package",
    packages=find_packages(),
    install_requires=["CurrencyConverter"],
    python_requires=">=3.6"
)