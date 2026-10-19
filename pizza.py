import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from overrides import overrides

MIN_RANK = 1
MAX_RANK = 100
EMPTY_STORE_RANK = 0  # a store with no employees has no ranks to calculate
MIN_RANK_RANGE = 0
OLD_RANK_DAYS = 30  # used in the tests to fake an old rank
DATE_FORMAT = '%d/%m/%Y'


# ==========================================
# Surprise interface
# ==========================================
class Surprise(ABC):
    @abstractmethod
    def activate_surprise(self):
        pass


class PizzaVoucher(Surprise):
    def activate_surprise(self):
        print("You got a surprise! Congratulations!")


# Not a Surprise subclass - works anyway because it has activate_surprise() (duck typing)
class FreeDessert:
    def activate_surprise(self):
        print("You got a surprise! Congratulations!")


# ==========================================
# Employee
# ==========================================
class PizzaEmployee:
    def __init__(self, id: int, first_name: str, last_name: str, address: str, salary: float,
                 start_date: datetime, pizza_rank: int = None, pizza_rank_date: datetime = None,
                 pizza_surprise=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.salary = salary
        self.start_date = start_date
        self.pizza_rank = pizza_rank
        self.pizza_rank_date = pizza_rank_date
        self.pizza_surprise = pizza_surprise
        # every employee has a rank when created - if none was given, rank now
        if self.pizza_rank is None or self.pizza_rank_date is None:
            self.set_rank()

    def set_rank(self):
        self.pizza_rank = random.randint(MIN_RANK, MAX_RANK)
        self.pizza_rank_date = datetime.now()

    def is_rank_valid(self, rank_range: int) -> bool:
        # not valid = the rank is older than rank_range days
        return datetime.now() - self.pizza_rank_date <= timedelta(days=rank_range)

    def use_surprise(self):
        if self.pizza_surprise is None:  # the surprise can be None - never call a method on None
            print(f"{self.first_name} {self.last_name} has no surprise")
            return
        self.pizza_surprise.activate_surprise()

    def __eq__(self, other):
        if not isinstance(other, PizzaEmployee):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return (f"Employee #{self.id}: {self.first_name} {self.last_name}, Salary: {self.salary:.2f}, "
                f"Rank: {self.pizza_rank} (ranked {self.pizza_rank_date.strftime(DATE_FORMAT)}), "
                f"Surprise: {'yes' if self.pizza_surprise is not None else 'no'}")


# ==========================================
# Stores
# ==========================================
class PizzaStore(ABC):
    def __init__(self, id: int, name: str, address: str, phone_number: str, employees: list = None):
        self.id = id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.employees = []
        self.number_of_employees = 0
        # hire one by one, so the same checks run for the starting employees too
        if employees is not None:
            for employee in employees:
                self.hire_employee(employee)
        # the rank is set in the constructor with the store's own calculation
        self.rank = self.calculate_rank()

    def calculate_employee_expenses(self) -> float:
        total_salaries = 0
        for employee in self.employees:
            total_salaries += employee.salary
        return total_salaries

    def hire_employee(self, employee: PizzaEmployee):
        if employee in self.employees:  # uses __eq__ - same id means the same employee
            print(f"{employee.first_name} {employee.last_name} already works at {self.name}")
            return
        self.employees.append(employee)
        self.number_of_employees = len(self.employees)
        print(f"{employee.first_name} {employee.last_name} was hired at {self.name}")

    def resign_employee(self, employee: PizzaEmployee):
        if employee not in self.employees:
            print(f"{employee.first_name} {employee.last_name} doesn't work at {self.name}")
            return
        self.take_back_surprise(employee)
        self.employees.remove(employee)
        self.number_of_employees = len(self.employees)
        print(f"{employee.first_name} {employee.last_name} resigned from {self.name}")

    def take_back_surprise(self, employee: PizzaEmployee):
        if employee.pizza_surprise is None:  # nothing to take back
            return
        employee.pizza_surprise = None
        print(f"Surprise taken back from {employee.first_name} {employee.last_name}")

    def give_surprise_to_best_employees(self, surprise):
        if not self.employees:  # max() of an empty list raises ValueError
            print(f"{self.name} has no employees - no one gets a surprise")
            return
        best_rank = max(self.get_ranks())
        # a tie at the top - every employee with the best rank gets the surprise
        for employee in self.employees:
            if employee.pizza_rank == best_rank:
                employee.pizza_surprise = surprise
                print(f"{employee.first_name} {employee.last_name} (rank {best_rank}) got a new surprise")

    def get_ranks(self) -> list:
        ranks = []
        for employee in self.employees:
            ranks.append(employee.pizza_rank)
        return ranks

    @abstractmethod
    def calculate_rank(self) -> float:
        pass

    def calculate_ranged_rank(self, rank_range: int) -> float:
        if rank_range < MIN_RANK_RANGE:
            print(f"Invalid rank range: {rank_range}")
            return self.rank
        # an employee whose rank isn't valid is asked to rank again (also updates the rank date)
        for employee in self.employees:
            if not employee.is_rank_valid(rank_range):
                print(f"Rank of {employee.first_name} {employee.last_name} is not valid - ranking again")
                employee.set_rank()
        # reuse the store's own rank logic (average / sum)
        return self.calculate_rank()

    def print_store(self):
        print(f"{self.name} (#{self.id}), {self.address}, Phone: {self.phone_number}, "
              f"Employees: {self.number_of_employees}, Rank: {self.rank:.2f}")
        for employee in self.employees:
            print(f"   {employee}")


class PizzaHut(PizzaStore):
    @overrides
    def calculate_rank(self) -> float:
        if not self.employees:  # avoid ZeroDivisionError on an empty store
            self.rank = EMPTY_STORE_RANK
            return self.rank
        ranks = self.get_ranks()
        self.rank = sum(ranks) / len(ranks)
        return self.rank


class PizzaDominos(PizzaStore):
    @overrides
    def calculate_rank(self) -> float:
        # sum() of an empty list is 0, so an empty store needs no special case
        self.rank = sum(self.get_ranks())
        return self.rank


# ==========================================
# Test Case Output
# ==========================================
if __name__ == '__main__':
    # fixed ranks and dates so the store ranks can be checked by hand
    old_date = datetime.now() - timedelta(days=OLD_RANK_DAYS)
    dana = PizzaEmployee(1, "Dana", "Levi", "Herzl 5, Tel Aviv", 8000, datetime(2024, 3, 1),
                         pizza_rank=80, pizza_rank_date=datetime.now())
    avi = PizzaEmployee(2, "Avi", "Cohen", "Ben Yehuda 10, Haifa", 7500, datetime(2023, 6, 15),
                        pizza_rank=60, pizza_rank_date=datetime.now())
    noa = PizzaEmployee(3, "Noa", "Mizrahi", "Weizmann 3, Rehovot", 9000, datetime(2022, 1, 10),
                        pizza_rank=40, pizza_rank_date=old_date)
    yossi = PizzaEmployee(4, "Yossi", "Peretz", "Rothschild 20, Tel Aviv", 7000, datetime(2025, 2, 1),
                          pizza_rank=95, pizza_rank_date=old_date)
    # a new employee without a rank - ranked in the constructor
    maya = PizzaEmployee(5, "Maya", "Katz", "Hagana 7, Holon", 6500, datetime.now())

    print("--- 1. set_rank() - random int 1-100 + today's date ---")
    print(f"Maya (new, no rank given): rank {maya.pizza_rank}, ranked {maya.pizza_rank_date.strftime(DATE_FORMAT)}")
    maya.set_rank()
    print(f"Maya ranked again: rank {maya.pizza_rank}, ranked {maya.pizza_rank_date.strftime(DATE_FORMAT)}")

    print("\n--- 2. Constructor sets the rank (Pizza Hut = average, Pizza Dominos = sum) ---")
    pizza_hut = PizzaHut(1, "Pizza Hut Dizengoff", "Dizengoff 50, Tel Aviv", "03-1234567", [dana, avi, noa])
    pizza_dominos = PizzaDominos(2, "Pizza Dominos Azrieli", "Menachem Begin 132, Tel Aviv", "03-7654321",
                                 [yossi, maya])
    print(f"{pizza_hut.name} rank: {pizza_hut.rank:.2f}  (expected average: {(80 + 60 + 40) / 3:.2f})")
    print(f"{pizza_dominos.name} rank: {pizza_dominos.rank:.2f}  (expected sum: {95 + maya.pizza_rank})")

    print("\n--- 3. hire_employee() + number_of_employees ---")
    pizza_dominos.hire_employee(avi)  # works in another store too - the rule is per store
    print(f"{pizza_dominos.name} employees: {pizza_dominos.number_of_employees}")

    print("\n--- 4. hire_employee() - duplicate (same object, and a different object with the same id) ---")
    pizza_hut.hire_employee(dana)
    dana_copy = PizzaEmployee(1, "Dana", "Levi", "Herzl 5, Tel Aviv", 8000, datetime(2024, 3, 1))
    pizza_hut.hire_employee(dana_copy)
    print(f"{pizza_hut.name} employees: {pizza_hut.number_of_employees}")

    print("\n--- 5. calculate_employee_expenses() ---")
    print(f"{pizza_hut.name}: {pizza_hut.calculate_employee_expenses():.2f}")          # 8000 + 7500 + 9000
    print(f"{pizza_dominos.name}: {pizza_dominos.calculate_employee_expenses():.2f}")  # 7000 + 6500 + 7500

    print("\n--- 6. calculate_rank() - called again after a change (polymorphism) ---")
    print(f"{pizza_dominos.name} rank before: {pizza_dominos.rank:.2f} (Avi was hired after the constructor)")
    for store in [pizza_hut, pizza_dominos]:
        print(f"{store.name}: {store.calculate_rank():.2f}")
    print(f"Pizza Dominos expected sum: {sum([95, maya.pizza_rank, 60])}")

    print(f"\n--- 7. calculate_ranged_rank(7) - Noa and Yossi were ranked {OLD_RANK_DAYS} days ago ---")
    print(f"Noa before: rank {noa.pizza_rank}, ranked {noa.pizza_rank_date.strftime(DATE_FORMAT)}")
    print(f"{pizza_hut.name} ranged rank: {pizza_hut.calculate_ranged_rank(7):.2f}")
    print(f"Noa after: rank {noa.pizza_rank}, ranked {noa.pizza_rank_date.strftime(DATE_FORMAT)}")
    print(f"Check: average of {pizza_hut.get_ranks()} = "
          f"{sum(pizza_hut.get_ranks()) / len(pizza_hut.get_ranks()):.2f}")
    print(f"{pizza_dominos.name} ranged rank: {pizza_dominos.calculate_ranged_rank(7):.2f}")
    print(f"Check: sum of {pizza_dominos.get_ranks()} = {sum(pizza_dominos.get_ranks())}")

    print("\n--- 8. calculate_ranged_rank() - every rank is valid, no one ranks again ---")
    print(f"{pizza_hut.name} ranged rank: {pizza_hut.calculate_ranged_rank(7):.2f}")

    print("\n--- 9. calculate_ranged_rank() - invalid rank range ---")
    print(f"{pizza_hut.name} ranged rank: {pizza_hut.calculate_ranged_rank(-5):.2f}")

    print("\n--- 10. give_surprise_to_best_employees() - one best employee, then a tie ---")
    pizza_hut.give_surprise_to_best_employees(PizzaVoucher())
    for employee in pizza_hut.employees:
        employee.use_surprise()  # only the best employee prints the message
    yossi.pizza_rank = 100  # Yossi and Avi both have the top rank at Pizza Dominos
    avi.pizza_rank = 100
    pizza_dominos.give_surprise_to_best_employees(FreeDessert())  # duck typing - not a Surprise subclass
    yossi.use_surprise()
    avi.use_surprise()

    print("\n--- 11. resign_employee() - with a surprise, without a surprise, not working here ---")
    pizza_dominos.resign_employee(avi)  # has a surprise - taken back
    print(f"Avi's surprise after resigning: {avi.pizza_surprise}")
    avi.use_surprise()
    pizza_dominos.resign_employee(maya)  # no surprise
    pizza_dominos.resign_employee(noa)   # works at Pizza Hut, not at Pizza Dominos
    pizza_dominos.resign_employee(maya)  # already resigned
    print(f"{pizza_dominos.name} employees: {pizza_dominos.number_of_employees}, "
          f"expenses: {pizza_dominos.calculate_employee_expenses():.2f}")

    print("\n--- 12. Empty stores - no ZeroDivisionError / ValueError ---")
    empty_pizza_hut = PizzaHut(3, "Pizza Hut Eilat", "Hatmarim 1, Eilat", "08-1111111")
    empty_pizza_dominos = PizzaDominos(4, "Pizza Dominos Eilat", "Hatmarim 2, Eilat", "08-2222222")
    print(f"Rank: {empty_pizza_hut.rank:.2f}")
    print(f"Rank: {empty_pizza_dominos.rank:.2f}")
    print(f"Ranged rank: {empty_pizza_hut.calculate_ranged_rank(7):.2f}")
    print(f"Expenses: {empty_pizza_dominos.calculate_employee_expenses():.2f}")
    empty_pizza_hut.give_surprise_to_best_employees(PizzaVoucher())

    print("\n--- 13. PizzaStore is abstract - can't be created directly ---")
    try:
        store = PizzaStore(5, "Generic Pizza", "Nowhere 1", "000")
    except TypeError as error:
        print(f"TypeError: {error}")

    print("\n--- 14. Final state ---")
    for store in [pizza_hut, pizza_dominos, empty_pizza_hut]:
        store.print_store()
