from setuptools import setup, find_packages

setup(
    name="drf-excel-export",
    version="0.1.2",   
    description="A tool to export Django REST Framework API documentation to Excel",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Donald Programmeur",
    author_email="donaldtedom0@gmail.com",
    url="https://github.com/donaldte/drf-excel-export",  # Link to your GitHub repo
    packages=find_packages(),
    install_requires=[
        "django",
        "djangorestframework",
        "openpyxl",
        "drf-spectacular", 
        "drf-yasg", 
        "pyyaml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
