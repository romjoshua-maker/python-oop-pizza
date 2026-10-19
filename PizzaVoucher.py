from overrides import overrides

from Surprise import Surprise


class PizzaVoucher(Surprise):
    @overrides
    def activate_surprise(self):
        print("You got a surprise! Congratulations!")
