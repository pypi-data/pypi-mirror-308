from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ahp-gauss",
    version="0.1.4",
    description="The AHP-Gaussian Decision Support Library is a extensible solution designed for multi-criteria decision-making (MCDM) leveraging both traditional and advanced AHP methodologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "pyyaml",
        "pytest"
    ],
    entry_points={
        "console_scripts": [
            "ahp-gauss=main:main",
        ],
    },
)
