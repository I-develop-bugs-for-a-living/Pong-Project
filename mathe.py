import sympy
import math

x = sympy.Symbol('x')
print(sympy.solvers.solve((x**2)+((2*x)**2)-(6**2), x))