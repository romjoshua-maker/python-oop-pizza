from abc import ABC, abstractmethod


class Surprise(ABC):
    @abstractmethod
    def activate_surprise(self):
        pass
