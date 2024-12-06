# Dainty

Dainty is a simple, plug and play extension of pydantic, that allows you to
easily create HTML input elements based on your pydantic models.

## Installation

```bash
uv add dainty
```

## Usage

```python
from dainty import DaintyModel

class MyModel(DaintyModel):
    name: str
    age: int
    gender: Literal["Male", "Female", "Non Binary", "Other"]

MyModel.to_html()
```
