from setuptools import setup

setup(
    name="shelf",
    version="1.0",
    py_modules=["shelf"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        shelf=shelf:cli
    """,
    pulls=4,
)
