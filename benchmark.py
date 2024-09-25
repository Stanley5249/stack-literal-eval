import argparse
import timeit
from ast import literal_eval
from collections.abc import Callable
from typing import Any

from main import stack_literal_eval

test_cases = {
    "constant": "42",
    "unary": "-42",
    "complex": "1 + 2j",
    "empty_tuple": "()",
    "empty_list": "[]",
    "empty_set": "set()",
    "empty_dict": "{}",
    "tuple": "(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)",
    "list": "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
    "set": "{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}",
    "dict": "{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}",
    "nested": "[0, " * 32 + "]" * 32,
}


def timeit_func(f: Callable[[str], Any], x: str, n: int) -> float:
    t = timeit.timeit(
        "f(x)",
        number=n,
        globals={"f": f, "x": x},
    )
    print(f"- {f.__name__:<20}: {t:.4f}s")
    return t


def plot(n: int) -> None:
    import matplotlib.pyplot as plt

    ratios = []

    print(f"number of iterations: {n:,}")

    for name, expr in test_cases.items():
        print(name)
        t1 = timeit_func(literal_eval, expr, n)
        t2 = timeit_func(stack_literal_eval, expr, n)
        r = (t1 - t2) / t1
        print(f"- {r:.2%}")
        ratios.append(r)

    plt.bar([*test_cases], ratios)
    plt.xlabel("test cases")
    plt.ylabel("time ratio ((a - b) / a)")
    plt.title("literal_eval (a) vs stack_literal_eval (b)")
    plt.xticks(rotation=45, ha="right")

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark literal_eval vs stack_literal_eval"
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=300000,
        help="Number of iterations for benchmarking",
    )
    args = parser.parse_args()
    plot(args.number)
