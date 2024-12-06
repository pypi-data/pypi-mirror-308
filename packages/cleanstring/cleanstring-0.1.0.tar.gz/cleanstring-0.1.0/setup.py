from setuptools import setup, find_packages

setup(
    name="cleanstring",
    version="0.1.0",
    author="Cool Murdock",
    author_email="coolmurdock6@justzeus.com",
    description="A simple package to clean strings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/firebase_data_storer",  # Your project's URL
    packages=find_packages(),
    include_package_data=True,
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
