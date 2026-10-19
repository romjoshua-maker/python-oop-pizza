from overrides import overrides

from PizzaStore import PizzaStore


class PizzaDominos(PizzaStore):
    @overrides
    def calculate_rank(self) -> float:
        self.rank = sum(self.get_ranks())
        return self.rank
