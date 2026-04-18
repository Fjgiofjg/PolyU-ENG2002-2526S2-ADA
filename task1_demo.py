from task1 import fixNum


def demo():
    print("Demo: Fixed-point addition and power (precision 2)")
    a = fixNum(12, 48)  # 12.48
    b = fixNum(2, 16)   # 2.16
    print(f"{a} + {b} = {a.add(b)}")

    c = fixNum(2, 16)   # 2.16
    print(f"{c} ** -2 = {c.power(-2)}")


if __name__ == "__main__":
    demo()
