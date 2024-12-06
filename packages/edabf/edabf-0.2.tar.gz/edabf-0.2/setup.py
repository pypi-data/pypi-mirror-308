from setuptools import setup, find_packages
from pathlib import Path

# Lee el contenido del README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="edabf",
    version="0.2",
    description="A package for EDA on CSV and SQL data.",
    author="nicolas_conde_brainfood",
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.2",
        "polars==1.10.0",
        "psycopg2==2.9.9",
        "psycopg2-binary==2.9.9",
        "pymssql==2.3.1",
        "oracledb==1.0.0",
        "cx_Oracle",
        "XlsxWriter==3.2.0",
        "pyarrow==17.0.0",
        "pymysql",
        "SQLAlchemy"
    ],
    python_requires=">=3.7",
    long_description=long_description,  # Agrega el contenido del README
    long_description_content_type="text/markdown",  # Especifica el tipo de contenido
)
