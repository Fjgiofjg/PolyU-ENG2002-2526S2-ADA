class fixNum:
    def __init__(self, a=0, b=0):
        self.a = int(a)
        self.b = int(b)
        self.normalize()

    def normalize(self):
        if self.b >= 100:
            self.a += self.b // 100
            self.b = self.b % 100
        elif self.b < 0:
            borrow = (-self.b + 99) // 100
            self.a -= borrow
            self.b += borrow * 100

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

    def show(self):
        sign = "-" if self.a < 0 else ""
        print(f"{self.a}.{abs(self.b):02d}")

    def __str__(self):
        return f"{self.a}.{self.b:02d}"


# ── Extra Task ─────────────────────────────────────────────────────────────────

def int_to_binary(n, bits=8):
    """Return unsigned binary string of n using the given number of bits."""
    if n == 0:
        return "0" * bits
    result = []
    for _ in range(bits):
        result.append(str(n & 1))
        n >>= 1
    return "".join(reversed(result))


def frac_to_binary(b, bits=8):
    """
    Convert the fractional part b/100 to a binary string of the given length.
    Uses the repeated-doubling algorithm.
    """
    value = b / 100.0
    result = []
    for _ in range(bits):
        value *= 2
        if value >= 1.0:
            result.append("1")
            value -= 1.0
        else:
            result.append("0")
    return "".join(result)


def to_binary(num, int_bits=8, frac_bits=8):
    """Display the binary representation of a fixNum."""
    negative = num.a < 0
    abs_int = abs(num.a)
    int_bin = int_to_binary(abs_int, int_bits)
    frac_bin = frac_to_binary(num.b, frac_bits)
    sign_str = "-" if negative else " "
    print(f"Binary representation of {num}:")
    print(f"  {sign_str}{int_bin}.{frac_bin}")
    print(f"  Integer part  : {sign_str}{int_bin} (= {abs_int})")
    print(f"  Fractional part: .{frac_bin} (≈ {num.b / 100:.6f})")


# ── Menu helpers ────────────────────────────────────────────────────────────────

def get_fixNum(label=""):
    a = int(input(f"Enter {label}integer part a: "))
    b = int(input(f"Enter {label}fractional part b: "))
    return fixNum(a, b)


def main():
    while True:
        print("\nFixed-Point Number Calculator")
        print("1. Add two fixed-point numbers")
        print("2. Subtract two fixed-point numbers")
        print("3. Multiply two fixed-point numbers")
        print("4. Divide two fixed-point numbers")
        print("5. [Extra Task] Show binary representation")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            num1 = get_fixNum("first number ")
            num2 = get_fixNum("second number ")
            result = num1.add(num2)
            print("Result:")
            result.show()

        elif choice == "2":
            num1 = get_fixNum("first number ")
            num2 = get_fixNum("second number ")
            result = num1.sub(num2)
            print("Result:")
            result.show()

        elif choice == "3":
            num1 = get_fixNum("first number ")
            num2 = get_fixNum("second number ")
            result = num1.mul(num2)
            print("Result:")
            result.show()

        elif choice == "4":
            num1 = get_fixNum("first number ")
            num2 = get_fixNum("second number ")
            result = num1.div(num2)
            if result is None:
                print("Error: Division by zero.")
            else:
                print("Result:")
                result.show()

        elif choice == "5":
            num = get_fixNum()
            to_binary(num)

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
