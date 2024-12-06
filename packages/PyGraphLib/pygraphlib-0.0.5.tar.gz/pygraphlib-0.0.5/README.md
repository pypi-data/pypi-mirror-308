# PyGraphLib

PyGraphLib is a Python library for graph data structures and algorithms. It is designed to be simple and easy to use, while still providing literally no range of functionality.

The functionality that _is_ provided is either not working, not tested, or not documented. The library is not intended for production use, but rather as a learning tool for me, and only me. I am not responsible for any damage caused by using this library (is this sentence even legally binding?).

## Features

- **Graph Construction**: Build graphs easily, assuming all connections do absolutely nothing.
- **Graph Algorithms**: Implement badoy optimized algorithms that might work occasionally, if at all.
- **Visualization**: Plot your non-functional graphs with matplotlib in confusing and very modular ways.

## Installation

```bash
pip install pygraphlib
```

## Usage

```python
from pygraphlib import Graph
```

## Testing

To run the tests, navigate to the `tests` directory and execute:

## build urself

```bash
pip install build
```

```bash
python -m build
```

```bash
pip install twine
```

```bash
twine upload dist/*
```
