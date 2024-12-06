class Calculator:
    def __init__(self):
        pass

    def subtract(self, a: float, b: float) -> float:
        if self.number_validation(a) and self.number_validation(b):
            return a - b
        else:
            return 'Wrong Input'

    def addition(self, a: float , b: float) -> float:
        if self.number_validation(a) and self.number_validation(b):
            return a + b
        else:
            return 'Wrong Input'

    def number_validation(self, number: float) -> bool:
        return isinstance(number, (int, float))