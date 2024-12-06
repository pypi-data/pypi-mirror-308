from hisscl import parser, ast
import unittest
import io

class TestLiterals(unittest.TestCase):
    def test_integer(self):
        val = parser.Parser(io.StringIO('1234'), 'TestLiterals.test_integer')._parse_value()
        self.assertIsInstance(val, ast.Integer)
        assert type(val) is ast.Integer
        self.assertEqual(val.value, 1234)
    
    def test_float(self):
        val = parser.Parser(io.StringIO('1234.5678'), 'TestLiterals.test_float')._parse_value()
        self.assertIsInstance(val, ast.Float)
        assert type(val) is ast.Float
        self.assertEqual(val.value, 1234.5678)
    
    def test_string(self):
        val = parser.Parser(io.StringIO('"test \\" \\u26a7"'), 'TestLiterals.test_string')._parse_value()
        self.assertIsInstance(val, ast.String)
        assert type(val) is ast.String
        self.assertEqual(val.value, 'test " \u26a7')
    
    def test_bool(self):
        val = parser.Parser(io.StringIO('true'), 'TestLiterals.test_bool')._parse_value()
        self.assertIsInstance(val, ast.Bool)
        assert type(val) is ast.Bool
        self.assertEqual(val.value, True)
    
    def test_heredoc(self):
        val = parser.Parser(io.StringIO('<<EOT\nthis\nis\na\nmultiline\nstring\nEOT'), 'TestLiterals.test_heredoc')._parse_value()
        self.assertIsInstance(val, ast.String)
        assert type(val) is ast.String
        self.assertEqual(val.value, '\nthis\nis\na\nmultiline\nstring\n')
        
class TestCollections(unittest.TestCase):
    def test_tuple(self):
        val = parser.Parser(io.StringIO('[1, 2.0, "3", true]'), 'TestCollections.test_tuple')._parse_value()
        self.assertIsInstance(val, ast.Tuple)
        assert type(val) is ast.Tuple
        self.assertEqual(val.items, [
            ast.Integer(
                pos = ast.Position(name="TestCollections.test_tuple", line=1, col=2),
                value = 1,
            ),
            ast.Float(
                pos = ast.Position(name="TestCollections.test_tuple", line=1, col=5),
                value = 2.0,
            ),
            ast.String(
                pos = ast.Position(name="TestCollections.test_tuple", line=1, col=10),
                value = "3",
            ),
            ast.Bool(
                pos = ast.Position(name="TestCollections.test_tuple", line=1, col=15),
                value = True,
            ),
        ])
        
    def test_object(self):
        val = parser.Parser(io.StringIO('{true: 2.0, "3": 4, 5.0: "6"}'), 'TestCollections.test_object')._parse_value()
        self.assertIsInstance(val, ast.Object)
        assert type(val) is ast.Object
        self.assertEqual(val.items, [
            (
                ast.Bool(
                    pos = ast.Position(name="TestCollections.test_object", line=1, col=2),
                    value = True,
                ),
                ast.Float(
                    pos = ast.Position(name="TestCollections.test_object", line=1, col=8),
                    value = 2.0,
                ),
            ),
            (
                ast.String(
                    pos = ast.Position(name="TestCollections.test_object", line=1, col=13),
                    value = "3",
                ),
                ast.Integer(
                    pos = ast.Position(name="TestCollections.test_object", line=1, col=18),
                    value = 4,
                ),
            ),
            (
                ast.Float(
                    pos = ast.Position(name="TestCollections.test_object", line=1, col=21),
                    value = 5.0,
                ),
                ast.String(
                    pos = ast.Position(name="TestCollections.test_object", line=1, col=26),
                    value = "6",
                ),
            )
        ])

