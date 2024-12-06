"""Tools to bridge Python and C.

There's tools to generate Python wrappers for C code:

>>> c_filename = 'example.c'
>>> generate_python_wrappers(c_filename)  # doctest: +SKIP


There's tools to generate C code from Python code:

>>> tree = ast.parse(source)  # doctest: +SKIP
>>> codegen = CCodeGenerator()  # doctest: +SKIP
>>> c_code = codegen.generate(tree)  # doctest: +SKIP

"""

from py2c.py_to_c_code import CCodeGenerator
from py2c.c_to_py_code import generate_python_wrappers
