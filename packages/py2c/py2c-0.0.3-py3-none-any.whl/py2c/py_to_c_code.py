"""
This module provides functionality to convert a subset of Python code into C code.
It uses the built-in `ast` module to parse Python code into an abstract syntax tree (AST)
and then traverses this AST to generate C code based on customizable mapping rules.

The module handles basic constructs such as:

- Operators
- Function calls
- Control flow statements (if, for, while)

Mapping dictionaries are used to define how different Python AST nodes are translated into C code.
These dictionaries can be edited to extend or modify the translation rules.

Usage:
    python py_to_c.py <python_file.py>

Example:
    Given a Python file `example.py` containing:
    
    ```python
    def add(a, b):
        return a + b

    x = add(5, 3)
    print(x)
    ```

    Running `python py_to_c.py example.py` will generate corresponding C code.
"""

import ast
import sys

# Mapping of Python operators to C operators
OPERATOR_MAP = {
    ast.Add: '+',
    ast.Sub: '-',
    ast.Mult: '*',
    ast.Div: '/',
    ast.Mod: '%',
    ast.Pow: '^',  # Note: C uses pow() function for exponentiation
    ast.Lt: '<',
    ast.Gt: '>',
    ast.LtE: '<=',
    ast.GtE: '>=',
    ast.Eq: '==',
    ast.NotEq: '!=',
    ast.And: '&&',
    ast.Or: '||',
    ast.Not: '!',
}

# Mapping of Python built-in functions to C functions
FUNCTION_MAP = {
    'print': 'printf',
    # Add more mappings as needed
}


# Base class for code generation
class CCodeGenerator(ast.NodeVisitor):
    def __init__(self):
        self.code = []
        self.indent_level = 0
        self.indent_with = '    '  # 4 spaces

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1

    def emit(self, code_line):
        indent = self.indent_with * self.indent_level
        self.code.append(f"{indent}{code_line}")

    def generate(self, node):
        self.visit(node)
        return '\n'.join(self.code)

    # Visit functions
    def visit_Module(self, node):
        self.emit('#include <stdio.h>')
        self.emit('')
        for stmt in node.body:
            self.visit(stmt)

    def visit_FunctionDef(self, node):
        args = ', '.join(
            ['int ' + arg.arg for arg in node.args.args]
        )  # Assuming all args are ints
        self.emit(f"int {node.name}({args})" + " {")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.dedent()
        self.emit('}')
        self.emit('')

    def visit_Return(self, node):
        self.emit('return ' + self.visit(node.value) + ';')

    def visit_Call(self, node):
        func_name = self.visit(node.func)
        args = ', '.join([self.visit(arg) for arg in node.args])
        return f"{func_name}({args})"

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        return repr(node.value)

    def visit_Assign(self, node):
        targets = ', '.join([self.visit(t) for t in node.targets])
        value = self.visit(node.value)
        self.emit(f"int {targets} = {value};")  # Assuming int type for simplicity

    def visit_Expr(self, node):
        self.emit(self.visit(node.value) + ';')

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = OPERATOR_MAP.get(type(node.op), '?')
        right = self.visit(node.right)
        return f"({left} {op} {right})"

    def visit_If(self, node):
        test = self.visit(node.test)
        self.emit(f"if ({test}) " + "{")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.dedent()
        self.emit('}')
        if node.orelse:
            self.emit('else {')
            self.indent()
            for stmt in node.orelse:
                self.visit(stmt)
            self.dedent()
            self.emit('}')

    def visit_Compare(self, node):
        left = self.visit(node.left)
        ops = [OPERATOR_MAP.get(type(op), '?') for op in node.ops]
        comparators = [self.visit(comp) for comp in node.comparators]
        comparison = ''
        for op, comp in zip(ops, comparators):
            comparison += f" {left} {op} {comp}"
            left = comp
        return comparison.strip()

    def visit_While(self, node):
        test = self.visit(node.test)
        self.emit(f"while ({test}) " + "{")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.dedent()
        self.emit('}')

    def visit_For(self, node):
        if not isinstance(node.target, ast.Name):
            raise NotImplementedError("Only simple for loops are supported.")
        iter_var = self.visit(node.target)
        if isinstance(node.iter, ast.Call) and node.iter.func.id == 'range':
            args = [self.visit(arg) for arg in node.iter.args]
            if len(args) == 1:
                start, end, step = '0', args[0], '1'
            elif len(args) == 2:
                start, end = args
                step = '1'
            elif len(args) == 3:
                start, end, step = args
            else:
                raise NotImplementedError("Unsupported range arguments.")
            self.emit(
                f"for (int {iter_var} = {start}; {iter_var} < {end}; {iter_var} += {step}) "
                + "{"
            )
            self.indent()
            for stmt in node.body:
                self.visit(stmt)
            self.dedent()
            self.emit('}')
        else:
            raise NotImplementedError("Only range() iterations are supported.")

    def visit_UnaryOp(self, node):
        op = OPERATOR_MAP.get(type(node.op), '?')
        operand = self.visit(node.operand)
        return f"({op}{operand})"

    def visit_BoolOp(self, node):
        op = OPERATOR_MAP.get(type(node.op), '?')
        values = [self.visit(v) for v in node.values]
        return f" {op} ".join(values)

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        op = OPERATOR_MAP.get(type(node.op), '?')
        value = self.visit(node.value)
        self.emit(f"{target} {op}= {value};")

    def visit_Attribute(self, node):
        value = self.visit(node.value)
        attr = node.attr
        return f"{value}.{attr}"

    def visit_Subscript(self, node):
        value = self.visit(node.value)
        index = self.visit(node.slice)
        return f"{value}[{index}]"

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Slice(self, node):
        raise NotImplementedError("Slices are not supported.")

    def visit_List(self, node):
        elements = [self.visit(el) for el in node.elts]
        return '{' + ', '.join(elements) + '}'

    def visit_Dict(self, node):
        raise NotImplementedError("Dictionaries are not supported.")

    def generic_visit(self, node):
        raise NotImplementedError(
            f"Node type {type(node).__name__} is not implemented."
        )


def main(python_file):
    with open(python_file, 'r') as file:
        source = file.read()

    tree = ast.parse(source)
    codegen = CCodeGenerator()
    c_code = codegen.generate(tree)

    c_filename = python_file.replace('.py', '.c')
    with open(c_filename, 'w') as file:
        file.write(c_code)

    print(f"C code generated and saved to {c_filename}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python py_to_c.py <python_file.py>")
    else:
        main(sys.argv[1])
