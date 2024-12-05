from currency_converter import CurrencyConverter

_currency_converter = CurrencyConverter()

class Employee:
    def __init__(self, vardas: str, pavarde: str, salary: int):
        self.vardas = vardas
        self.pavarde = pavarde
        self.salary = _currency_converter.convert(salary, "EUR", "USD")

    def calc_post_tax(self):
        return self.salary * 0.61

    def get_fullname(self):
        return f"{self.vardas} {self.pavarde}"

    def __repr__(self):
        return f"| {self.vardas} {self.pavarde} - {self.salary} |"

    def __str__(self):
        return self.__repr__()
