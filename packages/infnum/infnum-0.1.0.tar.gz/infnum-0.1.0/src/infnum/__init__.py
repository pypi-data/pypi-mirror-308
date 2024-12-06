from dataclasses import dataclass, field
import math
from operator import itemgetter
from typing import Self, Mapping
import jax.numpy as jnp
from jaxtyping import Float


SUPERSCRIPT_MAP = str.maketrans("0123456789-.", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻·")


def _to_superscript(
    n: float | int, superscript_map: dict[int, int] = SUPERSCRIPT_MAP
) -> str:
    """Convert a number to its superscript representation."""
    return str(n).translate(superscript_map)


type Exponent = Float
type Coefficient = Float

# TODO add @jit


@dataclass
class LeviCivitaNumber:
    """Represents a Levi-Civita number as a sparse series of terms.

    The terms are stored as a dictionary mapping exponents to coefficients.
    Only non-zero coefficients are stored.
    """

    terms: dict[Exponent, Coefficient] = field(default_factory=lambda: {0: 0.0})
    type CoeffLike = float | int | LeviCivitaNumber | Self

    @classmethod
    def from_number(cls, n: float | int) -> "LeviCivitaNumber":
        """Convert a regular number to a LeviCivita number.

        Args:
            n: A regular number (float or int)

        Returns:
            A LeviCivita number representing the constant term
        """
        return LeviCivitaNumber({0: float(n)} if n != 0 else {})

    def __post_init__(self) -> None:
        """Convert values to JAX arrays and remove zero terms.

        This ensures:
        1. All coefficients are JAX arrays
        2. Zero terms are removed
        3. All exponents are floats for consistency
        """
        self.terms = {
            float(exponent): jnp.asarray(coefficient)
            for exponent, coefficient in self.terms.items()
            if not jnp.isclose(coefficient, 0.0)
        }

    def __add__(self, other: CoeffLike) -> "LeviCivitaNumber":
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
        return LeviCivitaNumber(
            {
                exp: self.terms.get(exp, 0.0) + other.terms.get(exp, 0.0)
                for exp in set(self.terms.keys()) | set(other.terms.keys())
            }
        )

    def __radd__(self, other: CoeffLike) -> "LeviCivitaNumber":
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
        return other + self

    def __iadd__(self, other: CoeffLike) -> "LeviCivitaNumber":
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
        self = self + other
        return self

    def __mul__(self, other: CoeffLike) -> "LeviCivitaNumber":
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
        new_terms: dict[Exponent, Coefficient] = {}
        # Multiply each term from self with each term from other
        for exp1, coeff1 in self.terms.items():
            for exp2, coeff2 in other.terms.items():
                exp = exp1 + exp2
                coeff = coeff1 * coeff2
                new_terms[exp] = new_terms.get(exp, 0.0) + coeff
        return LeviCivitaNumber(new_terms)

    def __pow__(self, other: int) -> "LeviCivitaNumber":
        if other < 0:  # x^-n = 1/x^n
            return ~(self ** (-other))
        elif other == 0:  # x^0 = 1
            return LeviCivitaNumber.one()
        else:  # Exponentiation by squaring
            result = LeviCivitaNumber.one()
            base, exp = self, other
            while exp > 0:
                if exp % 2 == 1:
                    result = result * base
                base, exp = base * base, exp // 2
            return result

    def __invert__(self, num_terms: int = 8) -> "LeviCivitaNumber":
        """Reciprocal of a Levi-Civita number.

        For pure numbers (single term), directly compute reciprocal.
        For non-pure numbers, normalize by largest term and use series expansion.
        """
        # Fast path for pure numbers (single term)
        if len(self.terms) == 0:  # division by zero
            raise ZeroDivisionError("Division by zero")
        elif len(self.terms) == 1:
            exp, coeff = next(iter(self.terms.items()))
            if jnp.isclose(coeff, 0.0):
                raise ZeroDivisionError("Division by zero")
            return LeviCivitaNumber({-exp: 1.0 / coeff})

        # Get largest term (highest exponent)
        sorted_terms = sorted(self.terms.items(), key=lambda x: x[0], reverse=True)
        largest_term = LeviCivitaNumber({sorted_terms[0][0]: sorted_terms[0][1]})
        largest_exp, largest_coeff = sorted_terms[0]
        # Normalize by dividing by largest term
        normalized_terms = {
            exp - largest_exp: coeff / largest_coeff
            for exp, coeff in self.terms.items()
        }
        normalized = LeviCivitaNumber(normalized_terms)

        # Compute εₓ = normalized - 1 (since standard part is now 1)
        eps_x = normalized - LeviCivitaNumber.from_number(1)

        # Use series expansion: 1 / (1 + εₓ) ≈ Σ (-εₓ)^k for k = 0 to n - 1
        result = sum((-eps_x) ** k for k in range(num_terms))

        # Multiply by reciprocal of largest term
        return ~largest_term * result

    def __truediv__(self, other: CoeffLike) -> "LeviCivitaNumber":
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
        return self * ~other

    def __rmul__(self, other: float | int) -> "LeviCivitaNumber":
        return self * other

    def __neg__(self) -> "LeviCivitaNumber":
        return LeviCivitaNumber(
            {exponent: -coefficient for exponent, coefficient in self.terms.items()}
        )

    def __sub__(self, other: CoeffLike) -> "LeviCivitaNumber":
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
        return self + (-other)

    def __rsub__(self, other: CoeffLike) -> "LeviCivitaNumber":
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
        return other - self

    def __str__(self) -> str:
        """Pretty-print representation of a Levi-Civita number."""
        if not self.terms:
            return "0"

        def format_coefficient(coeff: float, is_standard_part: bool) -> str:
            """Format a coefficient according to its value and position."""
            is_negative = coeff < 0
            abs_coeff = abs(coeff)

            if jnp.isclose(abs_coeff, 1.0):
                if is_standard_part:  # Standard part
                    return "-1" if is_negative else "1"
                else:  # Non-standard part
                    return "-" if is_negative else ""

            if float(abs_coeff).is_integer():
                abs_coeff_str = str(int(abs_coeff))
            else:
                abs_coeff_str = str(abs_coeff)

            return f"-{abs_coeff_str}" if is_negative else abs_coeff_str

        def format_term(exp: float, coeff_str: str) -> str:
            """Format a single term with its exponent."""
            if float(exp).is_integer():
                exp = int(exp)

            if exp == 0:
                return coeff_str
            elif exp == 1:
                return f"{coeff_str}ε"
            else:
                return f"{coeff_str}ε{_to_superscript(exp)}"

        def format_term_with_sign(term: str, is_first: bool) -> str:
            """Add appropriate spacing and signs between terms."""
            if is_first:
                return term

            if term.startswith("-"):
                return f"- {term[1:]}"
            else:
                return f"+ {term}"

        # Sort terms by exponent
        sorted_terms = sorted(self.terms.items(), key=itemgetter(0))
        formatted_terms: list[str] = []

        for i, (exp, coeff) in enumerate(sorted_terms):
            # Format the coefficient
            coeff_str = format_coefficient(coeff, is_standard_part=(exp == 0))

            # Format the term with its exponent
            term = format_term(exp, coeff_str)

            # Add appropriate spacing and signs
            if term:  # Skip empty terms
                formatted_term = format_term_with_sign(term, is_first=(i == 0))
                formatted_terms.append(formatted_term)

        return " ".join(formatted_terms)

    def __eq__(self, other: CoeffLike, tol: float = 1e-5) -> bool:
        """
        Check if two Levi-Civita numbers are equal within a given tolerance.

        The coefficients are compared in order of their exponents, from most negative (infinite terms)
        to most positive (infinitesimal terms), by placing them in sorted lists.

        Parameters:
            other (LeviCivitaNumber): The other number to compare.
            tol (float): Tolerance for floating point comparison.

        Returns:
            bool: True if the numbers are equal within the tolerance, False otherwise.
        """
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
        return self.is_close_to(other, tol)

    def __lt__(self, other: CoeffLike) -> bool:
        """
        Compare two Levi-Civita numbers for ordering.

        Accounts for the fact that negative exponents correspond to infinite numbers.
        The comparison is performed by placing the coefficients in sorted lists according to exponents,
        and comparing these lists lexicographically.

        Returns:
            bool: True if self is less than other, False otherwise.
        """
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)

        # Get all exponents and sort them from smallest (most negative) to largest
        all_exponents = sorted(set(self.terms.keys()) | set(other.terms.keys()))

        self_coeffs = [self.terms.get(exp, 0.0) for exp in all_exponents]
        other_coeffs = [other.terms.get(exp, 0.0) for exp in all_exponents]
        # Compare lists lexicographically
        return self_coeffs < other_coeffs

    def __le__(self, other: Self | float | int) -> bool:
        return self < other or self == other

    def __gt__(self, other: Self | float | int) -> bool:
        return not self <= other

    def __ge__(self, other: Self | float | int) -> bool:
        return self > other or self == other

    def __ne__(self, other: Self | float | int) -> bool:
        return not self == other

    @property
    def is_pure(self) -> bool:
        return len(self.terms) == 1 and 0 in self.terms

    @property
    def is_zero(self) -> bool:
        return not self.terms

    @property
    def is_infinite(self) -> bool:
        return any(exp < 0 for exp in self.terms.keys())

    @property
    def is_infinitesimal(self) -> bool:
        return all(exp > 0 for exp in self.terms.keys())

    @property
    def is_standard(self) -> bool:
        return not self.is_infinite and not self.is_infinitesimal

    @property
    def infinite_part(self) -> "LeviCivitaNumber":
        """Infinite terms of a Levi-Civita number."""
        return LeviCivitaNumber(
            {exp: coeff for exp, coeff in self.terms.items() if exp < 0}
        )

    @property
    def infinitesimal_part(self) -> "LeviCivitaNumber":
        """Infinitesimal terms of a Levi-Civita number."""
        return LeviCivitaNumber(
            {exp: coeff for exp, coeff in self.terms.items() if exp > 0}
        )

    @property
    def standard_part(self) -> "LeviCivitaNumber":
        """Standard part of a Levi-Civita number."""
        return LeviCivitaNumber(
            {exp: coeff for exp, coeff in self.terms.items() if exp == 0}
        )

    def exp(self, num_terms: int = 8) -> "LeviCivitaNumber":
        """Taylor series expansion of e^x up to num_terms terms."""
        return sum(
            ((self**n / math.factorial(n)) for n in range(num_terms)),
            start=LeviCivitaNumber.one(),
        )  # 0^0 = 1

    @classmethod
    def zero(cls) -> "LeviCivitaNumber":
        return LeviCivitaNumber({0: 0.0})

    @classmethod
    def one(cls) -> "LeviCivitaNumber":
        return LeviCivitaNumber({0: 1.0})

    @classmethod
    def eps(cls) -> "LeviCivitaNumber":
        """Infinitesimal unit. Stands for "epsilon"."""
        return LeviCivitaNumber({1: 1.0})

    @classmethod
    def ε(cls) -> "LeviCivitaNumber":
        """Alias for infinitesimal unit. Stands for "epsilon"."""
        return LeviCivitaNumber.eps()

    @classmethod
    def H(cls) -> "LeviCivitaNumber":
        """Infinite unit. `H` for "hyperfinite"."""
        return LeviCivitaNumber({-1: 1.0})
    def is_close_to(self, other: CoeffLike, tol: float = 1e-6, max_order: float | None = None) -> bool:
        """Check if two Levi-Civita numbers are close within a specified tolerance.
        
        Args:
            other: The number to compare against
            tol: Tolerance for coefficient comparison
            max_order: Maximum order of terms to consider. Terms with higher order are ignored.
                      If None, all terms are considered.
        """
        if isinstance(other, (float, int)):
            other = LeviCivitaNumber.from_number(other)
            
        # Get all exponents up to max_order
        exponents = set(self.terms.keys()).union(other.terms.keys())
        if max_order is not None:
            exponents = {exp for exp in exponents if exp <= max_order}
            
        return all(
            jnp.isclose(self.terms.get(exp, 0.0), other.terms.get(exp, 0.0), atol=tol)
            for exp in exponents
        )


print(LeviCivitaNumber.one() == LeviCivitaNumber.one())
print(LeviCivitaNumber.one() - 2 * LeviCivitaNumber.one())
print(LeviCivitaNumber.eps() < LeviCivitaNumber.one() < LeviCivitaNumber.H())
