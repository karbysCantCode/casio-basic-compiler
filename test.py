from enum import Enum, auto
from typing import List, Optional, Union


# === Token and Type ===
class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    OPERATOR = auto()
    TYPEKEYWORD = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    SEMICOLON = auto()


class Token:
    def __init__(self, type_: TokenType, content: str):
        self.type = type_
        self.content = content

    def __repr__(self):
        return f"{self.type.name}({self.content})"


# === AST Nodes ===
class ASTNode:
    pass


class VariableDeclaration(ASTNode):
    def __init__(self, var_type: str, identifier: str, value: ASTNode):
        self.var_type = var_type
        self.identifier = identifier
        self.value = value


class BinaryExpression(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right


class NumberLiteral(ASTNode):
    def __init__(self, value: str):
        self.value = value


class Variable(ASTNode):
    def __init__(self, name: str):
        self.name = name


class FunctionCall(ASTNode):
    def __init__(self, name: str, arguments: List[ASTNode]):
        self.name = name
        self.arguments = arguments


# === Parser ===
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token(TokenType.SEMICOLON, '')

    def consume(self) -> Token:
        current = self.peek()
        self.pos += 1
        return current

    def match(self, *types) -> bool:
        if self.peek().type in types:
            self.consume()
            return True
        return False

    def parse(self) -> ASTNode:
        if self.peek().type == TokenType.TYPEKEYWORD:
            return self.parse_variable_declaration()
        else:
            return self.parse_expression()

    def parse_variable_declaration(self) -> VariableDeclaration:
        var_type = self.consume().content
        identifier = self.consume().content
        assert self.match(TokenType.ASSIGN), "Expected '='"
        value = self.parse_expression()
        self.match(TokenType.SEMICOLON)
        return VariableDeclaration(var_type, identifier, value)

    def parse_expression(self, precedence=0) -> ASTNode:
        expr = self.parse_primary()

        while True:
            op = self.peek()
            if op.type == TokenType.OPERATOR and self.get_precedence(op.content) > precedence:
                self.consume()
                right = self.parse_expression(self.get_precedence(op.content))
                expr = BinaryExpression(expr, op.content, right)
            else:
                break

        return expr

    def parse_primary(self) -> ASTNode:
        token = self.peek()

        if token.type == TokenType.NUMBER:
            self.consume()
            return NumberLiteral(token.content)

        elif token.type == TokenType.IDENTIFIER:
            self.consume()
            if self.match(TokenType.LPAREN):
                args = []
                if self.peek().type != TokenType.RPAREN:
                    while True:
                        args.append(self.parse_expression())
                        if not self.match(TokenType.COMMA):
                            break
                assert self.match(TokenType.RPAREN), "Expected ')'"
                return FunctionCall(token.content, args)
            else:
                return Variable(token.content)

        elif self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            assert self.match(TokenType.RPAREN), "Expected ')'"
            return expr

        raise SyntaxError(f"Unexpected token: {token}")

    def get_precedence(self, operator: str) -> int:
        return {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }.get(operator, 0)


# === Example Usage ===
tokens = [
    Token(TokenType.TYPEKEYWORD, 'int'),
    Token(TokenType.IDENTIFIER, 'x'),
    Token(TokenType.ASSIGN, '='),
    Token(TokenType.NUMBER, '1'),
    Token(TokenType.OPERATOR, '+'),
    Token(TokenType.NUMBER, '2'),
    Token(TokenType.OPERATOR, '*'),
    Token(TokenType.LPAREN, '('),
    Token(TokenType.NUMBER, '3'),
    Token(TokenType.OPERATOR, '+'),
    Token(TokenType.NUMBER, '4'),
    Token(TokenType.RPAREN, ')'),
    Token(TokenType.SEMICOLON, ';')
]

parser = Parser(tokens)
ast = parser.parse()

print(ast.)

#chatgpt code bc i dont understand :(