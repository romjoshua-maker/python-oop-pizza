from abc import ABC, abstractmethod

from PizzaEmployee import PizzaEmployee


class PizzaStore(ABC):
    def __init__(self, id: int, name: str, address: str, phone_number: str, employees: list):
        self.id = id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.employees = []
        for employee in employees:
            self.hire_employee(employee)
        self.rank = self.calculate_rank()

    @property
    def number_of_employees(self) -> int:
        return len(self.employees)

    def calculate_employee_expenses(self) -> float:
        total_salaries = 0
        for employee in self.employees:
            total_salaries += employee.salary
        return total_salaries

    def hire_employee(self, employee: PizzaEmployee):
        if employee in self.employees:
            print(f"{employee.first_name} already works at {self.name}")
            return
        self.employees.append(employee)

    def resign_employee(self, employee: PizzaEmployee):
        if employee not in self.employees:
            print(f"{employee.first_name} doesn't work at {self.name}")
            return
        employee.pizza_surprise = None  # take back the surprise
        self.employees.remove(employee)

    def give_surprise_to_best_employees(self, surprise):
        if not self.employees:
            return
        best_rank = max(self.get_ranks())
        for employee in self.employees:
            if employee.pizza_rank == best_rank:
                employee.pizza_surprise = surprise

    def get_ranks(self) -> list:
        ranks = []
        for employee in self.employees:
            ranks.append(employee.pizza_rank)
        return ranks

    @abstractmethod
    def calculate_rank(self) -> float:
        pass

    def calculate_ranged_rank(self, rank_range: int) -> float:
        for employee in self.employees:
            if not employee.is_rank_valid(rank_range):
                employee.set_rank()
        return self.calculate_rank()
