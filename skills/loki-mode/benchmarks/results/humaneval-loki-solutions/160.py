# HumanEval/160
# Loki Mode Multi-Agent Solution
# Attempts: 1
# Passed: True

def do_algebra(operator, operand):
    """
    Given two lists operator, and operand. The first list has basic algebra operations, and 
    the second list is a list of integers. Use the two given lists to build the algebric 
    expression and return the evaluation of this expression.

    The basic algebra operations:
    Addition ( + ) 
    Subtraction ( - ) 
    Multiplication ( * ) 
    Floor division ( // ) 
    Exponentiation ( ** ) 

    Example:
    operator['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operator list is equal to the length of operand list minus one.
        Operand is a list of of non-negative integers.
        Operator list has at least one operator, and operand list has at least two operands.

    """
    import ast
    import operator as arithmetic

    operations = {ast.Add: arithmetic.add, ast.Sub: arithmetic.sub,
                  ast.Mult: arithmetic.mul, ast.FloorDiv: arithmetic.floordiv,
                  ast.Pow: arithmetic.pow}
    if len(operand) != len(operator) + 1 or not operand:
        raise ValueError("Expected one more operand than operators")
    if any(type(n) is not int or n < 0 for n in operand):
        raise ValueError("Operands must be non-negative integers")
    if any(type(op) is not str or op not in {"+", "-", "*", "//", "**"} for op in operator):
        raise ValueError("Unsupported algebra operator")
    expression = str(operand[0]) + "".join(
        op + str(n) for op, n in zip(operator, operand[1:]))

    def calculate(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            return operations[type(node.op)](calculate(node.left), calculate(node.right))
        raise ValueError("Unsupported algebra expression")

    return calculate(ast.parse(expression, mode="eval").body)
