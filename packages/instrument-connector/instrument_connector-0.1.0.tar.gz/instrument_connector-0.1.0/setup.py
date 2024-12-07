from setuptools import setup, find_packages

setup(
    name="instrument_connector",  # Nome del pacchetto
    version="0.1.0",              # Versione iniziale
    author="Federico Guerra",
    author_email="",              # Email lasciata vuota come richiesto
    description="A Python library to connect to instruments via PyVISA",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",                # Licenza MIT
    packages=find_packages(),     # Cerca automaticamente i pacchetti
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyvisa",  # Dipendenze della libreria
    ],
)
