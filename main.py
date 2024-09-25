from ast import (
    AST,
    Add,
    BinOp,
    Call,
    Constant,
    Dict,
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
    node_stack: list[tuple[AST, bool]] = [(node, True)]
    value_stack: list[Any] = []

    while node_stack:
        node, not_visited = node_stack.pop()
        if isinstance(node, Constant):
            value_stack.append(node.value)
        elif isinstance(node, Tuple):
            if not_visited:
                node_stack.append((node, False))
                for elt in node.elts:
                    node_stack.append((elt, True))
            else:
                value_stack.append((*[value_stack.pop() for _ in node.elts],))
        elif isinstance(node, List):
            if not_visited:
                node_stack.append((node, False))
                for elt in node.elts:
                    node_stack.append((elt, True))
            else:
                value_stack.append([value_stack.pop() for _ in node.elts])
        elif isinstance(node, Set):
            if not_visited:
                node_stack.append((node, False))
                for elt in node.elts:
                    node_stack.append((elt, True))
            else:
                value_stack.append({value_stack.pop() for _ in node.elts})
        elif isinstance(node, Call):
            func = node.func
            if (
                isinstance(func, Name)
                and func.id == "set"
                and not (node.args or node.keywords)
            ):
                value_stack.append(set())
            else:
                break
        elif isinstance(node, Dict):
            if not_visited:
                node_stack.append((node, False))
                keys = node.keys
                values = node.values
                if len(keys) != len(values) or None in keys:
                    break
                for key in keys:
                    node_stack.append((key, True))  # type: ignore
                for value in values:
                    node_stack.append((value, True))
            else:
                items = zip(
                    [value_stack.pop() for _ in node.keys],
                    [value_stack.pop() for _ in node.values],
                )
                value_stack.append(dict(items))
        elif isinstance(node, BinOp):
            if not_visited:
                left = node.left
                right = node.right
                if not (
                    isinstance(left, (Constant, UnaryOp))
                    and isinstance(right, (Constant))
                ):
                    break
                node_stack.append((node, False))
                node_stack.append((left, True))
                node_stack.append((right, True))
            else:
                real = value_stack.pop()
                if not isinstance(real, (int, float)):
                    break
                imag = value_stack.pop()
                if not isinstance(imag, complex):
                    break
                op = node.op
                if isinstance(op, Add):
                    value_stack.append(real + imag)
                elif isinstance(op, Sub):
                    value_stack.append(real - imag)
                else:
                    break
        elif isinstance(node, UnaryOp):
            if not_visited:
                operand = node.operand
                if not isinstance(operand, Constant):
                    break
                node_stack.append((node, False))
                node_stack.append((operand, True))
            else:
                operand = value_stack.pop()
                if isinstance(operand, bool) or not isinstance(
                    operand, (int, float, complex)
                ):
                    break
                op = node.op
                if isinstance(op, UAdd):
                    value_stack.append(operand)
                elif isinstance(op, USub):
                    value_stack.append(-operand)
                else:
                    break
        else:
            break
    else:
        assert len(value_stack) == 1, value_stack
        return value_stack.pop()

    lno = getattr(node, "lineno", None)

    if lno is None:
        raise ValueError("malformed node or string:")

    raise ValueError(f"malformed node or string on line {lno}:")


def stack_literal_eval(node_or_string: str | AST) -> Any:
    if isinstance(node_or_string, str):
        node = parse(node_or_string.lstrip(" \t"), mode="eval").body
    else:
        node = node_or_string

    return convert(node)
