# task1.py

# Global variable to control the number of required decimal places
# prec = 2 means a multiplier of 10^2 = 100 (e.g., 2 decimal places)
prec = 2  

class fixNum:
    def __init__(self, a=0, b=0):
        """Initialize the fixed-point number."""
        self.a = int(a)
        self.b = int(b)
        
        # Calculate the internal scaled integer
        multiplier = 10 ** prec
        if self.a < 0:
            # If a is negative, the whole number is negative
            scaled = (self.a * multiplier) - self.b
        else:
            scaled = (self.a * multiplier) + self.b
            
        self.normalize(scaled)

    def normalize(self, scaled):
        """Ensure the fixed-point value is properly stored in a and b."""
        multiplier = 10 ** prec
        sign = -1 if scaled < 0 else 1
        abs_val = abs(scaled)
        
        # Reassign a and b based on the scaled value
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

    def add(self, other):
        """Task 1: Addition"""
        res = fixNum()
        res.normalize(self._scaled() + other._scaled())
        return res

    def sub(self, other):
        """Task 2: Subtraction"""
        res = fixNum()
        res.normalize(self._scaled() - other._scaled())
        return res

    def mul(self, other):
        """Task 3: Multiplication"""
        res = fixNum()
        multiplier = 10 ** prec
        total = self._scaled() * other._scaled()
        res.normalize(total // multiplier)
        return res

    def div(self, other):
        """Task 4: Division"""
        divisor = other._scaled()
        if divisor == 0:
            print("Error: Division by zero.")
            return None
            
        res = fixNum()
        multiplier = 10 ** prec
        # Multiply by multiplier first to maintain precision before integer division
        total = (self._scaled() * multiplier) // divisor
        res.normalize(total)
        return res

    def power(self, exponent):
        """Distinction Task: Power of n (int) or another fixNum"""
        if self.a == 0 and self.b == 0:
            print("Error: Base cannot be zero.")
            return None
            
        # Check if exponent is a fixNum object or an integer
        if type(exponent) == int:
            exp_val = exponent
        else:
            exp_val = exponent.to_float()
            
        # Compute power (supports negative ints and fractional values)
        result_float = self.to_float() ** exp_val
        
        # Convert the float result back to a fixed-point scaled integer
        multiplier = 10 ** prec
        res = fixNum()
        res.normalize(int(result_float * multiplier))
        return res

    def __str__(self):
        """Format as a.b based on the precision variable."""
        # e.g., if prec=2 and b=5, it prints as 05
        return f"{self.a}.{self.b:0{prec}d}"