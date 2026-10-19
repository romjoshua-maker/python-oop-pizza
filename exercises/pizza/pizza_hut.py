from pizza_store import PizzaStore


class PizzaHut(PizzaStore):
    def calculate_rank(self):
        """Pizza Hut rank = average of the employees' ranks."""
        if not self.employees:
            self.rank = 0
        else:
            self.rank = sum(employee.pizza_rank for employee in self.employees) / len(self.employees)
        return self.rank
