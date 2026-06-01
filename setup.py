from setuptools import setup, find_packages

setup(
    name="netsweep",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "scapy>=2.5.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "netsweep=netsweep.cli:main",
        ],
    },
    author="Seu Nome",
    description="Ferramenta CLI para varredura de rede local e análise de serviços",
    python_requires=">=3.8",
)
