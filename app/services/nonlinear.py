import sympy as sy


# Evaluate the expression at a given point
def evaluate(expr, x):
    return float(expr.evalf(subs={sy.symbols("x"): x}))


# Parse a numeric parameter
def parse_param(expr):
    return float(sy.parse_expr(expr.replace("^", "**")).evalf())


# Parse a function expression
def parse_func(expr):
    return sy.parse_expr(expr.replace("^", "**"))


# Calculate the error
def error(x1, x0, relative):
    if relative:
        return abs((x1-x0)/x1)
    return abs(x1-x0)


def Bisection(
        a: str,
        b: str,
        fx: str,
        tol: float,
        niter: int,
        relativeError: bool) -> (float, dict, str):
    try:
        a, b = parse_param(a), parse_param(b)
        fxExp = parse_func(fx)
    except Exception:
        return 0, None, "Invalid function or interval"

    n = 0
    an, bn, E = [a], [b], [100]
    fa, fb = evaluate(fxExp, a), evaluate(fxExp, b)
    xm = [(an[n] + bn[n]) / 2]
    fm = [evaluate(fxExp, xm[n])]

    if fa == 0:
        return a, None, None
    elif fb == 0:
        return b, None, None
    elif fa*fb >= 0:
        err = f'[{a}, {b}] is not a valid interval'
        return 0, None, err

    while E[n] > tol and n < niter:
        if fm[n] == 0:
            return xm[n], None, None
        elif fa*fm[n] > 0:
            an.append(xm[n])
            bn.append(bn[n])
            fa = fm[n]
        else:
            an.append(an[n])
            bn.append(xm[n])
        n += 1
        xm.append((an[n]+bn[n])/2)
        fm.append(evaluate(fxExp, xm[n]))
        E.append(error(xm[n-1], xm[n], relativeError))

    if n == niter or not (E[n] < tol):
        err = f'Method failed in {niter} iterations'
        return 0, None, err

    table = {
        "columns": ["n", "a", "xm", "b", "f(xm)", "error"],
        "rows": [[i, an[i], xm[i], bn[i], fm[i], E[i]] for i in range(n+1)],
    }

    return xm[n], table, None


def Fixed_point(
        x0: str,
        fx: str,
        gx: str,
        tol: float,
        niter: int,
        relativeError: bool) -> (float, dict, str):
    try:
        x0 = parse_param(x0)
        fxExp = parse_func(fx)
        gxExp = parse_func(gx)
    except Exception:
        return 0, None, "Invalid function or initial value"

    x, n = x0, 0
    xn, fn, E = [x], [evaluate(fxExp, x)], [100]

    while E[n] > tol and n < niter:
        x = evaluate(gxExp, x)
        if fn[n] == 0:
            return x, None, None

        n += 1
        xn.append(x)
        fn.append(evaluate(fxExp, x))
        E.append(error(xn[n], xn[n-1], relativeError))

    if n >= niter or not (E[n] < tol):
        err = f'Method failed in {niter} iterations'
        return 0, None, err

    table = {
        "columns": ["n", "x", "f(x)", "error"],
        "rows": [[i, xn[i], fn[i], E[i]] for i in range(n+1)],
    }
    return x, table, None


def False_position(
        a: str,
        b: str,
        fx: str,
        tol: float,
        niter: int,
        relativeError: bool) -> (float, dict, str):
    try:
        a, b = parse_param(a), parse_param(b)
        fxExp = parse_func(fx)
    except Exception:
        return 0, None, "Invalid function or interval"

    n = 0
    an, bn, E = [a], [b], [100]
    fa, fb = evaluate(fxExp, a), evaluate(fxExp, b)
    xm = [bn[n] - fb*(bn[n]-an[n])/(fb-fa)]
    fm = [evaluate(fxExp, xm[n])]

    if fa == 0:
        return a, None, None
    elif fb == 0:
        return b, None, None
    elif fa*fb >= 0:
        err = f'[{a}, {b}] is not a valid interval'
        return 0, None, err

    while E[n] > tol and n <= niter:
        if fm[n]*fb < 0:
            an.append(xm[n])
            bn.append(bn[n])
            fa = fm[n]
        else:
            bn.append(xm[n])
            an.append(an[n])
            fb = fm[n]
        n += 1
        xm.append(bn[n] - fb*(bn[n]-an[n])/(fb-fa))
        fm.append(evaluate(fxExp, xm[n]))
        E.append(error(xm[n], xm[n-1], relativeError))

    if n == niter or not (E[n] < tol):
        err = f'Method failed in {niter} iterations'
        return 0, None, err

    table = {
        "columns": ["n", "a", "xm", "b", "f(xm)", "error"],
        "rows": [[i, an[i], xm[i], bn[i], fm[i], E[i]] for i in range(n+1)],
    }
    return xm[n], table, None


def Newton(
        x0: str,
        fx: str,
        tol: float,
        niter: int,
        relativeError: bool) -> (float, dict, str):
    try:
        x0 = parse_param(x0)
        fxExp = parse_func(fx)
        fdExp = sy.diff(fxExp, sy.symbols("x"))
    except Exception:
        return 0, None, "Invalid function or interval"

    n = 0
    xn, fn, E = [x0], [evaluate(fxExp, x0)], [100]

    if fn[n] == 0:
        return xn[n], None, None

    while E[n] > tol and n < niter:
        fdx = evaluate(fdExp, xn[n])
        if fdx == 0:
            err = "Derivative is zero"
            return 0, None, err
        x = xn[n] - evaluate(fxExp, xn[n])/fdx
        xn.append(x)
        fn.append(evaluate(fxExp, x))
        E.append(error(x, xn[n], relativeError))
        n += 1

    if n == niter or not (E[n] < tol):
        err = f'Method failed in {niter} iterations'
        return 0, None, err

    table = {
        "columns": ["n", "x", "f(x)", "error"],
        "rows": [[i, xn[i], fn[i], E[i]] for i in range(n+1)],
    }
    return xn[n], table, None


def Secant(
        x0: str,
        x1: str,
        fx: str,
        tol: float,
        niter: int,
        relativeError: bool) -> (float, dict, str):

    try:
        x0, x1 = parse_param(x0), parse_param(x1)
        fxExp = parse_func(fx)
    except Exception:
        return 0, None, "Invalid function or interval"

    n = 1
    E = [100, 100]
    fx0, fx1 = evaluate(fxExp, x0), evaluate(fxExp, x1)
    xn, fx = [x0, x1], [fx0, fx1]

    if fx0 == 0:
        return x0, None, None
    elif fx1 == 0:
        return x1, None, None

    while n < niter:
        xn.append(x1 - fx1*(x1-x0)/(fx1-fx0))
        fx.append(evaluate(fxExp, xn[n]))
        if fx[n] == 0:
            return xn[n], None, None
        n += 1
        E.append(error(xn[n], xn[n-1], relativeError))
        if E[n] < tol:
            break
        x0, x1 = x1, xn[n]
        fx0, fx1 = evaluate(fxExp, x0), evaluate(fxExp, x1)
        if fx1 == fx0:
            return 0, None, "Division by zero"

    if n == niter or not (E[n] < tol):
        err = f'Method failed in {niter} iterations'
        return 0, None, err

    table = {
        "columns": ["n", "x", "f(x)", "error"],
        "rows": [[i, xn[i], fx[i], E[i]] for i in range(n+1)],
    }
    return xn[n], table, None
