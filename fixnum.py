from math import gcd
from typing import Tuple

# Global precision (number of decimal places)
prec = 2


def _round_div(numer: int, denom: int) -> int:
    """Integer division with rounding to nearest.

    Works with negative numerators as well.
    """
    if denom == 0:
        raise ZeroDivisionError("Division by zero in rounding")
    if numer >= 0:
        return (numer + denom // 2) // denom
    else:
        return -((-numer + denom // 2) // denom)


class fixNum:
    """Fixed-point number represented internally as an integer scaled by 10**prec.

    Construction:
    - `fixNum(a, b)` interprets `a` as the integer part and `b` as the
      fractional digits (the number of digits in `b` determines the denominator).
    - Example: `fixNum(123, 456)` => 123.456

    Attributes:
    - `a` and `b`: integer parts suitable for display (note: for negative values
      with |value| < 1, `a` will be 0 and the object will keep a sign internally).
    """

    def __init__(self, a: int = 0, b: int = 0, prec_local: int | None = None):
        self.prec = prec if prec_local is None else prec_local
        self.scale = 10 ** self.prec
        # compute internal scaled integer from given a and b
        self._scaled = self._scaled_from_ab(int(a), int(b))
        self._set_ab_from_scaled()

    def _scaled_from_ab(self, a: int, b: int) -> int:
        # Determine overall sign
        if a < 0 or (a == 0 and b < 0):
            sign = -1
        else:
            sign = 1
        a_abs = abs(a)
        b_abs = abs(b)
        if b_abs == 0:
            denom = 1
            numer = a_abs * denom
        else:
            b_digits = len(str(b_abs))
            denom = 10 ** b_digits
            numer = a_abs * denom + b_abs
        # scaled_abs = round(numer/denom * scale) done with integer arithmetic
        scaled_abs = _round_div(numer * self.scale, denom)
        return sign * scaled_abs

    @classmethod
    def from_scaled(cls, scaled: int, prec_local: int | None = None) -> "fixNum":
        inst = cls(0, 0, prec_local=prec_local)
        inst._scaled = int(scaled)
        inst._set_ab_from_scaled()
        return inst

    def _set_ab_from_scaled(self) -> None:
        s = int(self._scaled)
        sc = self.scale
        sign = -1 if s < 0 else 1
        abs_s = abs(s)
        a = abs_s // sc
        b = abs_s % sc
        # If negative and has integer part, store sign on `a`.
        if sign < 0 and a != 0:
            a = -a
            self._neg = False
        elif sign < 0 and a == 0 and b != 0:
            # Negative number with absolute value < 1: keep a=0 and mark negative
            self._neg = True
            a = 0
        else:
            self._neg = False
        self.a = int(a)
        self.b = int(b)

    def to_scaled(self) -> int:
        return int(self._scaled)

    def to_float(self) -> float:
        return self._scaled / self.scale

    def __str__(self) -> str:
        sgn = "-" if self._scaled < 0 else ""
        abs_s = abs(self._scaled)
        return f"{sgn}{abs_s // self.scale}.{abs_s % self.scale:0{self.prec}d}"

    # --- Basic arithmetic ---
    def add(self, other: "fixNum") -> "fixNum":
        return fixNum.from_scaled(self._scaled + other._scaled, prec_local=self.prec)

    def sub(self, other: "fixNum") -> "fixNum":
        return fixNum.from_scaled(self._scaled - other._scaled, prec_local=self.prec)

    def mul(self, other: "fixNum") -> "fixNum":
        # (s1/scale) * (s2/scale) = (s1*s2) / scale^2 -> scaled result = round((s1*s2)/scale)
        prod = self._scaled * other._scaled
        scaled = _round_div(prod, self.scale)
        return fixNum.from_scaled(scaled, prec_local=self.prec)

    def div(self, other: "fixNum") -> "fixNum":
        if other._scaled == 0:
            raise ZeroDivisionError("Division by zero")
        numer = self._scaled * self.scale
        scaled = _round_div(numer, other._scaled)
        return fixNum.from_scaled(scaled, prec_local=self.prec)

    # --- Power (distinction part) ---
    def power(self, exponent: int | "fixNum") -> "fixNum":
        """Raise this fixed-point number to `exponent`.

        - If `exponent` is an integer (or a `fixNum` that is exactly integer),
          compute exact rational power and round to `prec` decimal places.
        - If `exponent` is a non-integer `fixNum`, compute using floating-point
          then convert to fixed-point (practical approach).
        """
        if isinstance(exponent, fixNum):
            # check if exponent is integer
            if exponent._scaled % exponent.scale == 0:
                n = exponent._scaled // exponent.scale
                return self._power_int(int(n))
            else:
                base = self.to_float()
                expf = exponent.to_float()
                if base <= 0 and not float(expf).is_integer():
                    raise ValueError("Non-integer power of non-positive base yields complex result")
                val = base ** expf
                scaled = int(round(val * self.scale))
                return fixNum.from_scaled(scaled, prec_local=self.prec)
        else:
            return self._power_int(int(exponent))

    def _power_int(self, n: int) -> "fixNum":
        if n == 0:
            return fixNum.from_scaled(self.scale, prec_local=self.prec)  # 1.00
        p = self._scaled
        q = self.scale
        if n > 0:
            p_abs = abs(p)
            num = pow(p_abs, n)
            den = pow(q, n)
            scaled_abs = _round_div(num * self.scale, den)
            sign = -1 if p < 0 and (n % 2 == 1) else 1
            return fixNum.from_scaled(sign * scaled_abs, prec_local=self.prec)
        else:
            k = -n
            if p == 0:
                raise ZeroDivisionError("Zero cannot be raised to negative power")
            p_abs = abs(p)
            num = pow(q, k)
            den = pow(p_abs, k)
            scaled_abs = _round_div(num * self.scale, den)
            sign = -1 if p < 0 and (k % 2 == 1) else 1
            return fixNum.from_scaled(sign * scaled_abs, prec_local=self.prec)


__all__ = ["fixNum", "prec"]
