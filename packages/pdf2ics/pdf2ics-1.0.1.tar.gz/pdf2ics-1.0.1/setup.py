from setuptools import setup, find_packages

setup(
    name="pdf2ics",
    version="1.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "pdfplumber",
        "icalendar",
        "pytz",
    ],
    entry_points={
        "console_scripts": [
            "pdf2ics=pdf2ics.pdf2ics:main",
        ],
    },
    author="Stephen Swan",
    author_email="",
    description="Convert basketball schedule PDF to ICS calendar file",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaxnoth/pdf2ics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)