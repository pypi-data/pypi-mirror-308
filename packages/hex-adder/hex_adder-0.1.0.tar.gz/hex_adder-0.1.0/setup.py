from setuptools import setup, find_packages

setup(
    name="hex_adder",  # Replace with a unique name for your package
    version="0.1.0",
    description="A simple Python package to add two numbers",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),  # Automatically finds your `test.py` as a module
    py_modules=["test"],  # This specifies the modules included in the package
    entry_points={
        "console_scripts": [
            "simple-adder=test:add_numbers",  # Command-line tool entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
