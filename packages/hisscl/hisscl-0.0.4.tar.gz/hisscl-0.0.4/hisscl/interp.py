from . import ast
from . import parser

import typing
import io

__all__ = ['OperandError', 'Block', 'Interp']

class OperandError(Exception):
    def __init__(self, pos: ast.Position, action: str, issue: str, val: typing.Any):
        super().__init__(f'{pos}: cannot perform {action} on {issue} operand ({type(val).__name__})')

class Block(dict):
    def __init__(self, labels: list[str]):
        self.labels = labels
        super().__init__()

class Interp:    
    def __init__(self, stream: typing.TextIO, name: str):
        self.vars: dict[str, typing.Any] = {}
        self.parser = parser.Parser(stream, name)
        
    def __setitem__(self, key, val):
        self.vars[key] = val
    
    def __getitem__(self, key) -> typing.Any:
        return self.vars[key]
    
    def __delitem__(self, key):
        del self.vars[key]
    
    def update(self, vars: dict[str, typing.Any]):
        self.vars.update(vars)
    
    def _eval_index(self, index: ast.Index) -> typing.Any:
        val = self._convert_value(index.value)
        if not hasattr(val, '__getitem__'):
            raise ValueError(f'{index.value.pos}: value is not indexable ({type(val).__name__})')
        index_val = self._convert_value(index.index)
        if type(index_val) is int and hasattr(val, '__len__') and index_val >= len(val):
            raise IndexError(f'{index.index.pos}: index out of range ({index_val} with length {len(val)})')
        elif type(index_val) is not int:
            if isinstance(val, list) or isinstance(val, tuple) or isinstance(val, str):
                raise TypeError(f'{index.index.pos}: {type(val).__name__} indices must be integers, not {type(index_val).__name__}')
            elif hasattr(val, '__contains__') and index_val not in val:
                raise IndexError(f'{index.index.pos}: index {repr(index_val)} does not exist in value')
        return val[index_val]
    
    def _convert_value(self, val: ast.Value) -> typing.Any:
        if isinstance(val, ast.VariableRef):
            if val.name not in self.vars:
                raise KeyError(f'{val.pos}: no such variable: {repr(val.name)}')
            return self.vars[val.name]
        elif isinstance(val, ast.FunctionCall):
            return self._exec_func_call(val)
        elif isinstance(val, ast.Literal):
            return val.value
        elif isinstance(val, ast.Tuple):
            return [self._convert_value(item) for item in val.items]
        elif isinstance(val, ast.Object):
            return {self._convert_value(key): self._convert_value(value) for key, value in val.items}
        elif isinstance(val, ast.BinaryExpression):
            return self._eval_binary_expr(val)
        elif isinstance(val, ast.UnaryExpression):
            return self._eval_unary_expr(val)
        elif isinstance(val, ast.Index):
            return self._eval_index(val)
        elif isinstance(val, ast.GetAttr):
            obj = self._convert_value(val.value)
            if not hasattr(obj, val.attr):
                raise AttributeError(f'{val.pos}: no such attribute {repr(val.attr)} in object of type {type(obj).__name__}')
            return getattr(obj, val.attr)
        elif isinstance(val, ast.Expansion):
            raise ValueError(f'{val.pos}: cannot use expansion operator outside of a function call')
    
    def _is_numerical(self, val: typing.Any) -> bool:
        return isinstance(val, float | int) and type(val) is not bool
    
    def _is_comparable(self, val: typing.Any) -> bool:
        return self._is_numerical(val) or isinstance(val, str)
    
    def _exec_func_call(self, call: ast.FunctionCall) -> typing.Any:
        val = self._convert_value(call.value)
        if not callable(val):
            raise ValueError(f'{call.pos}: cannot call non-callable object')
        args = []
        for arg in call.args:
            if isinstance(arg, ast.Expansion):
                arg_val = self._convert_value(arg.value)
                if not isinstance(arg_val, typing.Iterable):
                    raise ValueError(f"{arg.pos}: cannot perform expansion on non-iterable value ({type(arg_val).__name__})")
                args.extend(arg_val)
            else:
                args.append(self._convert_value(arg))
        return val(*args)
        
    def _eval_unary_expr(self, expr: ast.UnaryExpression) -> float | int | bool:
        val = self._convert_value(expr.value)
        match expr.op.value:
            case '!':
                if type(val) is not bool:
                    raise OperandError(expr.value.pos, 'NOT operation', 'non-boolean', val)
                return not val
            case '-':
                if not self._is_numerical(val):
                    raise OperandError(expr.value.pos, 'negation', 'non-numerical', val)
                return -val
            case _:
                raise ValueError(f'{expr.op.pos}: unknown unary operation: {repr(expr.op.value)}')
    
    def _eval_binary_expr(self, expr: ast.BinaryExpression) -> float | int | bool:
        left = self._convert_value(expr.left)
        right = self._convert_value(expr.right)
                
        match expr.op.value:
            case '==':
                return left == right
            case '!=':
                return left != right
            case '+':
                if not self._is_numerical(left):
                    raise OperandError(expr.left.pos, 'addition operation', 'non-numerical', left)
                elif not self._is_numerical(right):
                    raise OperandError(expr.right.pos, 'addition operation', 'non-numerical', right)
                return left + right
            case '-':
                if not self._is_numerical(left):
                    raise OperandError(expr.left.pos, 'subtraction operation', 'non-numerical', left)
                elif not self._is_numerical(right):
                    raise OperandError(expr.right.pos, 'subtraction operation', 'non-numerical', right)
                return left - right
            case '*':
                if not self._is_numerical(left):
                    raise OperandError(expr.left.pos, 'multiplication operation', 'non-numerical', left)
                elif not self._is_numerical(right):
                    raise OperandError(expr.right.pos, 'multiplication operation', 'non-numerical', right)
                return left * right
            case '/':
                if not self._is_numerical(left):
                    raise OperandError(expr.left.pos, 'division operation', 'non-numerical', left)
                elif not self._is_numerical(right):
                    raise OperandError(expr.right.pos, 'division operation', 'non-numerical', right)
                return left / right
            case '%':
                if not self._is_numerical(left):
                    raise OperandError(expr.left.pos, 'modulo operation', 'non-numerical', left)
                elif not self._is_numerical(right):
                    raise OperandError(expr.right.pos, 'modulo operation', 'non-numerical', right)
                return left % right
            case '>':
                if not self._is_comparable(left):
                    raise OperandError(expr.left.pos, 'comparison', 'non-comparable', left)
                elif not self._is_comparable(right):
                    raise OperandError(expr.right.pos, 'comparison', 'non-comparable', right)
                return left > right
            case '<':
                if not self._is_comparable(left):
                    raise OperandError(expr.left.pos, 'comparison', 'non-comparable', left)
                elif not self._is_comparable(right):
                    raise OperandError(expr.right.pos, 'comparison', 'non-comparable', right)
                return left < right
            case '<=':
                if not self._is_comparable(left):
                    raise OperandError(expr.left.pos, 'comparison', 'non-comparable', left)
                elif not self._is_comparable(right):
                    raise OperandError(expr.right.pos, 'comparison', 'non-comparable', right)
                return left <= right
            case '>=':
                if not self._is_comparable(left):
                    raise OperandError(expr.left.pos, 'comparison', 'non-comparable', left)
                elif not self._is_comparable(right):
                    raise OperandError(expr.right.pos, 'comparison', 'non-comparable', right)
                return left >= right
            case '||':
                if type(left) is not bool:
                    raise OperandError(expr.left.pos, 'OR operation', 'non-boolean', left)
                elif type(right) is not bool:
                    raise OperandError(expr.right.pos, 'OR operation', 'non-boolean', right)
                return left or right
            case '&&':
                if type(left) is not bool:
                    raise OperandError(expr.left.pos, 'AND operation', 'non-boolean', left)
                elif type(right) is not bool:
                    raise OperandError(expr.right.pos, 'AND operation', 'non-boolean', right)
                return left and right
            case _:
                raise ValueError(f'{expr.op.pos}: unknown binary operation: {repr(expr.op.value)}')

    def _run(self, tree: ast.AST, cfg: dict[typing.Any, typing.Any]):
        for stmt in tree:
            if isinstance(stmt, ast.Assignment):
                if stmt.name in cfg:
                    raise KeyError(f'{stmt.pos}: {repr(stmt.name)} is already defined')
                cfg[stmt.name] = self._convert_value(stmt.value)
            elif isinstance(stmt, ast.Block):
                if stmt.name in cfg and (not isinstance(cfg[stmt.name], list) or type(cfg[stmt.name][0]) is not Block):
                    raise KeyError(f'{stmt.pos}: {repr(stmt.name)} is already defined')
                elif stmt.name not in cfg:
                    cfg[stmt.name] = []
                block = Block(stmt.labels)
                self._run(stmt.children, block)
                cfg[stmt.name].append(block)
    
    def run(self) -> dict[typing.Any, typing.Any]:
        cfg = {}
        self._run(self.parser.parse(), cfg)
        return cfg