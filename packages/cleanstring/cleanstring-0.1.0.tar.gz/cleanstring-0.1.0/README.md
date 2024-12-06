# Clean String

A simple package to clean strings.

## Installation

To install the package, run the following command:

```bash
pip install cleanstring
```

## Usage

To use the package, import it and call the `clean_string` function:

```python
from cleanstring import clean_string

name = "Anish Sharma"
contact = "1234567890"

cleaned_string = clean_string(name, contact)

print(f"The cleaned strings are Contact: {cleaned_string.get('contact')}, Name: {cleaned_string.get('name')}")
```

This will output:

```
The cleaned strings are Contact: 1234567890, Name: Anish Sharma
```
