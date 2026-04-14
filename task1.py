class fixNum:
    def __init__(self, a=0, b=0):
        self.a = int(a)
        self.b = int(b)
        self.normalize()

    def normalize(self):
        """Ensure the fixed-point value is stored in the internal scaled form."""
        scaled = self._scaled()
        self.a = scaled // 100
        self.b = scaled % 100

    def _scaled(self):
        return self.a * 100 + self.b

    def add(self, other):
        total = self._scaled() + other._scaled()
        return fixNum(total // 100, total % 100)

    def sub(self, other):
        total = self._scaled() - other._scaled()
        return fixNum(total // 100, total % 100)

    def mul(self, other):
        total = self._scaled() * other._scaled()
        result_scaled = total // 100
        return fixNum(result_scaled // 100, result_scaled % 100)

    def div(self, other):
        divisor = other._scaled()
        if divisor == 0:
            return None
        result_scaled = (self._scaled() * 100) // divisor
        return fixNum(result_scaled // 100, result_scaled % 100)

    def power(self, exponent):
        """Raise the fixed-point number to a non-negative integer power."""
        exponent = int(exponent)
        if exponent < 0:
            raise ValueError("Exponent must be non-negative")
        if exponent == 0:
            return fixNum(1, 0)
        result = pow(self._scaled(), exponent)
        scaled_result = result // (100 ** (exponent - 1))
        return fixNum(scaled_result // 100, scaled_result % 100)

    def __str__(self):
        scaled = self._scaled()
        sign = "-" if scaled < 0 else ""
        abs_val = abs(scaled)
        return f"{sign}{abs_val // 100}.{abs_val % 100:02d}"
