from setuptools import setup, find_packages

setup(
    name="bacon-distance",
    author="Adir Nissan",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["pytest", "pandas", "pyyaml"],
)
