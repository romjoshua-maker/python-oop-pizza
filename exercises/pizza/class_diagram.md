# Pizza Management System - Class Diagram

```mermaid
classDiagram
    direction TB

    class Surprise {
        <<abstract>>
        +activate_surprise()*
    }
    class FreePizzaSurprise {
        +activate_surprise()
    }
    class BonusSurprise {
        +amount: float
        +activate_surprise()
    }

    class Employee {
        +id: int
        +first_name: str
        +last_name: str
        +address: str
        +salary: float
        +start_date: date
        +pizza_rank: int
        +pizza_rank_date: datetime
        +pizza_surprise: Surprise
        +set_rank()
        +is_rank_valid(rank_range: int) bool
    }

    class PizzaStore {
        <<abstract>>
        +id: int
        +name: str
        +address: str
        +phone_number: str
        +employees: list~Employee~
        +number_of_employees: int
        +rank: float
        +is_employee(employee) bool
        +hire_employee(employee)
        +resign_employee(employee)
        +calculate_employee_expenses() float
        +calculate_rank() float
        +calculate_ranged_rank(rank_range: int) float
        +give_surprise(employee, surprise)
        +give_surprise_to_best(surprise)
        +take_back_surprise(employee) Surprise
        #_rank_formula(ranks: list~int~)* float
    }

    class PizzaHut {
        #_rank_formula(ranks) float
    }
    class PizzaDominos {
        #_rank_formula(ranks) float
    }

    PizzaStore <|-- PizzaHut
    PizzaStore <|-- PizzaDominos
    Surprise <|-- FreePizzaSurprise
    Surprise <|-- BonusSurprise
    PizzaStore "1" o-- "0..*" Employee : employs
    Employee "1" o-- "0..1" Surprise : pizza_surprise
    note for PizzaHut "rank = average of employee ranks"
    note for PizzaDominos "rank = sum of employee ranks"
```

## Design notes

- **PizzaStore** is abstract. The only thing that differs between the two stores is how the
  rank is calculated, so each subclass implements `_rank_formula()` (Template Method):
  `PizzaHut` = average of employee ranks, `PizzaDominos` = sum of employee ranks.
- The constructor calls `calculate_rank()`, so every new store starts with a rank.
- `number_of_employees` is a property computed from the employees list, so it can never go out of sync.
- `hire_employee()` / `resign_employee()` check `is_employee()` before changing the list.
  Resigning also takes back the employee's surprise.
- `calculate_ranged_rank(rank_range)` asks every employee whose rank is older than
  `rank_range` days to rank again (`set_rank()`), then recalculates the store rank.
- **Surprise** is an abstract class with `activate_surprise()`, so any surprise type works
  as long as it implements that method. An employee's surprise may be `None`.
