from setuptools import setup, find_packages

setup(
    name="my_cli_data_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
    ],
    entry_points={
        "console_scripts": [
            "my_cli_data_app = my_cli_data_app.main:app",
        ],
    },
)
