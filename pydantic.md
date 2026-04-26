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

## How does Pydantic work?

<img width="755" height="317" alt="image" src="https://github.com/user-attachments/assets/225c929f-919f-4e9c-b205-c9ecce888cf2" />

---
Here, <br>
model could also be named a class.
<br>

## Field Validator
**Definition:** Field validators are constraints defined on Pydantic model fields that enforce data types, formats, ranges, lengths, and custom business rules at the point of entry.

### What is a field validator?
A field validator is a rule (or set of rules) attached to a field in a Pydantic model. It ensures that the data coming from a request body, query parameter, or path matches exactly what you expect.

- If data passes → it continues to your endpoint.
- If data fails → FastAPI automatically returns a `422 Unprocessable Entity` error with a clear explanation of what went wrong.
No manual `if` statements needed.

### Two ways to add validators

#### 1. Inline constraints using `Field()`
Use the `Field()` function from Pydantic to set simple, declarative rules.

```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, lt=150)          # greater than 0, less than 150
    email: str = Field(pattern=r"^\S+@\S+\.\S+$")  # regex for a basic email
    website: str | None = Field(default=None, max_length=200)
```

#### 2. Custom validators with decorators
When you need logic that’s more than a simple boundary (e.g., “password must contain a digit and a special char”), you use the `@field_validator` decorator (Pydantic v2, recommended).

```python
from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char in "!@#$%^&*" for char in v):
            raise ValueError("Password must contain at least one special character")
        return v
```
#### 3. Full working example

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

class Item(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)            # must be > 0
    quantity: int = Field(ge=0)           # >= 0
    discount_code: str | None = Field(default=None, max_length=10)

    @field_validator("discount_code")
    @classmethod
    def check_discount_format(cls, v: str | None) -> str | None:
        if v is not None and not v.startswith("SAVE"):
            raise ValueError('Discount code must start with "SAVE"')
        return v

@app.post("/items/")
async def create_item(item: Item):
    # At this point, item is fully validated.
    return {"item": item}
```

#### 4. What happens if the validation fails

If I send this..

```json
{
  "name": "A",
  "price": -5,
  "quantity": 2
}
```
FastAPI automatically replies with a `422` status and a body like:

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "ensure this value has at least 2 characters",
      "type": "value_error.any_str.min_length"
    },
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

No extra code from me — just define the model.

### From Next.js to FastAPI – mental mapping

<div align="center">
    
|     **Next.js / Frontend**    	| **FastAPI (Pydantic)** 	|
|:-----------------------------:	|:----------------------:	|
|  Zod schema / Yup validation  	|   Pydantic BaseModel   	|
|       z.string().min(2)       	|   Field(min_length=2)  	|
|     z.number().positive()     	|       Field(gt=0)      	|
| .refine() / custom validation 	|    @field_validator    	|
|     react-hook-form errors    	| Automatic 422 response 	|

</div>

####  When to use which?

- Use `Field()` arguments for simple checks: lengths, ranges, regex, whether a field is required, default values.

- Use `@field_validator` when validation depends on another field, needs database lookups, or involves complex logic.

### Examples for field validator

```python
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '30', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info) # validation -> type coercion

update_patient_data(patient1)
```
---

## Model Validator
**Defination:** A model validator (Pydantic v2 @model_validator) is a validator that operates on the entire model instance after each field has been validated individually. It can see all fields at once, allowing you to enforce rules that involve multiple fields or to transform the whole data object.

In other words: <br>

- Field validators ask: “Is this one field correct?”
- Model validators ask: “Does this combination of fields make sense together?”

### Why is it used?

Use a model validator when:

- Cross‑field validation – One field’s validity depends on the value of another field (e.g., confirm_password must match password; if is_premium is true, then payment_id is required).
- Complex business rules – The logic involves multiple fields and can’t be cleanly expressed in a single field validator.
- Data transformation – You need to compute or modify several fields at once (e.g., create a full_name from first_name and last_name).
- Order matters – You want validation to happen after individual fields are checked but before the model is fully constructed.

### Two modes (Pydantic v2)

- `mode='before'` – Runs before field validation, giving you access to raw input (e.g., a dict). Useful for normalizing input.

- `mode='after'` – Runs after field validation, receiving the already-validated model instance (or a partially constructed one). This is the default and most common.


### Example: Password confirmation and conditional fields

```python
from pydantic import BaseModel, model_validator

class UserSignup(BaseModel):
    password: str
    confirm_password: str
    is_premium: bool = False
    payment_id: str | None = None

    # This runs after individual fields are validated
    @model_validator(mode='after')
    def check_passwords_match_and_payment(self):
        # 1. Passwords must match
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        
        # 2. If premium is selected, payment_id is required
        if self.is_premium and not self.payment_id:
            raise ValueError("payment_id is required for premium accounts")
        
        return self
```

If I send:

```json
{
  "password": "abc",
  "confirm_password": "xyz",
  "is_premium": true
}
```

I would get:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": [],
      "msg": "Value error, Passwords do not match",
      ...
    }
  ]
}
```

_**Notice the "loc": [] – it’s a model‑level error, not tied to a single field.**_

### Bonus: Transform data with mode='before'
Sometimes you receive data in a different shape and want to clean it up before validation.

```python
from pydantic import BaseModel, model_validator

class Product(BaseModel):
    name: str
    price: float
    tax: float = 0.0

    @model_validator(mode='before')
    @classmethod
    def compute_tax_if_missing(cls, data: dict) -> dict:
        # data is the raw input dict (e.g., from JSON)
        if isinstance(data, dict):
            if 'tax' not in data and 'price' in data:
                data['tax'] = data['price'] * 0.1
        return data
```

### Quick rule of thumb

- If the rule involves one field only → `@field_validator` or `Field()` constraints.

- If the rule needs two or more fields (or the whole object) → `@model_validator`.


### Examples

```python
from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model



def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '65', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462', 'emergency':'235236'}}

patient1 = Patient(**patient_info) 

update_patient_data(patient1)
```

---

