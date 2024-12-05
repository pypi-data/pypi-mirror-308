from setuptools import setup, find_packages

setup(
    name="eur-to-usd",
    version="0.1.0",
    author="Asasai001",
    email="ambrasas.arnoldas.com",
    description="simple converter eur to usd",
    packages=find_packages(),
    install_requires=["currencyconverter"],
    python_requires=">=3.6",
)