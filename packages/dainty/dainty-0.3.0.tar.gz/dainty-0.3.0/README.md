# Dainty

Dainty is a simple, plug and play extension of pydantic, that allows you to
easily create HTML input elements based on your pydantic models.

## Installation

```bash
uv add dainty
```

## Usage

```python
from typing import Literal

from pydantic import Field

from dainty import DaintyModel
from dainty.dainty import DaintyForm


class MyModel(DaintyModel):
    name: str
    age: int = Field(ge=20, lt=40)
    gender: Literal["Male", "Female", "Non Binary", "Other"]

    dainty_form = DaintyForm(target_url="/submit")


print(MyModel.to_html(form=True))
```

This will generate the following HTML:

```html
<form>
  <label for="name">Name: </label>
  <input type="text" name="name" id="name" value="" required />
  <br /><br />
  <label for="age">Age: </label>
  <input
    type="number"
    name="age"
    id="age"
    value=""
    step="1"
    min="20"
    max="39"
    required
  />
  <br /><br />
  <label for="gender">Gender: </label>
  <select name="gender" id="gender" required>
    <option value="Male">Male</option>
    <option value="Female">Female</option>
    <option value="Non Binary">Non Binary</option>
    <option value="Other">Other</option>
  </select>
  <br /><br />
  <input type="submit" value="Submit" method="post" formaction="/submit" />
</form>
```

## TODO:

- [ ] Add support for more field types
- [ ] Move inputs inside labels for better clickability
- [ ] More customization options for DaintyForm
- [ ] More html boilerplate elements, such as div containers
