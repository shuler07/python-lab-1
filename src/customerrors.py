class MathExpressionError(Exception):
    def __init__(self, msg: str, field: str):
        message = f"Invalid math expression ({msg}) -> {field}"
        super().__init__(message)