import sympy as sy


def Bisection(a, b, tol, fx, niter) -> (float, dict, str):
    n = 0
    an, bn, E = [a], [b], [100]
    x = sy.symbols("x")

    try:
        fxExp = sy.parse_expr(fx)
    except Exception:
        return 0, None, "Invalid function"

    fa, fb = fxExp.evalf(subs={x: a}), fxExp.evalf(subs={x: b})

    xm = [(an[n] + bn[n]) / 2]
    fm = [fxExp.evalf(subs={x: xm[n]})]

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
        fm.append(fxExp.evalf(subs={x: xm[n]}))
        E.append(abs(xm[n-1]-xm[n]))

    if n == niter or not (E[n] < tol):
        err = f'Method failed in {niter} iterations'
        return 0, None, err

    table = {
        "rows": ["n", "a", "b", "xm", "f(xm)", "error"],
        "columns": [[i, an[i], bn[i], xm[i], fm[i], E[i]] for i in range(n+1)],
    }

    return xm[n], table, None
