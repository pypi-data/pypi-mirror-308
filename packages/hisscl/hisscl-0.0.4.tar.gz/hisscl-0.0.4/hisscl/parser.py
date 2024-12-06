from . import ast
from . import lexer

from typing import TextIO

import ast as pyast

__all__ = ['ExpectedError', 'Parser']

class ExpectedError(Exception):
    def __init__(self, pos: ast.Position, expected: str, got: str):
        super().__init__(f'{pos}: expected {expected}; got {"EOF" if got == '' else repr(got)}')
        self.pos = pos
        self.got = got
        self.expected = expected

class Parser:
    def __init__(self, stream: TextIO, name: str):
        self.lexer = lexer.Lexer(stream, name)
        self._prev: tuple[lexer.Token, ast.Position, str] | None = None
        
    def _scan(self) -> tuple[lexer.Token, ast.Position, str]:
        if self._prev is not None:
            prev = self._prev
            self._prev = None
            return prev
        return self.lexer.scan()
    
    def _unscan(self, tok: lexer.Token, pos: ast.Position, lit: str):
        self._prev = tok, pos, lit
    
    def _parse_index(self, val: ast.Value, start_pos: ast.Position) -> ast.Index:
        index = ast.Index(pos=start_pos, value=val, index=self._parse_expr())
        tok, start_pos, lit = self._scan()
        if tok != lexer.Token.SQUARE or lit != ']':
            raise ExpectedError(start_pos, 'closing square bracket', lit)
        while self.lexer._peek(1) == '[':
            _, start_pos, _ = self._scan()
            index = self._parse_index(index, start_pos)
        return index
        
    def _parse_getattr(self, val: ast.Value, start_pos: ast.Position) -> ast.Index | ast.GetAttr:
        tok, pos, lit = self._scan()
        if tok == lexer.Token.INTEGER:
            return ast.Index(pos=start_pos, value=val, index=ast.Integer(pos=pos, value=int(lit)))
        elif tok == lexer.Token.IDENT:
            return ast.GetAttr(pos=start_pos, value=val, attr=lit)
        else:
            raise ExpectedError(pos, 'integer or identifier', lit)
        while self.lexer._peek(1) == '.':
            _, start_pos, _ = self._scan()
            index = self._parse_getattr(index, start_pos)
      
    def _parse_expr(self) -> ast.Value:
        left = self._parse_value()
        tok, pos, lit = self._scan()
        if tok != lexer.Token.OPERATOR:
            self._unscan(tok, pos, lit)
            return left
        right = self._parse_expr()
        return ast.BinaryExpression(pos=left.pos, op=ast.Operator(pos=pos, value=lit), left=left, right=right)
        
    def _parse_tuple(self, start_pos: ast.Position) -> ast.Tuple:
        items: list[ast.Value] = []
        while True:
            tok, pos, lit = self._scan()
            if tok == lexer.Token.SQUARE and lit == ']':
                break
            self._unscan(tok, pos, lit)
            items.append(self._parse_expr())
            
            tok, pos, lit = self._scan()
            if tok != lexer.Token.COMMA and (tok != lexer.Token.SQUARE or lit != ']'):
                raise ExpectedError(pos, 'comma or closing square bracket', lit)
            elif tok == lexer.Token.SQUARE and lit == ']':
                break
        return ast.Tuple(start_pos, items)
        
    def _parse_object(self, start_pos: ast.Position) -> ast.Object:
        items: list[tuple[ast.Value, ast.Value]] = []
        while True:
            tok, pos, lit = self._scan()
            if tok == lexer.Token.CURLY and lit == '}':
                break
            self._unscan(tok, pos, lit)
            key = self._parse_expr()
            
            tok, pos, lit = self._scan()
            if tok != lexer.Token.COLON and (tok != lexer.Token.OPERATOR or lit != '='):
                raise ExpectedError(pos, 'colon or equals sign', lit)
                
            val = self._parse_expr()
            items.append((key, val))
            
            tok, pos, lit = self._scan()
            if tok != lexer.Token.COMMA:
                self._unscan(tok, pos, lit)
            
        return ast.Object(start_pos, items)
        
    def _parse_func_call(self, val: ast.Value, start_pos: ast.Position) -> ast.FunctionCall:        
        tok, pos, lit = self._scan()        
        if tok == lexer.Token.PAREN and lit == ')':
            out = ast.FunctionCall(pos=start_pos, value=val, args=[])
            while self.lexer._peek(1) == '(':
                _, start_pos, _ = self._scan()
                out = self._parse_func_call(out, start_pos)
            return out
        self._unscan(tok, pos, lit)
        
        args: list[ast.Value] = []
        while True:
            args.append(self._parse_expr())
            tok, pos, lit = self._scan()
            if tok == lexer.Token.PAREN and lit == ')':
                break
            elif tok == lexer.Token.COMMA:
                continue
            elif tok == lexer.Token.ELLIPSIS:
                args[-1] = ast.Expansion(pos=args[-1].pos, value=args[-1])
                tok, pos, lit = self._scan()
                if tok != lexer.Token.PAREN or lit != ')':
                    raise ExpectedError(pos, 'closing parentheses', lit)
                break
            else:
                raise ExpectedError(pos, 'comma or closing parentheses', lit)
        
        out = ast.FunctionCall(pos=start_pos, value=val, args=args)
        while self.lexer._peek(1) == '(':
            _, start_pos, _ = self._scan()
            out = self._parse_func_call(out, start_pos)
        return out
    
    def _parse_value(self) -> ast.Value:
        out = None
        tok, pos, lit = self._scan()
        match tok:
            case lexer.Token.INTEGER:
                out = ast.Integer(pos=pos, value=int(lit))
            case lexer.Token.FLOAT:
                out = ast.Float(pos=pos, value=float(lit))
            case lexer.Token.BOOL:
                out = ast.Bool(pos=pos, value=(lit == 'true'))
            case lexer.Token.STRING:
                out = ast.String(pos=pos, value=pyast.literal_eval(lit))
            case lexer.Token.IDENT:
                out = ast.VariableRef(pos=pos, name=lit)
            case lexer.Token.HEREDOC:
                out = ast.String(pos=pos, value=lit)
            case lexer.Token.OPERATOR:
                out = ast.UnaryExpression(pos=pos, op=ast.Operator(pos=pos, value=lit), value=self._parse_value())
            case lexer.Token.SQUARE:
                if lit != '[':
                    raise ExpectedError(pos, repr('['), lit)
                out = self._parse_tuple(pos)
            case lexer.Token.CURLY:
                if lit != '{':
                    raise ExpectedError(pos, repr('{'), lit)
                out = self._parse_object(pos)
            case lexer.Token.PAREN:
                if lit != '(':
                    raise ExpectedError(pos, repr('('), lit)
                expr = self._parse_expr()
                tok, pos, lit = self._scan()
                if tok != lexer.Token.PAREN or lit != ')':
                    raise ExpectedError(pos, repr(')'), lit)
                out = expr
            case _:
                raise ExpectedError(pos, 'value', lit)
        
        tok, pos, lit = self._scan()
        if tok == lexer.Token.SQUARE and lit == '[':
            out = self._parse_index(out, pos)
        elif tok == lexer.Token.PAREN and lit == '(':
            out = self._parse_func_call(out, pos)
        elif tok == lexer.Token.DOT:
            out = self._parse_getattr(out, pos)
        else:
            self._unscan(tok, pos, lit)
        
        return out
        
    def parse(self, until: tuple[lexer.Token, str] = (lexer.Token.EOF, '')) -> ast.AST:
        tree = []
        while True:
            id_tok, id_pos, id_lit = self._scan()
            if id_tok == until[0] and id_lit == until[1]:
                break
            
            if id_tok != lexer.Token.IDENT:
                raise ExpectedError(id_pos, str(lexer.Token.IDENT), id_lit)
            
            tok, pos, lit = self._scan()
            if tok == lexer.Token.OPERATOR and lit == '=':
                tree.append(ast.Assignment(pos=id_pos, name=id_lit, value=self._parse_expr()))
            elif tok == lexer.Token.CURLY and lit == '{':
                tree.append(ast.Block(pos=id_pos, name=id_lit, labels=[], children=self.parse(until=(lexer.Token.CURLY, '}'))))
            elif tok in (lexer.Token.STRING, lexer.Token.IDENT):
                labels = []
                while tok in (lexer.Token.STRING, lexer.Token.IDENT):
                    if tok == lexer.Token.IDENT:
                        labels.append(lit)
                    else:
                        self._unscan(tok, pos, lit)
                        val = self._parse_value()
                        assert isinstance(val, ast.String)
                        labels.append(val.value)
                    tok, pos, lit = self._scan()
                if tok != lexer.Token.CURLY and lit != '{':
                    raise ExpectedError(pos, repr('{'), lit)
                tree.append(ast.Block(pos=id_pos, name=id_lit, labels=labels, children=self.parse(until=(lexer.Token.CURLY, '}'))))
            else:
                raise ExpectedError(pos, "equals sign, opening curly brace, or string", lit)
        return tree