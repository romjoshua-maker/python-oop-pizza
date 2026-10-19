from datetime import date, datetime, timedelta

from employee import Employee
from pizza_dominos import PizzaDominos
from pizza_hut import PizzaHut
from surprise import BonusSurprise, FreePizzaSurprise


def main():
    dana = Employee(1, "Dana", "Levi", "Tel Aviv", 8000, date(2023, 1, 10))
    avi = Employee(2, "Avi", "Cohen", "Haifa", 7500, date(2024, 3, 1))
    noa = Employee(3, "Noa", "Mizrahi", "Jerusalem", 9000, date(2022, 6, 15))
    yossi = Employee(4, "Yossi", "Peretz", "Ramat Gan", 7000, date(2025, 2, 20))

    hut = PizzaHut(1, "Pizza Hut", "Dizengoff 50, Tel Aviv", "03-1234567", [dana, avi])
    dominos = PizzaDominos(2, "Pizza Dominos", "Herzl 10, Haifa", "04-7654321", [noa, yossi])

    print("--- Stores ---")
    print(hut)
    print(dominos)

    print("\n--- Employee expenses ---")
    print(f"{hut.name}: {hut.calculate_employee_expenses()}")
    print(f"{dominos.name}: {dominos.calculate_employee_expenses()}")

    print("\n--- Hiring ---")
    hut.hire_employee(dana)  # already works there
    hut.hire_employee(yossi)
    print(hut)

    print("\n--- Re-rank ---")
    for employee in hut.employees:
        employee.set_rank()
        print(employee)
    print(f"New {hut.name} rank: {hut.calculate_rank()}")

    print("\n--- Ranged rank ---")
    avi.pizza_rank_date = datetime.now() - timedelta(days=5)  # Avi's rank is 5 days old
    old_rank = avi.pizza_rank
    print(f"{hut.name} ranged rank (1 day): {hut.calculate_ranged_rank(1)}")
    print(f"Avi ranked again: {old_rank} -> {avi.pizza_rank}, valid now: {avi.is_rank_valid(1)}")

    print("\n--- Surprises ---")
    best = dominos.give_surprise_to_best(FreePizzaSurprise())
    for employee in best:
        print(f"{employee.first_name} got: {employee.pizza_surprise}")
    hut.give_surprise(avi, BonusSurprise(500))

    print("\n--- Resigning ---")
    hut.resign_employee(noa)  # not an employee of Pizza Hut
    hut.resign_employee(avi)
    print(f"Avi's surprise after resigning: {avi.pizza_surprise}")
    print(hut)


if __name__ == "__main__":
    main()
