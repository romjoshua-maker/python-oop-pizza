from pizza_store import PizzaStore


class PizzaDominos(PizzaStore):
    def _rank_formula(self, ranks):
        """Pizza Dominos rank = sum of the employees' ranks."""
        return sum(ranks)
