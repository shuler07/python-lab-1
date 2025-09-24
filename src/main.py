from customerrors import MathExpressionError


class SolverM1:
    """
    Класс для решения математический выражений. Для вычисления значения:\n
    1. Создайте объект класса.\n
    2. Передайте выражение в метод expr().\n
    3. Если выражение корректно, метод expr() вернет вычисленное значение.\n
    Поддерживаются знаки: < 0-9 . ~ $ + - * ** / // % ( ) >
    """

    def __init__(self) -> None:
        self.rec_count = 0

    def expr(self, expression: str) -> float:
        "Вычисление значения математического выражения"
        if self.is_expr_valid(expression):
            self.rec_count = 1
            return self.add(expression.replace(" ", ""))
        else:
            raise MathExpressionError("Extra brackets", expression)

    def is_expr_valid(self, expr: str) -> bool:
        "Проверка правильности выражения"
        last_key = "operator"
        brackets_opened = 0

        i = 0
        while i < len(expr):
            char = expr[i]

            if char.isspace():
                pass
            elif char.isdigit() or char in "~$":
                if last_key in ["operator", "lbracket"]:
                    i += 1
                    was_point = False
                    if char in "~$" and i < len(expr) and expr[i] == "(":
                        brackets_opened += 1
                        last_key = "lbracket"
                    else:
                        while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                            if expr[i] == ".":
                                if was_point:
                                    raise MathExpressionError(
                                        "2 floating points in signle number",
                                        expr[i - 5 : i + 5],
                                    )
                                else:
                                    was_point = True
                            i += 1
                        i -= 1
                        last_key = "number"
                else:
                    raise MathExpressionError(
                        "Number must go after operator or left bracket",
                        expr[i - 5 : i + 5],
                    )
            elif char == "/":
                if last_key in ["number", "rbracket"]:
                    if i + 1 == len(expr):
                        raise MathExpressionError(
                            "Expression must end with number or right bracket",
                            expr[i - 5 : i + 5],
                        )
                    elif expr[i + 1] == "/":
                        i += 1
                        if i + 1 == len(expr):
                            raise MathExpressionError(
                                "Expression must end with number or right bracket",
                                expr[i - 5 : i + 5],
                            )
                        elif expr[i + 1] == "/":
                            raise MathExpressionError(
                                "Operator '///' doesn't exist", expr[i - 5 : i + 5]
                            )
                        else:
                            last_key = "operator"
                    else:
                        last_key = "operator"
                else:
                    raise MathExpressionError(
                        "Operator '/' must go after number or left bracket",
                        expr[i - 5 : i + 5],
                    )
            elif char == "*":
                if last_key in ["number", "rbracket"]:
                    if i + 1 == len(expr):
                        raise MathExpressionError(
                            "Expression must end with number or right bracket",
                            expr[i - 5 : i + 5],
                        )
                    elif expr[i + 1] == "*":
                        i += 1
                        if i + 1 == len(expr):
                            raise MathExpressionError(
                                "Expression must end with number or right bracket",
                                expr[i - 5 : i + 5],
                            )
                        elif expr[i + 1] == "*":
                            raise MathExpressionError(
                                "Operator '***' doesn't exist", expr[i - 5 : i + 5]
                            )
                        else:
                            last_key = "operator"
                    else:
                        last_key = "operator"
                else:
                    raise MathExpressionError(
                        "Operator '*' must go after number or left bracket",
                        expr[i - 5 : i + 5],
                    )
            elif char in "+-%":
                if last_key in ["number", "rbracket"]:
                    last_key = "operator"
                else:
                    raise MathExpressionError(
                        f"Operator '{char}' must go after number or left bracket",
                        expr[i - 5 : i + 5],
                    )
            elif char == "(":
                if last_key in ["operator", "lbracket"]:
                    last_key = "lbracket"
                    brackets_opened += 1
                else:
                    raise MathExpressionError(
                        "Left bracket must go after operator or left bracket",
                        expr[i - 5 : i + 5],
                    )
            elif char == ")":
                if last_key in ["number", "rbracket"]:
                    last_key = "rbracket"
                    brackets_opened -= 1
                else:
                    raise MathExpressionError(
                        "Right bracket must go after number or right bracket",
                        expr[i - 5 : i + 5],
                    )
            else:
                raise MathExpressionError(
                    f"Invalid symbol '{char}'", expr[i - 5 : i + 5]
                )

            i += 1

        return brackets_opened == 0 and last_key != "operator"

    def is_expr_has_edge_brackets_and_sign(self, expr: str) -> tuple[bool, str]:
        """
        Проверка на наличие крайних скобок выражения (с учетом возможного унарного минуса / плюса перед ними).\n
        Возвращает кортеж, где первый элемент - наличие крайних скобок, второй - символ перед ними. Например:\n~~~
        (2 + 3 * 2) -> True, ''\n
        ~(2 + 3 * 2) -> True, '~'\n
        (2 + 3) * 2 -> False, ''\n
        $(2 + 3 * 2) -> True, '$'
        ~~~"""
        sign = ""
        if expr[:2] == "~(" and expr[-1] == ")":
            sign = "~"
            expr = expr[2:-1]
        elif expr[:2] == "$(" and expr[-1] == ")":
            sign = "$"
            expr = expr[2:-1]
        elif expr[0] == "(" and expr[-1] == ")":
            expr = expr[1:-1]
        else:
            return (False, "")

        brackets_count = 1
        for char in expr:
            if char == "(":
                brackets_count += 1
            elif char == ")":
                brackets_count -= 1
            if brackets_count == 0:
                return (False, "")

        return (True, sign)

    def add(self, expr: str) -> float:
        """
        1. Проверка на наличие крайних скобок выражения\n
        2. Выполнение всех операций сложения / вычитания в выражении\n
        3. Переход к mul()
        """
        hasEdgeBrackets, sign = self.is_expr_has_edge_brackets_and_sign(expr)
        if hasEdgeBrackets:
            if sign != "":
                expr = expr[2:-1]
            else:
                expr = expr[1:-1]

        brackets_opened = 0
        values, operators = [], []

        i = start = 0
        while i < len(expr):
            char = expr[i]
            if char in "+-" and brackets_opened == 0:
                values.append(expr[start:i])
                operators.append(char)
                start = i + 1
            elif char == "(":
                brackets_opened += 1
            elif char == ")":
                brackets_opened -= 1
            i += 1

        values.append(expr[start:])
        # print("Add found:", values, operators)

        while len(values) != 1:
            self.rec_count += 2
            match (operators.pop(0)):
                case "+":
                    values[0] = str(
                        self.mul(values[0]) + self.mul(values.pop(1))
                    ).replace("-", "~")
                case "-":
                    values[0] = str(
                        self.mul(values[0]) - self.mul(values.pop(1))
                    ).replace("-", "~")

        # print("Add -> Mul", values[0])

        return -self.mul(values[0]) if sign == "~" else self.mul(values[0])

    def mul(self, expr: str) -> float:
        """
        1. Проверка на наличие крайних скобок выражения\n
        2. Выполнение всех операций умножения / деления в выражении\n
        3. Переход к pow()
        """
        if self.is_expr_has_edge_brackets_and_sign(expr)[0]:
            return self.add(expr)

        brackets_opened = 0
        values, operators = [], []

        i = start = 0
        while i < len(expr):
            char = expr[i]
            if char in "/*%" and brackets_opened == 0:
                if char == "*" and expr[i + 1] == "*":
                    i += 1
                else:
                    values.append(expr[start:i])
                    if char == "/":
                        if expr[i + 1] == "/":
                            operators.append("//")
                            start = i + 2
                            i += 1
                        else:
                            operators.append("/")
                            start = i + 1
                    elif char == "*":
                        operators.append("*")
                        start = i + 1
                    else:
                        operators.append("%")
                        start = i + 1
            elif char == "(":
                brackets_opened += 1
            elif char == ")":
                brackets_opened -= 1
            i += 1

        values.append(expr[start:])
        # print("Mul found:", values, operators)

        while len(values) != 1:
            self.rec_count += 2
            match (operators.pop(0)):
                case "//":
                    num1, num2 = self.pow(values[0]), self.pow(values.pop(1))
                    if isinstance(num1, int) and isinstance(num2, int):
                        values[0] = str(num1 // num2).replace("-", "~")
                    else:
                        raise MathExpressionError(
                            "Operator '//' allowed only between integers",
                            f"{num1} {type(num1)}, {num2} {type(num2)}",
                        )
                case "/":
                    values[0] = str(
                        self.pow(values[0]) / self.pow(values.pop(1))
                    ).replace("-", "~")
                case "*":
                    values[0] = str(
                        self.pow(values[0]) * self.pow(values.pop(1))
                    ).replace("-", "~")
                case "%":
                    num1, num2 = self.pow(values[0]), self.pow(values.pop(1))
                    if isinstance(num1, int) and isinstance(num2, int):
                        values[0] = str(num1 % num2).replace("-", "~")
                    else:
                        raise MathExpressionError(
                            "Operator '%' allowed only between integers",
                            f"{num1} {type(num1)}, {num2} {type(num2)}",
                        )

        # print("Mul -> Pow", values[0])

        return self.pow(values[0])

    def pow(self, expr: str) -> float:
        """
        1. Проверка на наличие крайних скобок выражения\n
        2. Выполнение всех операций возведения в степень в выражении\n
        3. Переход к unary()
        """
        if self.is_expr_has_edge_brackets_and_sign(expr)[0]:
            return self.add(expr)

        brackets_opened = 0
        values = []
        isReverse = False

        i = start = 0
        while i < len(expr):
            char = expr[i]
            if char == "*" and expr[i] == "*" and brackets_opened == 0:
                lnum = expr[start:i]
                # Если перед первым числом унарный минус, он идет в ответ (~2**2 == ~4)
                if lnum[0] == "~":
                    values.append(lnum[1:])
                    isReverse = True
                else:
                    values.append(lnum)
                start = i + 2
                i += 1
            elif char == "(":
                brackets_opened += 1
            elif char == ")":
                brackets_opened -= 1
            i += 1

        values.append(expr[start:])
        # print("Pow found:", values)

        while len(values) != 1:
            self.rec_count += 2
            values.append(
                str(self.unary(values.pop(-2)) ** self.unary(values.pop())).replace(
                    "-", "~"
                )
            )

        # print("Pow -> Unary", values[0])

        return -self.unary(values[0]) if isReverse else self.unary(values[0])

    def unary(self, expr: str) -> float:
        """
        1. Проверка на наличие крайних скобок выражения\n
        2. Проверка на финальность числа\n
        3. Переход к primary() или определение знака числа
        """
        if self.is_expr_has_edge_brackets_and_sign(expr)[0]:
            return self.add(expr)

        if self.rec_count == 1:
            return self.primary(expr)

        for char in expr[1:]:
            if char.isdigit() or char in ".":
                continue
            else:
                return self.add(expr)
        else:
            self.rec_count -= 1
            if expr[0] == "~":
                return -float(expr[1:]) if "." in expr else -int(expr[1:])
            else:
                expr = expr.replace("$", "")
                return float(expr) if "." in expr else int(expr)

    def primary(self, expr: str) -> float:
        "Определение знака финального числа и возврат значения"
        minuses_count = expr.count("~")
        expr = expr.replace("~", "")
        if minuses_count % 2 == 0:
            return float(expr) if "." in expr else int(expr)
        else:
            return -float(expr) if "." in expr else -int(expr)


def main() -> None:
    "Создание объекта класса SolverM1, при помощи которого вычисляются значения математических выражений"
    solver = SolverM1()

    while True:
        expression = input("Введите выражение: ")
        answer = solver.expr(expression)
        print("Ответ:", answer, "\n")


if __name__ == "__main__":
    main()
