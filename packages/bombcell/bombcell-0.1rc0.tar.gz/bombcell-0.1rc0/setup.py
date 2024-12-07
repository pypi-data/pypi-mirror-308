from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name="bombcell",
    version="0.1c",
    descriptin="Description of the package",
    author="Julie Fabre and Sam Dodgson",
    author_email="samuel.dodgson@ucl.ac.uk",
    packages=find_packages(),  
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
        "mtscomp",
        "jobLib",
        "pyarrow",
        "Path"
    ],
    long_description=description,
    long_description_content_type='text/markdown'
)