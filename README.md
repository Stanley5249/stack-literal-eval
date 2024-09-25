# Stack-based `ast.literal_eval`

## Purpose

### Avoiding Recursion Errors

Using a stack to implement `literal_eval` can avoid `RecursionError`.

### Removing Unnecessary Closures

Related to a closed issue [#75934](https://github.com/python/cpython/issues/75934).

## Running Tests

The tests are copied from the CPython main branch, retaining only those related to `ast.literal_eval`. To run the tests, use the following command:

```sh
python -m unittest test_main.py