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

## Computed Fields

A computed field is a field that doesn’t come from the request body or user input. Instead, its value is calculated inside the model based on other fields, and it’s included when the model is serialized (e.g., returned as a JSON response). It acts like a derived property that’s always consistent with the rest of the data.

### Why is it used?

Use a computed field when:

- Derived data – You want to expose a value that is fully determined by other fields (e.g., total_price = unit_price * quantity).

- Avoid frontend recalculations – Instead of making your Next.js frontend compute the same thing over and over, you let the backend do it once and ship it.

- Consistency – Ensures the same calculation logic is used everywhere, not scattered across clients.

- Read‑only guarantees – The client can never set or overwrite this field; it’s purely an output.

- Cleaner responses – You can include extra information in API responses without storing it in a database.

### How to create one (Pydantic v2)

Use the computed_field decorator from Pydantic. The function’s return value becomes the field’s value whenever the model is serialized (e.g., in a FastAPI response).

```python
from pydantic import BaseModel, computed_field

class Order(BaseModel):
    unit_price: float
    quantity: int
    discount_percent: float = 0.0

    @computed_field
    @property
    def total_price(self) -> float:
        discount = self.discount_percent / 100
        return self.unit_price * self.quantity * (1 - discount)

    @computed_field
    @property
    def is_bulk_order(self) -> bool:
        return self.quantity >= 10
```

The `@property` decorator makes it accessible like an attribute (order.total_price), and `@computed_field` tells Pydantic to include it in the model’s serialized output (.model_dump(), JSON response, etc.).

###  Full FastAPI Example

```python
from fastapi import FastAPI
from pydantic import BaseModel, computed_field

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    tax_rate: float = 0.1

    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1 + self.tax_rate), 2)

    @computed_field
    @property
    def description(self) -> str:
        return f"{self.name} (${self.final_price})"

@app.post("/product/")
async def create_product(product: Product):
    # product now contains computed fields automatically
    return product
```

#### Request:

```json
{
  "name": "Notebook",
  "price": 20.0
}
```

#### Response:

```json
{
  "name": "Notebook",
  "price": 20.0,
  "tax_rate": 0.1,
  "final_price": 22.0,
  "description": "Notebook ($22.0)"
}
```

The client never sent `final_price` or `description` – they were computed on the server and included in the response.

### Examples

```python
from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float # kg
    height: float # mtr
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi



def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('BMI', patient.bmi)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '65', 'weight': 75.2, 'height': 1.72, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462', 'emergency':'235236'}}

patient1 = Patient(**patient_info) 

update_patient_data(patient1)
```

### Field Validator vs Model Validator vs Computed Field

|     Purpose     	| Validates input? 	| Transforms output? 	| Sees multiple fields? 	|
|:---------------:	|:----------------:	|:------------------:	|:---------------------:	|
| Field Validator 	|   single field   	|          X         	|           X           	|
| Model Validator 	|    whole object  	|   (with 'before')  	|           ✅           	|
|  Computed Field 	|         X        	|   adds new fields  	|   (can read others)   	|

## Important note
- Computed fields are read‑only in requests. If a client tries to send them, Pydantic will ignore them (they are not accepted as input). They exist only in serialized output.

- They are recalculated every time you call `.model_dump()` or the model is returned by FastAPI, so keep them lightweight (no heavy DB calls, unless you really need to).


## Nested Modules

A nested model is simply a Pydantic model used as the type of a field inside another Pydantic model. This allows you to define complex, tree‑like data structures.
Serialization (in our context) is the automatic conversion of these nested model instances into and from JSON – handled entirely by FastAPI and Pydantic.

In easier words: if a user’s data includes an address, you create an Address model, and then your User model has an address: Address field. The validation and JSON conversion happens recursively.


### Why is it used?

- Real‑world complex data – Most APIs need to receive or return structured, hierarchical data (e.g., an order contains multiple items, each with its own fields).

- Clean code & reuse – Define a sub‑model once and reuse it in multiple parent models.

- Automatic deep validation – Pydantic will validate every level of nesting; you get full 422 errors for any invalid nested field.

- One‑line serialization – When you return a model from a FastAPI endpoint, all nested models get automatically converted to nested JSON. No manual mapping or serializing.

- Works with all previous tools – Field validators, model validators, and computed fields all work inside nested models as well.

### Example: Order with nested customer and items
```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field

app = FastAPI()

# ---------- Nested Model 1 ----------
class Address(BaseModel):
    street: str
    city: str
    zip_code: str = Field(min_length=5, max_length=10)

# ---------- Nested Model 2 ----------
class Customer(BaseModel):
    name: str
    email: str
    shipping_address: Address    # <-- nested model

# ---------- Nested Model 3 ----------
class OrderItem(BaseModel):
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

    @computed_field
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price

# ---------- The Parent Model ----------
class Order(BaseModel):
    customer: Customer
    items: list[OrderItem]      # a list of nested models
    discount_code: str | None = None

    @computed_field
    @property
    def order_total(self) -> float:
        return sum(item.total_price for item in self.items)

@app.post("/order/")
async def create_order(order: Order):
    # Order is fully validated, including all nesting
    return order   # FastAPI serializes the entire tree to JSON automatically
```
#### Sample Request:
```json
{
  "customer": {
    "name": "Alice",
    "email": "alice@example.com",
    "shipping_address": {
      "street": "123 Main St",
      "city": "Springfield",
      "zip_code": "12345"
    }
  },
  "items": [
    {
      "product_name": "Widget",
      "quantity": 3,
      "unit_price": 9.99
    },
    {
      "product_name": "Gadget",
      "quantity": 1,
      "unit_price": 24.99
    }
  ]
}
```

#### Response (automatically serialized):

```json
{
  "customer": {
    "name": "Alice",
    "email": "alice@example.com",
    "shipping_address": {
      "street": "123 Main St",
      "city": "Springfield",
      "zip_code": "12345"
    }
  },
  "items": [
    {
      "product_name": "Widget",
      "quantity": 3,
      "unit_price": 9.99,
      "total_price": 29.97
    },
    {
      "product_name": "Gadget",
      "quantity": 1,
      "unit_price": 24.99,
      "total_price": 24.99
    }
  ],
  "discount_code": null,
  "order_total": 54.96
}
```
Notice that computed fields (total_price, order_total) are also present, even inside nested items.

### Another Examples

```python
from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'gender': 'male', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(include=)

print(type(temp))


# Better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use Vitals in multiple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically—no extra work needed
```



### Helpful tricks

#### 1. Optional Nested Model:

```python
class User(BaseModel):
    profile_picture: Image | None = None   # can be missing or null
```


#### 2. Deep validation still works:

```bash
loc: ["body", "customer", "shipping_address", "zip_code"]
```

#### 3. Nested models work with Field() defaults

```python
class Order(BaseModel):
    customer: Customer
    items: list[OrderItem] = Field(default_factory=list)  # default empty list
```

#### 4. Model validators at any level
You can have a `@model_validator` inside `Address` that checks something like "if city is X, zip must start with Y" – it runs independently during validation of that sub‑object.

### Bringing it all together

|     **Tool**    	|     **Where it runs**     	|                            **Purpose**                            	|
|:---------------:	|:-------------------------:	|:-----------------------------------------------------------------:	|
| Field Validator 	|     On a single field     	|                  Validate individual input values                 	|
| Model Validator 	|     On the whole model    	|              Cross‑field checks, data transformation              	|
|  Computed Field 	|      After validation     	|                Add read‑only derived output fields                	|
|  Nested Models  	| On fields that are models 	| Structure complex data, automatic deep validation & serialization 	|







