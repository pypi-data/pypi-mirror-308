class Calculator: 

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def daugyba(self):
        """Grazina daugyba"""
        return self.a * self.b

    def dalyba(self):
        """Grazina dalyba, iskeliame errora jeigu daliname is 0"""
        try:
            return self.a / self.b
        except ZeroDivisionError:
            return "Klaida: Negalima dalinti is 0"