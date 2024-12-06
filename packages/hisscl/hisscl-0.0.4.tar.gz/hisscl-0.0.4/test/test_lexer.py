from hisscl import lexer
import unittest
import io

class TestComments(unittest.TestCase):
    def test_double_slash(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('// this should be ignored'), 'TestComments.test_double_slash').scan()
        self.assertEqual(tok, lexer.Token.EOF)
        self.assertEqual(lit, '')
        
    def test_pound(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('# this should be ignored'), 'TestComments.test_pound').scan()
        self.assertEqual(tok, lexer.Token.EOF)
        self.assertEqual(lit, '')
        
    def test_multiline(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('/* this\nshould\nbe\nignored */'), 'TestComments.test_multiline').scan()
        self.assertEqual(tok, lexer.Token.EOF)
        self.assertEqual(lit, '')

class TestOperators(unittest.TestCase):
    def test_lt(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('<'), 'TestOperators.test_lt').scan()
        self.assertEqual(tok, lexer.Token.OPERATOR)
        self.assertEqual(lit, '<')
        
    def test_div(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('/'), 'TestOperators.test_div').scan()
        self.assertEqual(tok, lexer.Token.OPERATOR)
        self.assertEqual(lit, '/')
        
    def test_multichar(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('<='), 'TestOperators.test_multichar').scan()
        self.assertEqual(tok, lexer.Token.OPERATOR)
        self.assertEqual(lit, '<=')
    
    def test_ellipsis(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('...'), 'TestOperators.test_ellipsis').scan()
        self.assertEqual(tok, lexer.Token.ELLIPSIS)
        self.assertEqual(lit, '...')
    
    def test_invalid_ellipsis(self):
        with self.assertRaises(lexer.ExpectedError) as ctx:
            lexer.Lexer(io.StringIO('..'), 'TestOperators.test_invalid_ellipsis').scan()
        self.assertIn("expected .", str(ctx.exception))
        self.assertIn("got EOF", str(ctx.exception))
        
class TestHeredoc(unittest.TestCase):
    def test_heredoc(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('<<EOT\nthis\nis\na\nmultiline\nstring\nEOT'), 'TestHeredoc.test_heredoc').scan()
        self.assertEqual(tok, lexer.Token.HEREDOC)
        self.assertEqual(lit, '\nthis\nis\na\nmultiline\nstring\n')

class TestNumber(unittest.TestCase):
    def test_integer(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('1234'), 'TestNumber.test_integer').scan()
        self.assertEqual(tok, lexer.Token.INTEGER)
        self.assertEqual(lit, "1234")
    
    def test_float(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('1234.5678'), 'TestNumber.test_float').scan()
        self.assertEqual(tok, lexer.Token.FLOAT)
        self.assertEqual(lit, "1234.5678")
    
    def test_invalid_float(self):
        with self.assertRaises(lexer.ExpectedError) as ctx:
            lexer.Lexer(io.StringIO('1.0.0'), 'TestNumber.test_invalid_float').scan()
        self.assertIn("expected number", str(ctx.exception))
        self.assertIn("got '.'", str(ctx.exception))

class TestString(unittest.TestCase):
    def test_basic(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('""'), 'TestString.test_basic').scan()
        self.assertEqual(tok, lexer.Token.STRING)
        self.assertEqual(lit, '""')
        
    def test_escape(self):
        tok, pos, lit = lexer.Lexer(io.StringIO('"\\""'), 'TestString.test_escape').scan()
        self.assertEqual(tok, lexer.Token.STRING)
        self.assertEqual(lit, '"\\""')
        
    def test_newline(self):
        with self.assertRaises(lexer.ExpectedError) as ctx:
            lexer.Lexer(io.StringIO('"\n"'), 'TestString.test_newline').scan()
        self.assertIn("expected '\"'", str(ctx.exception))
        self.assertIn("got '\\n'", str(ctx.exception))