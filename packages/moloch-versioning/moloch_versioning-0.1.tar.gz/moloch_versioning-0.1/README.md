# Moloch Versioning

Moloch Versioning is an automated version control system that manages versioning with
a detailed and customizable changelog. It offers semantic versioning capabilities, thematic name generation,
and visibility and priority classification.

## Installation

To install this package locally, use the following command after generating the `.whl` file:

```bash
pip install path/to/moloch_versioning-0.1-py3-none-any.whl
```

## Usage

```python
from moloch_versioning import VersionControlSystem

vcs = VersionControlSystem()
# Generate a new version and add an entry to the changelog
version = vcs.create_version_identifier("major")
print("Generated version:", version)
```

## Features

- **Semantic Versioning**: Supports `major`, `minor`, and `patch` versioning.
- **Customizable Changelog**: Includes fields like timestamp, description, status, and impact.
- **Visibility Classification**: Classify changes as public, confidential, or secret.
- **Thematic Names**: Generate unique version names based on predefined themes.

## Requirements

- Python 3.7 or higher

