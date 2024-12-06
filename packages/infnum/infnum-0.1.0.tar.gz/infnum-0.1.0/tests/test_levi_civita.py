import unittest
from infnum import LeviCivitaNumber
from hypothesis import given, assume, strategies as st
from hypothesis.strategies import composite
from _pytest.assertion import truncate

# Prevent pytest from cutting off input.
truncate.DEFAULT_MAX_LINES = 9999
truncate.DEFAULT_MAX_CHARS = 9999


@composite
def levi_civita_numbers(
    draw,
    min_exponent: int = -5,
    max_exponent: int = 5,
    min_coefficient: float = -10.0,
    max_coefficient: float = 10.0,
    max_terms: int = 5,
) -> LeviCivitaNumber:
    """Composite strategy for generating random Levi-Civita numbers."""
    use_special_case = draw(st.booleans())
    if use_special_case:
        special_cases = [
            LeviCivitaNumber.zero(),
            LeviCivitaNumber.one(),
            LeviCivitaNumber.eps(),
            LeviCivitaNumber.H(),
        ]
        special_case = draw(st.sampled_from(special_cases))
        return special_case

    num_terms = draw(st.integers(min_value=1, max_value=max_terms))

    # Generate unique exponents
    exponents = draw(
        st.lists(
            st.integers(min_value=min_exponent, max_value=max_exponent),
            min_size=num_terms,
            max_size=num_terms,
            unique=True,
        )
    )

    # Generate coefficients corresponding to the exponents
    coefficients = draw(
        st.lists(
            st.floats(
                min_value=min_coefficient,
                max_value=max_coefficient,
                allow_nan=False,
                allow_infinity=False,
                exclude_min=True,
                exclude_max=True,
                width=32,
            ),
            min_size=num_terms,
            max_size=num_terms,
        )
    )

    # Combine exponents and coefficients into a terms dictionary
    terms = dict(zip(exponents, coefficients))

    return LeviCivitaNumber(terms)


