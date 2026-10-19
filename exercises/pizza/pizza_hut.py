from pizza_store import PizzaStore


class PizzaHut(PizzaStore):
    def _rank_formula(self, ranks):
        """Pizza Hut rank = average of the employees' ranks."""
        if not ranks:
            return 0
        return sum(ranks) / len(ranks)
