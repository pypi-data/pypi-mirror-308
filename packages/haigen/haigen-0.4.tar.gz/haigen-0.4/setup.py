from setuptools import setup, find_packages

setup(
    name='haigen',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain_core"
    ]

)