class TestLeviCivitaNumber(unittest.TestCase):
    def setUp(self):
        # Common test numbers
        self.zero = LeviCivitaNumber.zero()
        self.one = LeviCivitaNumber.one()
        self.eps = LeviCivitaNumber.eps()
        self.eps_squared = LeviCivitaNumber({2: 1.0})
        self.complex_num = LeviCivitaNumber({0: 1.0, 1: 2.0, 2: 3.0})
        # Test high-order term
        self.high_order = LeviCivitaNumber({100: 1.0})

    def test_addition(self):
        # Test basic addition
        result = self.one + self.eps
        print(f"Testing addition: {self.one} + {self.eps} = {result}")
        self.assertEqual(result.terms, {0: 1.0, 1: 1.0})

        # Test commutativity
        result_comm = self.eps + self.one
        print(f"Testing commutativity: {self.eps} + {self.one} = {result_comm}")
        self.assertEqual(result.terms, result_comm.terms)

        # Test zero identity
        result_zero = self.complex_num + self.zero
        print(
            f"Testing zero identity: {self.complex_num} + {self.zero} = {result_zero}"
        )
        self.assertEqual(result_zero.terms, self.complex_num.terms)

        # Add test for high-order terms
        result_high = self.one + self.high_order
        print(
            f"Testing high-order addition: {self.one} + {self.high_order} = {result_high}"
        )
        self.assertEqual(result_high.terms, {0: 1.0, 100: 1.0})

    def test_multiplication(self):
        # Test basic multiplication
        result = self.eps * self.eps
        print(f"Testing multiplication: {self.eps} * {self.eps} = {result}")
        self.assertEqual(result.terms, {2: 1.0})
        self.assertEqual(
            LeviCivitaNumber.eps() * LeviCivitaNumber.H(),
            LeviCivitaNumber.one(),
            msg=f"{LeviCivitaNumber.eps() * LeviCivitaNumber.H() = }",
        )
        # Test with more complex numbers
        result_complex = self.complex_num * self.eps
        print(
            f"Testing multiplication: ({self.complex_num}) * ({self.eps}) = {result_complex}"
        )
        self.assertEqual(result_complex.terms, {1: 2.0, 2: 3.0, 3: 0.0})

        # Test one identity
        result_identity = self.complex_num * self.one
        print(
            f"Testing multiplication identity: {self.complex_num} * {self.one} = {result_identity}"
        )
        self.assertEqual(result_identity.terms, self.complex_num.terms)

        # Test multiplication with high-order terms
        result_high = self.eps * self.high_order
        print(
            f"Testing high-order multiplication: {self.eps} * {self.high_order} = {result_high}"
        )
        self.assertEqual(result_high.terms, {101: 1.0})

    def test_comparison(self):
        # Test equality
        self.assertEqual(self.one, LeviCivitaNumber({0: 1.0}))

        # Test less than
        self.assertTrue(self.zero < self.one)
        self.assertTrue(self.eps < self.one)

        # Test greater than
        self.assertTrue(self.one > self.zero)
        self.assertTrue(self.complex_num > self.one)

        # Test lexicographic ordering
        a = LeviCivitaNumber({0: 1.0, 1: 2.0, 2: 0.0})
        b = LeviCivitaNumber({0: 1.0, 1: 3.0, 2: 0.0})
        self.assertTrue(a < b)

    def test_negation_and_subtraction(self):
        # Test negation
        neg_one = -self.one
        print(f"Testing negation: -{self.one} = {neg_one}")
        self.assertEqual(neg_one.terms, {0: -1.0})

        # Test subtraction
        result = self.complex_num - self.one
        print(f"Testing subtraction: {self.complex_num} - {self.one} = {result}")
        self.assertEqual(
            result.terms, {1: 2.0, 2: 3.0}
        )  # 1.0 - 1.0 = 0 for constant term

    def test_string_representation(self):
        # Test basic representation
        self.assertEqual(str(self.zero), "0")
        self.assertEqual(str(self.one), "1")
        self.assertEqual(str(self.eps), "ε")
        self.assertEqual(str(self.eps_squared), "ε²")

        # Test complex number representation
        self.assertEqual(str(self.complex_num), "1 + 2ε + 3ε²")

    def test_division(self):
        """Test division of Levi-Civita numbers."""
        # Test division by a scalar
        result = self.one / 2
        print(f"Testing division by scalar: {self.one} / 2 = {result}")
        self.assertEqual(result.terms, {0: 0.5})

        # Test division of Levi-Civita numbers
        result_eps_one = self.eps / self.one
        print(f"Testing division: {self.eps} / {self.one} = {result_eps_one}")
        self.assertEqual(result_eps_one.terms, {1: 1.0})  # ε / 1 = ε

        # Test division resulting in negative exponents
        result_neg_exp = self.eps / self.eps_squared
        print(
            f"Testing negative exponents: {self.eps} / {self.eps_squared} = {result_neg_exp}"
        )
        self.assertEqual(result_neg_exp.terms, {-1: 1.0})  # ε / ε² = ε⁻¹

        # Test division resulting in positive exponents
        result_pos_exp = self.eps_squared / self.eps
        print(
            f"Testing positive exponents: {self.eps_squared} / {self.eps} = {result_pos_exp}"
        )
        self.assertEqual(result_pos_exp.terms, {1: 1.0})  # ε² / ε = ε
        # Test division of non-pure terms

    def test_power(self):
        """Test exponentiation of Levi-Civita numbers."""
        # Test positive exponent
        result = self.eps**3
        self.assertEqual(result.terms, {3: 1.0})  # ε³

        # Test zero exponent
        result = self.eps**0
        self.assertEqual(result.terms, {0: 1.0})  # ε⁰ = 1

        # Test negative exponent
        result = self.eps**-1
        self.assertEqual(result.terms, {-1: 1.0})  # ε⁻¹

        # Test exponentiation by squaring
        result = (self.one + self.eps) ** 2
        self.assertEqual(
            result.terms, {0: 1.0, 1: 2.0, 2: 1.0}
        )  # (1 + ε)² = 1 + 2ε + ε²

    def test_inversion(self):
        """Test inversion of Levi-Civita numbers."""
        # Test inversion of a pure infinitesimal
        inv_eps = ~self.eps
        print(f"Testing inversion of ε: ~{self.eps} = {inv_eps}")
        self.assertEqual(inv_eps.terms, {-1: 1.0})

        # Test inversion of a standard number
        inv_one = ~self.one
        print(f"Testing inversion of 1: ~{self.one} = {inv_one}")
        self.assertEqual(inv_one.terms, {0: 1.0})

        # Test inversion with series expansion
        num = LeviCivitaNumber({0: 1.0, 1: 1.0})
        inv_num = ~num
        print(f"Testing inversion with expansion: ~{num} = {inv_num}")
        expected_terms = {0: 1.0, 1: -1.0, 2: 1.0, 3: -1.0}
        self.assertEqual(inv_num.terms, expected_terms)

    def test_comparison_operators(self):
        """Test comparison operators (<, <=, >, >=)."""
        num_a = LeviCivitaNumber({0: 1.0, 1: 1.0})  # 1 + ε
        num_b = LeviCivitaNumber({0: 1.0})  # 1
        num_c = LeviCivitaNumber({0: 1.0, 1: -1.0})  # 1 - ε

        self.assertTrue(num_b < num_a)
        self.assertTrue(num_c < num_b)
        self.assertTrue(num_c <= num_b)
        self.assertTrue(num_a > num_b)
        self.assertTrue(num_a >= num_b)

    def test_equality(self):
        """Test equality and inequality of Levi-Civita numbers."""
        num_a = LeviCivitaNumber({0: 1.0, 1: 1e-10})
        num_b = LeviCivitaNumber({0: 1.0})

        self.assertTrue(num_a == num_b)  # Should be equal within tolerance
        self.assertFalse(self.eps == self.zero)
        self.assertTrue(self.zero == LeviCivitaNumber({}))

    def test_negation(self):
        """Test negation of Levi-Civita numbers."""
        result = -self.eps
        self.assertEqual(result.terms, {1: -1.0})

        result = -self.complex_num
        expected_terms = {0: -1.0, 1: -2.0, 2: -3.0}
        self.assertEqual(result.terms, expected_terms)

    def test_subtraction(self):
        """Test subtraction of Levi-Civita numbers."""
        result = self.one - self.eps
        self.assertEqual(result.terms, {0: 1.0, 1: -1.0})

        result = self.eps - self.eps_squared
        self.assertEqual(result.terms, {1: 1.0, 2: -1.0})

        result = self.complex_num - self.one
        self.assertEqual(result.terms, {1: 2.0, 2: 3.0})

    def test_mixed_operations(self):
        """Test mixed operations combining addition, multiplication, etc."""
        # (1 + ε) * (1 - ε) = 1 - ε²
        num = (self.one + self.eps) * (self.one - self.eps)
        self.assertEqual(num.terms, {0: 1.0, 2: -1.0})

        # (ε + ε²) / ε = 1 + ε
        num = (self.eps + self.eps_squared) / self.eps
        self.assertEqual(num.terms, {0: 1.0, 1: 1.0})

        # (1 + ε) ** 3 = 1 + 3ε + 3ε² + ε³
        num = (self.one + self.eps) ** 3
        expected_terms = {0: 1.0, 1: 3.0, 2: 3.0, 3: 1.0}
        self.assertEqual(num.terms, expected_terms)

    def test_repr(self):
        """Test the string representation of Levi-Civita numbers."""
        # Test representation of negative exponents
        num = LeviCivitaNumber.H()
        self.assertEqual(str(num), "ε⁻¹")

        # Test representation with mixed exponents
        num = LeviCivitaNumber({2: -1.0, -1: -1.0})
        self.assertEqual(str(num), "-ε⁻¹ - ε²")

    def test_non_pure_operations(self):
        """Test operations on non-pure Levi-Civita numbers."""
        # Approximate square root of (1 + ε)
        num = LeviCivitaNumber({0: 1.0, 1: 1.0})
        approx_sqrt = LeviCivitaNumber(
            {0: 1.0, 1: 0.5, 2: -0.125, 3: 0.0625, 4: -0.0390625}
        )
        squared = approx_sqrt * approx_sqrt
        print(f"Testing square root approximation: ({approx_sqrt})^2 = {squared}")
        print(f"{squared = }")
        print(f"{num = }")
        self.assertEqual(squared.terms, num.terms)

        # Inverse of the square root approximation
        inverse = ~approx_sqrt
        print(f"Testing inversion of sqrt approximation: ~{approx_sqrt} = {inverse}")
        expected_inverse = LeviCivitaNumber({0: 1.0, 1: -0.5, 2: 0.375, 3: -0.3125})
        self.assertEqual(inverse.terms, expected_inverse.terms)

        # Test multiplication of non-pure terms
        num1 = LeviCivitaNumber({0: 1.0, 1: 1.0})
        num2 = LeviCivitaNumber({0: 2.0, 2: 3.0})
        result = num1 * num2
        print(f"Testing multiplication of non-pure terms: {num1} * {num2} = {result}")
        expected = LeviCivitaNumber({0: 2.0, 1: 2.0, 2: 3.0, 3: 3.0})
        self.assertEqual(result.terms, expected.terms)

    def test_precision_handling(self):
        """Test calculations involving small coefficients and higher-order terms."""
        num_a = LeviCivitaNumber({0: 1.0, 5: 1e-10})
        num_b = LeviCivitaNumber({0: 1.0})
        self.assertTrue(num_a == num_b)  # Coefficient is negligible

        # Test addition with negligible terms
        result = num_b + LeviCivitaNumber({10: 1e-15})
        self.assertEqual(result.terms, {0: 1.0})  # Higher-order term is negligible

    def test_edge_cases(self):
        """Test edge cases such as division by infinitesimal and zero."""
        # Division by infinitesimal
        with self.assertRaises(ZeroDivisionError):
            result = self.one / self.zero

        # Division of infinitesimal by standard number
        result = self.eps / 2
        self.assertEqual(result.terms, {1: 0.5})

        # Raising zero to a negative exponent
        with self.assertRaises(ZeroDivisionError):
            result = self.zero**-1

    def test_complex_multiplication(self):
        """Test complex multiplication expressions."""
        # Compute (1 + ε + ε²) * (1 - ε + ε²)
        num1 = LeviCivitaNumber({0: 1.0, 1: 1.0, 2: 1.0})
        num2 = LeviCivitaNumber({0: 1.0, 1: -1.0, 2: 1.0})
        result = num1 * num2
        print(f"Testing complex multiplication: ({num1}) * ({num2}) = {result}")
        expected = LeviCivitaNumber({0: 1.0, 2: 1.0, 4: 1.0})
        self.assertEqual(
            result,
            expected,
            msg=f"{str(result) = }, {str(expected) = }",
        )

    def test_complex_division(self):
        """Test complex division expressions."""
        # Compute (1 + ε) / (1 - ε)
        num = (self.one + self.eps) / (self.one - self.eps)
        print(
            f"Testing division: ({self.one} + {self.eps}) / ({self.one} - {self.eps}) = {num}"
        )
        expected = LeviCivitaNumber({0: 1.0, 1: 2.0, 2: 4.0, 3: 8.0, 4: 16.0})
        self.assertEqual(num.terms, expected.terms)

        # Compute e^(ε) ≈ 1 + ε
        num = LeviCivitaNumber({0: 1.0, 1: 1.0})
        # Assuming exponential function is implemented
        # result = num.exp()
        # expected = LeviCivitaNumber({0: math.e})
        # self.assertEqual(result.terms, expected.terms)

    @given(x=levi_civita_numbers(), y=levi_civita_numbers())
    def test_addition_commutativity(
        self, x: LeviCivitaNumber, y: LeviCivitaNumber
    ) -> None:
        result1 = x + y
        result2 = y + x
        self.assertEqual(
            result1, result2, f"Addition is not commutative for {x} and {y}"
        )

    @given(x=levi_civita_numbers())
    def test_double_negation(self, x: LeviCivitaNumber) -> None:
        result = -(-x)
        self.assertEqual(result, x, f"Double negation failed for {x}")

    @given(x=levi_civita_numbers().filter(lambda n: not n.is_zero))
    def test_double_reciprocal(self, x: LeviCivitaNumber) -> None:
        assume(not x.is_zero)
        result = ~(~x)
        self.assertEqual(result, x, f"Double reciprocal failed for {x}")

    @given(
        x=levi_civita_numbers(), y=levi_civita_numbers().filter(lambda n: not n.is_zero)
    )
    def test_division_multiplication(
        self, x: LeviCivitaNumber, y: LeviCivitaNumber
    ) -> None:
        assume(not y.is_zero)
        result = (x / y) * y
        self.assertTrue(
            x.is_close_to(result, tol=1e-6),
            f"Division and multiplication failed for {x} and {y}",
        )

    @given(x=levi_civita_numbers())
    def test_zero_addition(self, x: LeviCivitaNumber) -> None:
        self.assertEqual(x + self.zero, x, msg=f"Zero addition failed for {x}")

    @given(x=levi_civita_numbers())
    def test_zero_multiplication(self, x: LeviCivitaNumber) -> None:
        self.assertEqual(
            x * self.zero, self.zero, msg=f"Zero multiplication failed for {x}"
        )

    @given(x=levi_civita_numbers())
    def test_one_multiplication(self, x: LeviCivitaNumber) -> None:
        self.assertEqual(x * self.one, x, msg=f"One multiplication failed for {x}")


if __name__ == "__main__":
    unittest.main()
