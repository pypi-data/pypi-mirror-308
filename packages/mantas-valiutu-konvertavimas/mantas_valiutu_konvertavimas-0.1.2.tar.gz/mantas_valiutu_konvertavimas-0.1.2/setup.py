from setuptools import setup, find_packages

setup(
    name="mantas_valiutu_konvertavimas",
    version="0.1.2",
    author="Mantaszup123",
    email="mantaszup@gmail.com",
    packages=find_packages(),
    install_requires=["currency_converter"],
    python_requires=">=3.6"
)