class TestExpressions(unittest.TestCase):
    def test_bare_value(self):
        val = parser.Parser(io.StringIO('1234'), 'TestExpressions.test_bare_value')._parse_expr()
        self.assertIsInstance(val, ast.Integer)
        assert type(val) is ast.Integer
        self.assertEqual(val.value, 1234)
    
    def test_binary(self):
        val = parser.Parser(io.StringIO('1234 == 5678'), 'TestExpressions.test_binary')._parse_expr()
        self.assertEqual(val, ast.BinaryExpression(
            pos = ast.Position(name='TestExpressions.test_binary', line=1, col=1),
            left = ast.Integer(
                pos = ast.Position(name='TestExpressions.test_binary', line=1, col=1),
                value = 1234,
            ),
            op = ast.Operator(
                pos = ast.Position(name='TestExpressions.test_binary', line=1, col=6),
                value = '==',
            ),
            right = ast.Integer(
                pos = ast.Position(name='TestExpressions.test_binary', line=1, col=9),
                value = 5678
            ),
        ))
        
    def test_binary_nested(self):
        val = parser.Parser(io.StringIO('(1234 - 5) == 5678'), 'TestExpressions.test_binary_nested')._parse_expr()
        self.assertEqual(val, ast.BinaryExpression(
            pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=2),
            left = ast.BinaryExpression(
                pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=2),
                left = ast.Integer(
                    pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=2),
                    value = 1234,
                ),
                op = ast.Operator(
                    pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=7),
                    value = '-',
                ),
                right = ast.Integer(
                    pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=9),
                    value = 5,
                ),
            ),
            op = ast.Operator(
                pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=12),
                value = '==',
            ),
            right = ast.Integer(
                pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=15),
                value = 5678
            ),
        ))
        
    def test_binary_multi(self):
        val = parser.Parser(io.StringIO('1234 == 5678 - 4444'), 'TestExpressions.test_binary_nested')._parse_expr()
        self.assertEqual(val, ast.BinaryExpression(
            pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=1),
            left = ast.Integer(
                pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=1),
                value = 1234,
            ),
            op = ast.Operator(
                pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=6),
                value = '==',
            ),
            right = ast.BinaryExpression(
                pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=9),
                left = ast.Integer(
                    pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=9),
                    value = 5678
                ),
                op = ast.Operator(
                    pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=14),
                    value = '-',
                ),
                right = ast.Integer(
                    pos = ast.Position(name='TestExpressions.test_binary_nested', line=1, col=16),
                    value = 4444,
                ),
            ),
        ))
        
    def test_expansion(self):
        val = parser.Parser(io.StringIO('x(y...)'), 'TestExpressions.test_expansion')._parse_expr()
        self.assertEqual(val, ast.FunctionCall(
            pos = ast.Position(name='TestExpressions.test_expansion', line=1, col=2),
            value = ast.VariableRef(
                pos = ast.Position(name='TestExpressions.test_expansion', line=1, col=1),
                name = 'x',
            ),
            args = [
                ast.Expansion(
                    pos = ast.Position(name='TestExpressions.test_expansion', line=1, col=3),
                    value = ast.VariableRef(
                        pos = ast.Position(name='TestExpressions.test_expansion', line=1, col=3),
                        name = 'y',
                    ),
                ),
            ],
        ))
        
    def test_index(self):
        val = parser.Parser(io.StringIO('x[0]'), 'TestExpressions.test_index')._parse_expr()
        self.assertIsInstance(val, ast.Index)
        assert type(val) is ast.Index
        self.assertEqual(val.value, ast.VariableRef(
            pos = ast.Position(name='TestExpressions.test_index', line=1, col=1),
            name = 'x',
        ))
        self.assertEqual(val.index, ast.Integer(
            pos = ast.Position(name='TestExpressions.test_index', line=1, col=3),
            value = 0,
        ))
        
    def test_index_legacy(self):
        val = parser.Parser(io.StringIO('x.0'), 'TestExpressions.test_index_legacy')._parse_expr()
        self.assertIsInstance(val, ast.Index)
        assert type(val) is ast.Index
        self.assertEqual(val.value, ast.VariableRef(
            pos = ast.Position(name='TestExpressions.test_index_legacy', line=1, col=1),
            name = 'x',
        ))
        self.assertEqual(val.index, ast.Integer(
            pos = ast.Position(name='TestExpressions.test_index_legacy', line=1, col=3),
            value = 0,
        ))
        
    def test_getattr(self):
        val = parser.Parser(io.StringIO('x.y'), 'TestExpressions.test_getattr')._parse_expr()
        self.assertIsInstance(val, ast.GetAttr)
        assert type(val) is ast.GetAttr
        self.assertEqual(val.value, ast.VariableRef(
            pos = ast.Position(name='TestExpressions.test_getattr', line=1, col=1),
            name = 'x',
        ))
        self.assertEqual(val.attr, 'y')
    
    def test_unary(self):
        val = parser.Parser(io.StringIO('!true'), 'TestExpressions.test_unary')._parse_value()
        self.assertIsInstance(val, ast.UnaryExpression)
        assert type(val) is ast.UnaryExpression
        self.assertEqual(val.op.value, '!')
        self.assertEqual(val.value, ast.Bool(
            pos = ast.Position(name="TestExpressions.test_unary", line=1, col=2),
            value = True,
        ))