# -*- coding: utf-8 -*-
import sys


class ParserError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message


class Parser():
    def __init__(self):
        self.variables = {}
        self.tokens = []
        self.idx = 0


    def isName(self, name):
        return name.isalnum() and name[0].isalpha()


    def tokenize(self, string):
        op_symbols = ['=', '(', ')', '+', '-', '*', '/']
        self.tokens = []
        token = ''
        for symbol in string:
            if symbol.isspace() or symbol in op_symbols:
                if token != '':
                    self.tokens.append(token)
                if symbol in op_symbols:
                    self.tokens.append(symbol)
                token = ''
            else:
                token += symbol
        if token != '':
            self.tokens.append(token)


    def parseSum(self):
        return self.parseSumPrime(self.parseProduct())


    def parseSumPrime(self, acc):
        if (self.idx == len(self.tokens) or
            (self.tokens[self.idx] != '+' and self.tokens[self.idx] != '-') ):
            return acc

        if self.tokens[self.idx] == '+':
            self.idx += 1
            term = self.parseProduct()
            return self.parseSumPrime(acc + term)

        if self.tokens[self.idx] == '-':
            self.idx += 1
            term = self.parseProduct()
            return self.parseSumPrime(acc - term)

        raise ParserError('Sintax error')


    def parseProduct(self):
        return self.parseProductPrime(self.parseTerm())


    def parseProductPrime(self, acc):
        if (self.idx == len(self.tokens) or
            (self.tokens[self.idx] != '*' and self.tokens[self.idx] != '/') ):
            return acc

        if self.tokens[self.idx] == '*':
            self.idx += 1
            multiplier = self.parseTerm()
            return self.parseProductPrime(acc * multiplier)

        if self.tokens[self.idx] == '/':
            self.idx += 1
            divider = self.parseTerm()
            if divider == 0:
                raise ParserError('division by zero')
            return self.parseProductPrime(acc // divider)

        raise ParserError('Sintax error')


    def parseTerm(self):
        if self.idx == len(self.tokens):
            raise ParserError('Sintax error')

        if self.tokens[self.idx] == '-':
            self.idx += 1
            return -self.parseUnsigned()

        return self.parseUnsigned()


    def parseUnsigned(self):
        if self.idx == len(self.tokens):
            raise ParserError('Sintax error')

        if self.tokens[self.idx].isdigit():
            val = int(self.tokens[self.idx])
            self.idx += 1
            return val

        elif self.tokens[self.idx] == '(':
            self.idx += 1
            val = self.parseSum()
            if self.idx == len(self.tokens) or self.tokens[self.idx] != ')':
                raise ParserError('Parentheses balance')
            self.idx += 1
            return val

        else:
            if self.tokens[self.idx] in self.variables.keys():
                val = self.variables[self.tokens[self.idx]]
                self.idx += 1
                return val
            else:
                raise ParserError('Unknown variable {}'.format(
                    self.tokens[self.idx]))


    def parseLine(self, string):
        self.tokenize(string)
        varName = self.tokens[0]
        if not self.isName(varName):
            raise ParserError('Invalid variable name: {}'.format(
                self.tokens[0]))
        if self.tokens[1] != '=':
            raise ParserError('Invalid assignment operator: {}'.format(
                self.tokens[1]))

        self.idx = 2
        value = self.parseSum()

        if self.idx != len(self.tokens):
            raise ParserError('Sintax error')

        self.variables[varName] = value

        return '{} = {}'.format(varName, value)


    def parseLines(self, input_file, output_file):
        n_lines = 0

        if input_file is not None:
            inf = open(input_file, 'r')
        else:
            inf = sys.stdin

        if output_file is not None:
            otf = open(output_file, 'w')
        else:
            otf = sys.stdout

        for line in inf:
            n_lines += 1

            try:
                answer = self.parseLine(line)
            except ParserError as e:
                answer = 'Error in line {}: {}'.format(n_lines, e)

            otf.write(answer + '\n')

        if inf is not sys.stdin:
            inf.close()
        if otf is not sys.stdout:
            otf.close()

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    p = Parser()
    p.parseLines(input_file, output_file)
