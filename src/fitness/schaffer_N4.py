from math import cos, sin

fact1 = lambda x1, x2: (cos(sin(abs(x1**2-x2**2))))**2 - 0.5
fact2 = lambda x1, x2: (1 + 0.001*(x1**2+x2**2))**2

schaffer_N4 = lambda x1, x2: 0.5 + fact1(x1, x2) / fact2(x1, x2)

__all__ = ['schaffer_N4']
