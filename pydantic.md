# Pydantic Notes
## What is Pydantic?
Pydantic is a Python library that helps you check and validate data. Think of it like a data security guard: whenever you give it data, it makes sure the data is the right type and shape before you use it.

## What does it do?

- Validates data → Ensures numbers are numbers, strings are strings, emails look like emails, etc.
- Converts types → If you pass "123" (string), it can automatically turn it into 123 (integer).
- Defines models → You create a "blueprint" (class) for your data, and Pydantic enforces it.

## Examples

### Example 1

```python
from pydantic import BaseModel

# Define a data model (blueprint)
class User(BaseModel):
    name: str
    age: int
    email: str

# Give it some data
user = User(name="Alice", age="25", email="alice@example.com")

print(user)
```
### What is happening here?

- `age="25"` was a string, but Pydantic converted it into an integer automatically.
- If you tried `age="twenty five"`, it would throw an error, because that’s not a valid number.

### Output:

```bash
name='Alice' age=25 email='alice@example.com'
```

### Example 2:

```python
def insert_patient_data(name: str, age: int):
    print(name)
    print(age)
    print("Inserted data type"
# Function call: lets say the programmer by mistake gave string instead of int. The code still works in python, instead of showing error
insert_patient_data("raj", "26")

# Output:
'''
The code will work fine without shodwing any error.
'''
```
### What the code does?
- This code will work fine, instead of showing any error, by default python does not handle type errors very well.

### The correct way:

```python
def insert_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
            print(name)
            print(age)
            print("Inserted data type")
    else:
        raise TypeError("Incorrect Data Type")
# Function call
insert_patient_data("raj", "26")

# Output:
'''
This time the code will rise a type error
'''

```

