from setuptools import setup, find_packages

setup(
    name="cleanstring",
    version="0.2.0",
    author="Your Name",
    author_email="coolmurdock6@justzeus.com",
    description="A simple package to clean strings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cleanstring",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["serviceAccountKey.json"]},  # Include JSON file
    install_requires=[
        "firebase-admin",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
