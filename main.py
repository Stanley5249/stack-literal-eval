from ast import (
    AST,
    Add,
    BinOp,
    Call,
    Constant,
    Dict,
    Expression,
    List,
    Name,
    Set,
    Sub,
    Tuple,
    UAdd,
    UnaryOp,
    USub,
    parse,
)
from typing import Any


def convert(node: AST) -> Any:
    if isinstance(node, Constant):
        return node.value
    elif isinstance(node, Tuple):
        return (*[convert(elt) for elt in node.elts],)
    elif isinstance(node, List):
        return [convert(elt) for elt in node.elts]
    elif isinstance(node, Set):
        return {convert(elt) for elt in node.elts}
    elif isinstance(node, Call):
        func = node.func
        if (
            isinstance(func, Name)
            and func.id == "set"
            and not (node.args or node.keywords)
        ):
            return set()
    elif isinstance(node, Dict):
        if len(node.keys) == len(node.values) and None not in node.keys:
            return {
                convert(k):  # type: ignore
                convert(v)
                for k, v in zip(node.keys, node.values)
            }
    elif isinstance(node, BinOp):
        left = node.left
        right = node.right
        if isinstance(left, (Constant, UnaryOp)) and isinstance(right, Constant):
            real = convert(left)
            imag = convert(right)
            if type(real) in [int, float] and type(imag) is complex:
                op = node.op
                if isinstance(op, Add):
                    return real + imag
                elif isinstance(op, Sub):
                    return real - imag
    elif isinstance(node, UnaryOp):
        operand = node.operand
        if isinstance(operand, Constant):
            operand = convert(operand)
            if type(operand) in [int, float, complex]:
                op = node.op
                if isinstance(op, UAdd):
                    return operand
                elif isinstance(op, USub):
                    return -operand
    lno = getattr(node, "lineno", None)
    if lno is None:
        raise ValueError("malformed node or string:")
    raise ValueError(f"malformed node or string on line {lno}:")


def stack_literal_eval(node_or_string: str | AST) -> Any:
    if isinstance(node_or_string, str):
        node = parse(node_or_string.lstrip(" \t"), mode="eval").body
    elif isinstance(node_or_string, Expression):
        node = node_or_string.body
    else:
        node = node_or_string

    return convert(node)
