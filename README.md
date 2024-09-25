# Stack-based `ast.literal_eval`

## Purpose

### Avoiding Recursion Errors

~~Using a stack to implement `literal_eval` can avoid `RecursionError`.~~

I realized that this error was caused by the C implementation, not Python, so this approach was not effective in avoiding the error.

### Removing Unnecessary Closures

Related to a closed issue [#75934](https://github.com/python/cpython/issues/75934).

## Running Tests

The tests are copied from the CPython main branch, retaining only those related to `ast.literal_eval`. To run the tests, use the following command:

```sh
python -m unittest test_main.py
```

## Benchmark Results

To run the benchmark, use the following command:

```sh
python benchmark.py
```

Below are the benchmark results comparing `ast.literal_eval` and `stack_literal_eval`, conducted on an Intel(R) Core(TM) Ultra 9 185H.

![benchmark](resource/benchmark.png)

For detailed timings, refer to the [benchmark results](resource/benchmark.txt).
