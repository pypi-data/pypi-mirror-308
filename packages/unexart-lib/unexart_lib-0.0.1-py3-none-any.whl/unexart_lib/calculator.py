class calculator:
    """ Класс для вычисления простых операций. """
    def __init__(self, num1, operator, num2):
        self.num1 = num1
        self.num2 = num2
        self.operator = operator

    def do(self):
        if not self.validate_data():
            raise TypeError("Ошибка: данные должны быть числовыми.")
        if self.operator == "+":
            return self.num1 + self.num2
        elif self.operator == "-":
            return self.num1 - self.num2
        elif self.operator == "*":
            return self.num1 * self.num2
        elif self.operator == "/":
            if self.num2 == 0:
                raise ZeroDivisionError("Ошибка: деление на ноль")
            else:
                return self.num1 / self.num2
        else:
            raise ValueError("Ошибка: недопустимый оператор")

    def validate_data(self):
        if not (isinstance(self.num1, (int, float))
                and isinstance(self.num2, (int, float))):
            return False
        return True
