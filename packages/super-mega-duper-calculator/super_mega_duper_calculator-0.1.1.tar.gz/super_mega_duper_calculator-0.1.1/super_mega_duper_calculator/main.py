class Calculator:
    def __init__(self):
        pass

    def subtract(self, a: float, b: float) -> float:
        if self.number_validation(a) and self.number_validation(b):
            return a - b
        else:
            return 'Wrong Input'

    def daugyba (self, a, b):
        return a * b

    def addition(self, a: float , b: float) -> float:
        if self.number_validation(a) and self.number_validation(b):
            return a + b
        else:
            return 'Wrong Input'

    def division(self, a: float , b: float) -> float:
        if self.number_validation(a) and self.number_validation(b) and b != 0:
            return a / b
        else:
            return 'Wrong Input'

    def number_validation(self, number: float) -> bool:
        return isinstance(number, (int, float))

    def square(self, number: float) -> float:
        if self.number_validation(number) and self.number_validation(number):
            return number**2
        else:
            "Wrong Input"