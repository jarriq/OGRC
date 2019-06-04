from setuptools import setup, find_packages

setup(name='sipa',
        version='0.2',
        description="Painel SIPA - Sistema Inteligente para Padronização e Análise",
        author="Marcelo Nunes Paolillo e Felipe de Avila",
        packages=find_packages(),
        install_requires=[
                "dbfread",
                "flask",
                "fuzzywuzzy",
                "imbalanced-learn",
                "joblib",
                "nltk",
                "openpyxl",
                "pandas",
                "pymongo",
                "pyunpack",
                "scikit-learn",
                "unidecode",
                "psutil",
                "pyexcel",
                "pyexcel-xls",
                "pyexcel-xlsx",
                "python-Levenshtein"
                ]
)
