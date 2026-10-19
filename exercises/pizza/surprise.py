from abc import ABC, abstractmethod


class Surprise(ABC):
    """Any surprise type must implement activate_surprise()."""

    @abstractmethod
    def activate_surprise(self):
        pass


class FreePizzaSurprise(Surprise):
    def activate_surprise(self):
        print("You got a surprise! Congratulations!")

    def __str__(self):
        return "Free pizza"


class BonusSurprise(Surprise):
    def __init__(self, amount):
        self.amount = amount

    def activate_surprise(self):
        print("You got a surprise! Congratulations!")

    def __str__(self):
        return f"Bonus of {self.amount}"
