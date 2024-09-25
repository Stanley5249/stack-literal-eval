from ast import literal_eval

import pyperf

from benchmark import test_cases

if __name__ == "__main__":
    runner = pyperf.Runner()
    for name, expr in test_cases.items():
        runner.bench_func(name, literal_eval, expr)
