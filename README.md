# Python OOP - Second Exam Practice: Pizza Management System

Employee management for two pizza stores: **Pizza Hut** and **Pizza Dominos**.

The exam is done in three parts:

1. **Design** - class diagram: [exercises/pizza/class_diagram.md](exercises/pizza/class_diagram.md)
2. **Implementation** in Python: [exercises/pizza](exercises/pizza)
3. **Submission** - this public Git repository (the link is sent by email)

## Run

```bash
cd exercises/pizza
python main.py
```

## Files

| File | Contents |
|------|----------|
| `surprise.py` | `Surprise` (abstract) + `FreePizzaSurprise`, `BonusSurprise` |
| `employee.py` | `Employee` - rank 1-100 with `set_rank()`, rank date, optional surprise |
| `pizza_store.py` | `PizzaStore` (abstract) - hiring, resigning, expenses, rank, surprises |
| `pizza_hut.py` | `PizzaHut` - rank = average of employee ranks |
| `pizza_dominos.py` | `PizzaDominos` - rank = sum of employee ranks |
| `main.py` | Demo of the whole system |
