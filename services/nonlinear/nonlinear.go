package nonlinear

import (
	"errors"
	"fmt"
	"math"

	"github.com/Pramod-Devireddy/go-exprtk"
	clc "github.com/TheDemx27/calculus"
)

func newExpression(exp string) (exprtk.GoExprtk, error) {
	expression := exprtk.NewExprtk()
	expression.SetExpression(exp)
	expression.AddDoubleVariable("x")

	err := expression.CompileExpression()
	if err != nil || exp == "" {
		return expression, errors.New("please enter a valid expression")
	}
	return expression, nil
}

func evaluateExp(exp *exprtk.GoExprtk, x float64) float64 {
	exp.SetDoubleVariableValue("x", x)
	return exp.GetEvaluatedValue()
}

func Bisection(a, b, tol float64, fx string, niter int) (float64, map[string]interface{}, error) {
	n := 0
	an, bn, E := []float64{a}, []float64{b}, []float64{100}

	// Evaluate interval
	fxExp, err := newExpression(fx)
	if err != nil {
		return 0, nil, err
	}

	defer fxExp.Delete()
	fa, fb := evaluateExp(&fxExp, an[n]), evaluateExp(&fxExp, b)

	xm := []float64{(an[n] + bn[n]) / 2}
	fm := []float64{evaluateExp(&fxExp, xm[n])}

	// Validate interval before iterating
	if fa == 0 {
		return a, nil, nil
	} else if fb == 0 {
		return b, nil, nil
	} else if fa*fb >= 0 {
		err := fmt.Sprintf("[%v, %v] is not a valid interval\n", a, b)
		return 0, nil, errors.New(err)
	}

	for E[n] > tol && n < niter {
		if fm[n] == 0 {
			return xm[n], nil, nil
		} else if fa*fm[n] > 0 {
			an, bn = append(an, xm[n]), append(bn, bn[n])
			fa = fm[n]
		} else {
			an, bn = append(an, an[n]), append(bn, xm[n])
		}
		n++
		xm = append(xm, (an[n]+bn[n])/2)
		fm = append(fm, evaluateExp(&fxExp, xm[n]))
		E = append(E, math.Abs(xm[n-1]-xm[n]))
	}
	if n == niter || !(E[n] < tol) {
		err := fmt.Sprint("method faild in ", niter, " iterations")
		return 0, nil, errors.New(err)
	}

	table := map[string]interface{}{
		"n":     n,
		"a":     an,
		"b":     bn,
		"xm":    xm,
		"fm":    fm,
		"error": E}

	return xm[n], table, nil
}

func FixedPoint(x0, tol float64, fx, gx string, niter int) (float64, map[string]interface{}, error) {
	var fn, xn, E []float64
	// Generate expressions for f(x) and g(x)
	x, c := x0, 0
	fxExp, err := newExpression(fx)
	if err != nil {
		return 0, nil, err
	}
	gxExp, err := newExpression(gx)
	if err != nil {
		return 0, nil, err
	}
	defer fxExp.Delete()
	defer gxExp.Delete()

	// Evaluate f(x)
	xn = append(xn, x)
	fn = append(fn, evaluateExp(&fxExp, x))
	E = append(E, 100)

	for E[c] > tol && fn[c] != 0 && c < niter {
		x = evaluateExp(&gxExp, x)
		fn = append(fn, evaluateExp(&fxExp, x))
		xn = append(xn, x)
		c++
		E = append(E, math.Abs(xn[c]-xn[c-1]))
	}
	if fn[c] == 0 {
		return x, nil, nil
	} else if E[len(E)-1] < tol {
		table := map[string]interface{}{
			"n":     c,
			"xn":    xn,
			"fn":    fn,
			"error": E,
		}
		return x, table, nil
	} else {
		err := fmt.Sprint("Fracaso en", niter, "iteraciones")
		return 0, nil, errors.New(err)
	}
}

func FalsePosition(a, b, tol float64, fx string, niter int) (float64, map[string]interface{}, error) {
	fxExp, err := newExpression(fx)
	if err != nil {
		return 0, nil, err
	}

	var an, bn, xm, fm, E []float64
	an, bn = append(an, a), append(bn, b)
	n := 0
	fa, fb := evaluateExp(&fxExp, a), evaluateExp(&fxExp, b)

	if fa == 0 {
		return a, nil, nil
	} else if fb == 0 {
		return b, nil, nil
	} else if fa*fb >= 0 {
		err := fmt.Sprintf("[%v, %v] is not a valid interval\n", a, b)
		return 0, nil, errors.New(err)
	}

	for n < niter {
		xm = append(xm, bn[n]-fb*(bn[n]-an[n])/(fb-fa))
		fm = append(fm, xm[n])
		if fm[n] == 0 {
			return xm[n], nil, nil
		}
		E = append(E, math.Abs(xm[n]-bn[n]))
		if E[n] <= tol {
			table := map[string]interface{}{
				"n":     n,
				"a":     an,
				"xm":    xm,
				"b":     bn,
				"f(xm)": fm,
				"error": E,
			}
			return xm[n], table, nil
		}
		n++
		if fm[n-1]*fb < 0 {
			an = append(an, bn[n-1])
			fa = fb
		} else {
			an = append(an, an[n-1])
		}
		bn = append(bn, xm[n-1])
		fb = fm[n-1]
	}
	return 0, nil, errors.New(fmt.Sprint("failed after ", niter, " iterations\n"))
}

func Newton(x0, tol float64, fx string, niter int) (float64, map[string]interface{}, error) {
	var xn, fn, E []float64

	fxExp, err := newExpression(fx)
	if err != nil {
		return 0, nil, err
	}
	f := func(x float64) float64 {
		return evaluateExp(&fxExp, x)
	}
	fdx := func(x float64) float64 {
		return clc.Diff(f, x)
	}

	n := 0
	xn = append(xn, x0)
	fn = append(fn, f(xn[n]))
	E = append(E, 100)

	if fn[n] == 0 {
		return x0, nil, nil
	}

	for n < niter {
		x := xn[n] - f(xn[n])/fdx(xn[n])
		e := math.Abs(x - xn[n])
		E = append(E, e)
		xn = append(xn, x)
		fn = append(fn, f(x))
		n++
		if e < tol {
			table := map[string]interface{}{
				"n":     n,
				"xn":    xn,
				"fn":    fn,
				"error": E,
			}
			return x, table, nil
		}
	}

	return 0, nil, errors.New(fmt.Sprint("method failed in ", niter, " iterations"))
}
