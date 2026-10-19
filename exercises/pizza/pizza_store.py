from abc import ABC, abstractmethod


class PizzaStore(ABC):
    def __init__(self, id, name, address, phone_number, employees=None):
        self.id = id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.employees = list(employees) if employees else []
        # the rank is set by the store's own calculation method
        self.rank = self.calculate_rank()

    @property
    def number_of_employees(self):
        return len(self.employees)

    # ---------- rank ----------

    @abstractmethod
    def calculate_rank(self):
        """Each store calculates its rank differently."""
        pass

    def calculate_ranged_rank(self, rank_range):
        """Ask employees with a rank older than rank_range days to rank again, then recalculate."""
        for employee in self.employees:
            if not employee.is_rank_valid(rank_range):
                employee.set_rank()
        return self.calculate_rank()

    # ---------- employees ----------

    def is_employee(self, employee):
        return employee in self.employees

    def hire_employee(self, employee):
        if self.is_employee(employee):
            print(f"{employee.first_name} already works at {self.name}")
            return False
        self.employees.append(employee)
        return True

    def resign_employee(self, employee):
        if not self.is_employee(employee):
            print(f"{employee.first_name} is not an employee of {self.name}")
            return False
        self.take_back_surprise(employee)
        self.employees.remove(employee)
        return True

    def calculate_employee_expenses(self):
        return sum(employee.salary for employee in self.employees)

    # ---------- surprises ----------

    def give_surprise_to_best(self, surprise):
        """Give the surprise to the employee(s) with the highest rank."""
        if not self.employees:
            return []
        best_rank = max(employee.pizza_rank for employee in self.employees)
        best = [employee for employee in self.employees if employee.pizza_rank == best_rank]
        for employee in best:
            employee.pizza_surprise = surprise
            surprise.activate_surprise()
        return best

    def take_back_surprise(self, employee):
        if not self.is_employee(employee):
            return None
        surprise = employee.pizza_surprise
        employee.pizza_surprise = None
        return surprise

    def __str__(self):
        return f"{self.name} (id {self.id}) - {self.number_of_employees} employees, rank {round(self.rank, 2)}"
