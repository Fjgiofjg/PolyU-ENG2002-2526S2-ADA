prec = 2  

class fixNum:
    def __init__(self, a=0, b=0):
        """Initialize the fixed-point number."""
        self.a = int(a)
        self.b = int(b)
        
        multiplier = 10 ** prec
        if self.a < 0:
            scaled = (self.a * multiplier) - self.b
        else:
            scaled = (self.a * multiplier) + self.b
            
        self.normalize(scaled)

    def normalize(self, scaled):
        """Ensure the fixed-point value is properly stored in a and b."""
        multiplier = 10 ** prec
        sign = -1 if scaled < 0 else 1
        abs_val = abs(scaled)
        
        self.a = sign * (abs_val // multiplier)
        self.b = abs_val % multiplier

    def _scaled(self):
        """Return the internal scaled integer representation."""
        multiplier = 10 ** prec
        if self.a < 0:
            return (self.a * multiplier) - self.b
        else:
            return (self.a * multiplier) + self.b
    
    def to_float(self):
        """Helper to get a float representation for complex power math."""
        return self._scaled() / (10 ** prec)

    def calculate_basic_ops(choice, num1, num2):
        """Handles the routing, calculation, and printing for basic operations."""
        if choice == "1":
            result = num1.add(num2)
            print(f"Result: {num1} + {num2} = {result}")

    def add(self, other):
        """Task 1: Addition"""
        res = fixNum()
        res.normalize(self._scaled() + other._scaled())
        return res

    def power(self, exponent):
        """Distinction Task: Power of n (int) or another fixNum"""
        if self.a == 0 and self.b == 0:
            print("Error: Base cannot be zero.")
            return None
            
        if type(exponent) == int:
            exp_val = exponent
        else:
            exp_val = exponent.to_float()
            
        result_float = self.to_float() ** exp_val
        
        if isinstance(result_float, complex):
            print("Error: Fractional power of a negative base results in a complex number, which is not supported.")
            return None
        
        multiplier = 10 ** prec
        res = fixNum()
        res.normalize(int(result_float * multiplier))
        return res

    def __str__(self):
        """Format as a.b based on the precision variable."""
        return f"{self.a}.{self.b:0{prec}d}"