from hisscl import interp
import unittest
import io

class TestBasic(unittest.TestCase):
    def test_assignment(self):
        cfg = interp.Interp(io.StringIO("x = 26.04"), "TestBasic.test_assignment").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 26.04)

    def test_block(self):
        cfg = interp.Interp(io.StringIO("x { y = 26.04 }"), "TestBasic.test_block").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], [{'y': 26.04}])

    def test_block_labels(self):
        cfg = interp.Interp(io.StringIO("x y { z = 26.04 }"), "TestBasic.test_block_labels").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], [{'z': 26.04}])
        self.assertEqual(cfg['x'][0].labels, ['y'])

class TestExpressions(unittest.TestCase):
    def test_add(self):
        cfg = interp.Interp(io.StringIO("x = 123 + 333"), "TestExpressions.test_add").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 456)

    def test_sub(self):
        cfg = interp.Interp(io.StringIO("x = 456 - 333"), "TestExpressions.test_sub").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 123)

    def test_mul(self):
        cfg = interp.Interp(io.StringIO("x = 128 * 2"), "TestExpressions.test_mul").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 256)

    def test_div(self):
        cfg = interp.Interp(io.StringIO("x = 256 / 2"), "TestExpressions.test_div").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 128)

    def test_mod(self):
        cfg = interp.Interp(io.StringIO("x = 256 % 3"), "TestExpressions.test_mod").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 1)
        
    def test_eq(self):
        cfg = interp.Interp(io.StringIO("x = 123 == 456"), "TestExpressions.test_eq").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], False)
        
    def test_ne(self):
        cfg = interp.Interp(io.StringIO("x = 123 != 456"), "TestExpressions.test_ne").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], True)

    def test_lt(self):
        cfg = interp.Interp(io.StringIO("x = 123 < 456"), "TestExpressions.test_lt").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], True)

    def test_gt(self):
        cfg = interp.Interp(io.StringIO("x = 123 > 456"), "TestExpressions.test_gt").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], False)

    def test_le(self):
        cfg = interp.Interp(io.StringIO("x = 123 <= 123"), "TestExpressions.test_le").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], True)

    def test_ge(self):
        cfg = interp.Interp(io.StringIO("x = 1234 >= 123"), "TestExpressions.test_ge").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], True)

    def test_or(self):
        cfg = interp.Interp(io.StringIO("x = true || false"), "TestExpressions.test_or").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], True)
        
    def test_and(self):
        cfg = interp.Interp(io.StringIO("x = true && false"), "TestExpressions.test_and").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], False)
        
    def test_not(self):
        cfg = interp.Interp(io.StringIO("x = !true"), "TestExpressions.test_not").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], False)
        
    def test_neg(self):
        cfg = interp.Interp(io.StringIO("x = -1"), "TestExpressions.test_neg").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], -1)

class TestRefs(unittest.TestCase):
    def test_var(self):
        i = interp.Interp(io.StringIO("x = 123 + y"), "TestRefs.test_var")
        i['y'] = 333
        cfg = i.run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 456)
        
    def test_index(self):
        i = interp.Interp(io.StringIO('x = y[1]'), "TestRefs.test_index")
        i['y'] = [123, 456, 789]
        cfg = i.run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 456)
        
    def test_multi_index(self):
        cfg = interp.Interp(io.StringIO('x = ["123", "456", "789"][1][2]'), "TestRefs.test_multi_index").run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], '6')
        
    def test_index_legacy(self):
        i = interp.Interp(io.StringIO('x = y.1'), "TestRefs.test_index_legacy")
        i['y'] = [123, 456, 789]
        cfg = i.run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 456)
        
    def test_getattr(self):
        class Y:
            z = 123
        i = interp.Interp(io.StringIO('x = Y.z'), "TestRefs.test_getattr")
        i['Y'] = Y()
        cfg = i.run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 123)

    def test_func(self):
        def y(a, b):
            return a + b
        i = interp.Interp(io.StringIO("x = y(123, 333)"), "TestRefs.test_func")
        i['y'] = y
        cfg = i.run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 456)

    def test_func_expansion(self):
        def y(a, b):
            return a + b
        i = interp.Interp(io.StringIO("x = y(z...)"), "TestRefs.test_func_expansion")
        i['y'] = y
        i['z'] = (123, 333)
        cfg = i.run()
        self.assertIn('x', cfg)
        self.assertEqual(cfg['x'], 456)

    def test_call_uncallable(self):
        i = interp.Interp(io.StringIO("x = y(123, 333)"), "TestRefs.test_call_uncallable")
        i['y'] = 0
        with self.assertRaises(ValueError) as ctx:
            cfg = i.run()
        self.assertIn('cannot call non-callable object', str(ctx.exception))
