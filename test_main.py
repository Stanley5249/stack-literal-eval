import ast
import contextlib
import sys
import unittest

from main import stack_literal_eval

# override with the new implementation
ast.literal_eval = stack_literal_eval


# copy from test.support
@contextlib.contextmanager
def adjust_int_max_str_digits(max_digits):
    """Temporarily change the integer string conversion length limit."""
    current = sys.get_int_max_str_digits()
    try:
        sys.set_int_max_str_digits(max_digits)
        yield
    finally:
        sys.set_int_max_str_digits(current)


class ConstantTests(unittest.TestCase):
    """Tests on the ast.Constant node type."""

    def test_literal_eval(self):
        tree = ast.parse("1 + 2")
        binop = tree.body[0].value  # type: ignore

        new_left = ast.Constant(value=10)
        ast.copy_location(new_left, binop.left)
        binop.left = new_left

        new_right = ast.Constant(value=20j)
        ast.copy_location(new_right, binop.right)
        binop.right = new_right

        self.assertEqual(ast.literal_eval(binop), 10 + 20j)


class ASTHelpers_Test(unittest.TestCase):
    maxDiff = None

    def test_literal_eval(self):
        self.assertEqual(ast.literal_eval("[1, 2, 3]"), [1, 2, 3])
        self.assertEqual(ast.literal_eval('{"foo": 42}'), {"foo": 42})
        self.assertEqual(ast.literal_eval("(True, False, None)"), (True, False, None))
        self.assertEqual(ast.literal_eval("{1, 2, 3}"), {1, 2, 3})
        self.assertEqual(ast.literal_eval('b"hi"'), b"hi")
        self.assertEqual(ast.literal_eval("set()"), set())
        self.assertRaises(ValueError, ast.literal_eval, "foo()")
        self.assertEqual(ast.literal_eval("6"), 6)
        self.assertEqual(ast.literal_eval("+6"), 6)
        self.assertEqual(ast.literal_eval("-6"), -6)
        self.assertEqual(ast.literal_eval("3.25"), 3.25)
        self.assertEqual(ast.literal_eval("+3.25"), 3.25)
        self.assertEqual(ast.literal_eval("-3.25"), -3.25)
        self.assertEqual(repr(ast.literal_eval("-0.0")), "-0.0")
        self.assertRaises(ValueError, ast.literal_eval, "++6")
        self.assertRaises(ValueError, ast.literal_eval, "+True")
        self.assertRaises(ValueError, ast.literal_eval, "2+3")

    def test_literal_eval_str_int_limit(self):
        with adjust_int_max_str_digits(4000):
            ast.literal_eval("3" * 4000)  # no error
            with self.assertRaises(SyntaxError) as err_ctx:
                ast.literal_eval("3" * 4001)
            self.assertIn("Exceeds the limit ", str(err_ctx.exception))
            self.assertIn(" Consider hexadecimal ", str(err_ctx.exception))

    def test_literal_eval_complex(self):
        # Issue #4907
        self.assertEqual(ast.literal_eval("6j"), 6j)
        self.assertEqual(ast.literal_eval("-6j"), -6j)
        self.assertEqual(ast.literal_eval("6.75j"), 6.75j)
        self.assertEqual(ast.literal_eval("-6.75j"), -6.75j)
        self.assertEqual(ast.literal_eval("3+6j"), 3 + 6j)
        self.assertEqual(ast.literal_eval("-3+6j"), -3 + 6j)
        self.assertEqual(ast.literal_eval("3-6j"), 3 - 6j)
        self.assertEqual(ast.literal_eval("-3-6j"), -3 - 6j)
        self.assertEqual(ast.literal_eval("3.25+6.75j"), 3.25 + 6.75j)
        self.assertEqual(ast.literal_eval("-3.25+6.75j"), -3.25 + 6.75j)
        self.assertEqual(ast.literal_eval("3.25-6.75j"), 3.25 - 6.75j)
        self.assertEqual(ast.literal_eval("-3.25-6.75j"), -3.25 - 6.75j)
        self.assertEqual(ast.literal_eval("(3+6j)"), 3 + 6j)
        self.assertRaises(ValueError, ast.literal_eval, "-6j+3")
        self.assertRaises(ValueError, ast.literal_eval, "-6j+3j")
        self.assertRaises(ValueError, ast.literal_eval, "3+-6j")
        self.assertRaises(ValueError, ast.literal_eval, "3+(0+6j)")
        self.assertRaises(ValueError, ast.literal_eval, "-(3+6j)")

    def test_literal_eval_malformed_dict_nodes(self):
        malformed = ast.Dict(
            keys=[ast.Constant(1), ast.Constant(2)], values=[ast.Constant(3)]
        )
        self.assertRaises(ValueError, ast.literal_eval, malformed)
        malformed = ast.Dict(
            keys=[ast.Constant(1)], values=[ast.Constant(2), ast.Constant(3)]
        )
        self.assertRaises(ValueError, ast.literal_eval, malformed)

    def test_literal_eval_trailing_ws(self):
        self.assertEqual(ast.literal_eval("    -1"), -1)
        self.assertEqual(ast.literal_eval("\t\t-1"), -1)
        self.assertEqual(ast.literal_eval(" \t -1"), -1)
        self.assertRaises(IndentationError, ast.literal_eval, "\n -1")

    def test_literal_eval_malformed_lineno(self):
        msg = r"malformed node or string on line 3:"
        with self.assertRaisesRegex(ValueError, msg):
            ast.literal_eval("{'a': 1,\n'b':2,\n'c':++3,\n'd':4}")

        node = ast.UnaryOp(ast.UAdd(), ast.UnaryOp(ast.UAdd(), ast.Constant(6)))
        self.assertIsNone(getattr(node, "lineno", None))
        msg = r"malformed node or string:"
        with self.assertRaisesRegex(ValueError, msg):
            ast.literal_eval(node)

    def test_literal_eval_syntax_errors(self):
        with self.assertRaisesRegex(SyntaxError, "unexpected indent"):
            ast.literal_eval(r"""
                \
                (\
            \ """)
