from setuptools import setup, find_packages

setup(name='SNMP Manager',
        version='0.1',
        description="SNMP Manager - Sistema para gerenciamento de portas SNMP",
        author="Marcelo Nunes Paolillo e Felipe de Avila",
        packages=find_packages(),
        install_requires=[
                "pysnmp",
                "flask",
                "apscheduler",
                "pymongo"
                ]
)
