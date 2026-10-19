from overrides import overrides

from PizzaStore import PizzaStore


class PizzaHut(PizzaStore):
    @overrides
    def calculate_rank(self) -> float:
        ranks = self.get_ranks()
        self.rank = sum(ranks) / len(ranks) if ranks else 0  # no employees - avoid dividing by 0
        return self.rank
