import pyperf

from benchmark import test_cases
from main import stack_literal_eval

if __name__ == "__main__":
    runner = pyperf.Runner()
    for name, expr in test_cases.items():
        runner.bench_func(name, stack_literal_eval, expr)
