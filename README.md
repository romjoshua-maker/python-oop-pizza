# Pizza Management System - Exam II Practice

Employee management for two pizza stores: **Pizza Hut** and **Pizza Dominos**.

1. Class diagram (below)
2. Python implementation: `pizza.py`
3. Submitted as this Git repository

## Class Diagram

```mermaid
classDiagram
    direction TB

    class PizzaEmployee {
        +id: int
        +first_name: str
        +last_name: str
        +address: str
        +salary: float
        +start_date: datetime
        +pizza_rank: int
        +pizza_rank_date: datetime
        +pizza_surprise: Surprise
        +set_rank()
        +is_rank_valid(rank_range: int) bool
        +use_surprise()
    }

    class Surprise {
        <<interface>>
        +activate_surprise()*
    }

    class PizzaVoucher {
        +activate_surprise()
    }

    class PizzaStore {
        <<abstract>>
        +id: int
        +name: str
        +address: str
        +phone_number: str
        +employees: list~PizzaEmployee~
        +number_of_employees: int
        +rank: float
        +calculate_employee_expenses() float
        +hire_employee(employee: PizzaEmployee)
        +resign_employee(employee: PizzaEmployee)
        +take_back_surprise(employee: PizzaEmployee)
        +give_surprise_to_best_employees(surprise: Surprise)
        +get_ranks() list
        +calculate_rank()* float
        +calculate_ranged_rank(rank_range: int) float
        +print_store()
    }

    class PizzaHut {
        +calculate_rank() float
    }

    class PizzaDominos {
        +calculate_rank() float
    }

    PizzaEmployee "*" --o "1" PizzaStore : employs
    PizzaEmployee "0..1" --> "1" Surprise : has
    Surprise <|.. PizzaVoucher : implements
    PizzaStore <|-- PizzaHut : inherits
    PizzaStore <|-- PizzaDominos : inherits

    style PizzaEmployee fill:#eefbfa,stroke:#2cc2bd
    style Surprise fill:#fdf0ff,stroke:#e07be6
    style PizzaVoucher fill:#fff6d8,stroke:#e6be55
    style PizzaStore fill:#fff5ec,stroke:#f39a4f
    style PizzaHut fill:#edfbff,stroke:#21c3e6
    style PizzaDominos fill:#eefbf2,stroke:#47d07a
```

- Pizza Hut rank = **average** of the employees' ranks, Pizza Dominos rank = **sum**.
- `FreeDessert` (in the tests) isn't a `Surprise` subclass but has `activate_surprise()` - duck typing.

## Run

```bash
python pizza.py
```

Needs the `overrides` package (`pip install overrides`).
