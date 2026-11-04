"""Comprobaciones simbolicas sencillas para la exposicion de Poincare.

Son ejemplos y cuentas elementales. No prueban la conjetura ni verifican la prueba de Perelman.
"""
import sys

import sympy as sp


def check(name, ok):
    print(f"{'OK ' if ok else 'FAIL'} {name}")
    return bool(ok)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    t, c, s = sp.symbols("t c s", positive=True)
    w0 = sp.symbols("w0", positive=True)
    results = []

    # Esfera redonda de dimension n y radio r: Ric = (n - 1) g0, con g = r^2 g0.
    # La ecuacion dg/dt = -2 Ric da d(r^2)/dt = -2 (n - 1).
    n = sp.Integer(3)
    r2 = sp.Function("r2")
    solution = sp.dsolve(sp.Eq(r2(t).diff(t), -2 * (n - 1)), r2(t), ics={r2(0): 1})
    results.append(check("esfera S^3: r^2(t) = 1 - 4 t", sp.simplify(solution.rhs - (1 - 4 * t)) == 0))
    extinction = sp.solve(1 - 4 * t, t)[0]
    results.append(check("esfera S^3 unidad: desaparece en t = 1/4", extinction == sp.Rational(1, 4)))
    curvature = 6 / (1 - 4 * t)
    results.append(check("curvatura escalar 6 / r^2 tiende a infinito al desaparecer",
                         sp.limit(curvature, t, sp.Rational(1, 4), dir="-") == sp.oo))

    # Cota del tipo Colding-Minicozzi: W' <= -4 pi + 3 W / (4 (t + c)).
    # La igualdad acota W por arriba; su solucion cae por debajo de cero en tiempo finito.
    W = sp.Function("W")
    equation = sp.Eq(W(t).diff(t), -4 * sp.pi + 3 * W(t) / (4 * (t + c)))
    bound = (t + c) ** sp.Rational(3, 4) * (w0 / c ** sp.Rational(3, 4) - 16 * sp.pi * ((t + c) ** sp.Rational(1, 4) - c ** sp.Rational(1, 4)))
    residual = sp.simplify(bound.diff(t) - equation.rhs.subs(W(t), bound))
    results.append(check("la formula cerrada resuelve la igualdad", residual == 0))
    results.append(check("la formula cerrada empieza en w0", sp.simplify(bound.subs(t, 0) - w0) == 0))

    # La cota se anula cuando (t + c)^(1/4) = c^(1/4) + w0 / (16 pi c^(3/4)), que es un tiempo finito.
    root = (c ** sp.Rational(1, 4) + w0 / (16 * sp.pi * c ** sp.Rational(3, 4))) ** 4 - c
    results.append(check("la cota se anula en un tiempo finito", sp.simplify(bound.subs(t, root)) == 0))
    numeric = root.subs({c: 1, w0: 1}).evalf()
    print(f"Ejemplo con c = 1 y W(0) = 1: la cota llega a cero en t = {numeric:.4f}")

    print("TODO OK" if all(results) else "HAY FALLOS")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
