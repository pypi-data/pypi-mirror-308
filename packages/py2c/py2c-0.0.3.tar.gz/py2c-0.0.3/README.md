# py2c

Tools to bridge python and C.

To install:	```pip install py2c```

There's tools to generate Python wrappers for C code:

>>> c_filename = 'example.c'
>>> generate_python_wrappers(c_filename)  # doctest: +SKIP

There's tools to generate C code from Python code:

>>> tree = ast.parse(source)  # doctest: +SKIP
>>> codegen = CCodeGenerator()  # doctest: +SKIP
>>> c_code = codegen.generate(tree)  # doctest: +SKIP