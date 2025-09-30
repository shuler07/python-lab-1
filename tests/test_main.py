from pytest import raises
from src.main import SolverM1
from src.customerrors import MathExpressionError

solver = SolverM1()


class TestSolverM1:

    def test_1(self):
        assert solver.expr("(2 + 4* 2)// 3+ 4") == 7

    def test_2(self):
        assert solver.expr("(20+4*20 % 1) * 2") == 40

    def test_3(self):
        assert solver.expr("5**2**2") == 625

    def test_4(self):
        assert solver.expr("2**(2+1)-1") == 7

    def test_5(self):
        assert solver.expr("(10-2)**0+(3-1)%2") == 1

    def test_6(self):
        assert solver.expr("(~2- 3) **  3") == -125

    def test_7(self):
        assert solver.expr("~4 ** 4") == -256

    def test_8(self):
        assert solver.expr("(~4) ** 4") == 256

    def test_9(self):
        assert solver.expr("~(2  **2 ** 3%10 - 4 *2) ** 3") == 8

    def test_10(self):
        assert solver.expr("~(~(~(~(~(3 ** 2 + 2))))+ ~2)") == -9

    def test_11(self):
        assert solver.expr("2**3+2**3 -(3)**2") == 7

    def test_12(self):
        assert solver.expr("2+2*(2**2+3*3//2-10+~23)+23**2-20") == 461

    def test_13(self):
        assert solver.expr("~(   ~2** (~0.5) ** (~1)  ) +6*2 % 5") == 2.25

    def test_14(self):
        assert f"{solver.expr('2**~2**~2'):.5f}" == "0.84090"

    def test_15(self):
        assert solver.expr("~(~2)**2") == -4

    def test_16(self):
        assert solver.expr("~(~2)**3") == 8


class TestErrorsSolverM1:

    def assertError(self, exception, expr) -> bool:
        with raises(exception) as exc:
            solver.expr(expr)
        return exc.errisinstance(exception)

    def test_error_1(self):
        assert self.assertError(ZeroDivisionError, "2 / ((1+2) % 3)")

    def test_error_2(self):
        assert self.assertError(MathExpressionError, "3/2 // 1")

    def test_error_3(self):
        assert self.assertError(MathExpressionError, "2 / 3 // 2")

    def test_error_4(self):
        assert self.assertError(ValueError, "")
