# -*- coding: utf-8 -*-
import ast
import pycodestyle


class Flake8Pep3101(object):

    name = 'flake8_pep3101'
    version = '1.0'
    message = 'S001 found module formatter'

    def __init__(self, tree, filename):
        self.filename = filename
        self.tree = tree

    def run(self):
        if self.filename is 'stdin':
            lines = pycodestyle.stdin_get_value().splitlines()
            tree = ast.parse(lines)
        elif self.tree:
            tree = self.tree
        else:
            with open(self.filename) as f:
                tree = ast.parse(f.read())

        for stmt in ast.walk(tree):
            if isinstance(stmt, ast.BinOp) and \
                    isinstance(stmt.op, ast.Mod) and \
                    isinstance(stmt.left, ast.Str):
                yield stmt.lineno, stmt.col_offset, self.message, type(self)
