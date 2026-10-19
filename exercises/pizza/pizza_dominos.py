from pizza_store import PizzaStore


class PizzaDominos(PizzaStore):
    def calculate_rank(self):
        """Pizza Dominos rank = sum of the employees' ranks."""
        self.rank = sum(employee.pizza_rank for employee in self.employees)
        return self.rank
