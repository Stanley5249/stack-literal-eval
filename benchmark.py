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

    fig = plt.figure(figsize=(12, 6), layout="tight")
    ax = fig.add_subplot(111)

    ratios = []

    print(f"number of iterations: {n:,}")

    for name, expr in test_cases.items():
        print(name)
        t1 = timeit_func(literal_eval, expr, n)
        t2 = timeit_func(stack_literal_eval, expr, n)
        r = (t1 - t2) / t1
        print(f"- {r:.2%}")
        ratios.append(r)

    xlabels = [*test_cases]
    ax.bar(xlabels, ratios)
    ax.set_xlabel("test cases")
    ax.set_ylabel("time ratio")
    ax.set_title("literal_eval vs stack_literal_eval")
    ax.tick_params(axis="x", rotation=45)
    fig.savefig("resources/benchmark.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark literal_eval vs stack_literal_eval"
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=100000,
        help="Number of iterations for benchmarking",
    )
    args = parser.parse_args()
    plot(args.number)
