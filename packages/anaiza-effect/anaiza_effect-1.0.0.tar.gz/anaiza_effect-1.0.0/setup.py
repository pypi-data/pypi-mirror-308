from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="anaiza_effect",
    version="1.0.0",
    description="Display Anaiza Text Effect in the terminal.",
    long_description=long_description,  # Use README content as long description
    long_description_content_type="text/markdown",  # Specify markdown format
    author="anaiza",
    author_email="test@email.com",
    packages=find_packages(),
    install_requires=["pyfiglet"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)