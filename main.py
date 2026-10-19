from datetime import datetime, timedelta

from PizzaDominos import PizzaDominos
from PizzaEmployee import PizzaEmployee
from PizzaHut import PizzaHut
from PizzaVoucher import PizzaVoucher

# ==========================================
# Test Case Output
# ==========================================
if __name__ == '__main__':
    # create employees - fixed ranks so the store ranks can be checked by hand
    employee_1 = PizzaEmployee(1, "John", "Doe", "123 street", 300, datetime.now())
    employee_2 = PizzaEmployee(2, "Jane", "Doe", "456 street", 350, datetime.now())
    employee_3 = PizzaEmployee(3, "James", "Doe", "789 street", 400, datetime.now())
    employee_4 = PizzaEmployee(4, "Jake", "Doe", "1000 street", 500, datetime.now())
    print(f"set_rank() - random rank 1-100: {employee_4.pizza_rank}, rank date: {employee_4.pizza_rank_date}")
    employee_1.pizza_rank, employee_2.pizza_rank, employee_3.pizza_rank, employee_4.pizza_rank = 50, 70, 80, 90

    # create pizza stores - the rank is set in the constructor
    pizza_dominos = PizzaDominos(1, "Pizza Dominos", "1000 street", "+123456", [employee_1, employee_2])
    pizza_hut = PizzaHut(2, "Pizza Hut", "2000 street", "+789101", [employee_3])
    print(f"Pizza Dominos rank (sum): {pizza_dominos.rank}")  # 50 + 70 = 120
    print(f"Pizza Hut rank (average): {pizza_hut.rank}")      # 80

    # hire - a new employee, then the same employee again
    pizza_dominos.hire_employee(employee_4)
    pizza_dominos.hire_employee(employee_4)  # already works here
    print(f"Number of employees: {pizza_dominos.number_of_employees}")       # 3
    print(f"Employee expenses: {pizza_dominos.calculate_employee_expenses()}")  # 300 + 350 + 500 = 1150
    print(f"Pizza Dominos rank after calculate_rank(): {pizza_dominos.calculate_rank()}")  # 50 + 70 + 90 = 210

    # give a surprise to the best employee
    pizza_dominos.give_surprise_to_best_employees(PizzaVoucher())
    print(f"Best employee: {employee_4.first_name}, rank {employee_4.pizza_rank}")
    employee_4.pizza_surprise.activate_surprise()

    # resign - takes the surprise back, then an employee that doesn't work here
    pizza_dominos.resign_employee(employee_4)
    print(f"Number of employees: {pizza_dominos.number_of_employees}")  # 2
    print(f"Surprise after resigning: {employee_4.pizza_surprise}")      # None
    pizza_dominos.resign_employee(employee_3)  # works at Pizza Hut

    # ranged rank - employee_1's rank is 10 days old, employee_2's is 5 days old
    employee_1.pizza_rank_date = datetime.now() - timedelta(days=10)
    employee_2.pizza_rank_date = datetime.now() - timedelta(days=5)
    print(f"Pizza Dominos ranged rank (7 days): {pizza_dominos.calculate_ranged_rank(7)}")
    print(f"Employee 1 ranked again: rank {employee_1.pizza_rank}, date {employee_1.pizza_rank_date}")
    print(f"Employee 2 kept: rank {employee_2.pizza_rank}, date {employee_2.pizza_rank_date}")

    # a store with no employees
    empty_pizza_hut = PizzaHut(3, "Empty Pizza Hut", "3000 street", "+111111", [])
    print(f"Empty Pizza Hut rank: {empty_pizza_hut.rank}")  # 0
