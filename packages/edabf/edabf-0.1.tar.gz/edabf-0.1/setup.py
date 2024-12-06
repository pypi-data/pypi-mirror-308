from setuptools import setup, find_packages

setup(
    name="edabf",
    version="0.1",
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
)
