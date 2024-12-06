from setuptools import setup

setup(
    name="SalesData",
    version="0.1.0",
    description="A PySpark-based sales data processing tool",
    author="Diogo Mariano",
    author_email="diogo.mariano@deus.ai",
    url="https://github.com/DiogoRM-DEUS-DE/ABN_CHALLENGE",
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "sales-data = main:main",  # Entry point command
        ],
    },
    install_requires=[
        "pyspark==3.5.3",
    ],
    python_requires=">=3.10",
)
