import random
from datetime import datetime, timedelta


class Employee:
    def __init__(self, id, first_name, last_name, address, salary, start_date, pizza_surprise=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.salary = salary
        self.start_date = start_date
        self.pizza_rank = None
        self.pizza_rank_date = None
        self.pizza_surprise = pizza_surprise
        # every employee gets a rank when created
        self.set_rank()

    def set_rank(self):
        """Randomly rank 1-100 and save the date of the rank."""
        self.pizza_rank = random.randint(1, 100)
        self.pizza_rank_date = datetime.now()

    def is_rank_valid(self, rank_range):
        """True if the rank was given within the last rank_range days."""
        return datetime.now() - self.pizza_rank_date <= timedelta(days=rank_range)

    def __eq__(self, other):
        return isinstance(other, Employee) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.id}: {self.first_name} {self.last_name} (rank {self.pizza_rank}, salary {self.salary})"
