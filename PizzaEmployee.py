import random
from datetime import datetime, timedelta

MIN_RANK = 1
MAX_RANK = 100


class PizzaEmployee:
    def __init__(self, id: int, first_name: str, last_name: str, address: str, salary: float,
                 start_date: datetime, pizza_surprise=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.salary = salary
        self.start_date = start_date
        self.pizza_surprise = pizza_surprise
        self.set_rank()

    def set_rank(self):
        self.pizza_rank = random.randint(MIN_RANK, MAX_RANK)
        self.pizza_rank_date = datetime.now()

    def is_rank_valid(self, rank_range: int) -> bool:
        return datetime.now() - self.pizza_rank_date <= timedelta(days=rank_range)

    def __eq__(self, other):
        if not isinstance(other, PizzaEmployee):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
