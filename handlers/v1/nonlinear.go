package handlers_v1

import (
	"net/http"

	"github.com/Adrephos/TheNumberForgeAPI/handlers"
	"github.com/Adrephos/TheNumberForgeAPI/services/nonlinear"
	"github.com/Adrephos/TheNumberForgeAPI/utils"
	"github.com/gin-gonic/gin"
)

func Bisection(c *gin.Context) {
	var b struct {
		A     string  `json:"a"`
		B     string  `json:"b"`
		Tol   float64 `json:"tol"`
		Fx    string  `json:"fx"`
		Niter int     `json:"niter"`
	}
	c.Bind(&b)

	p0, err := utils.EvalParameter(b.A)
	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	p1, err := utils.EvalParameter(b.B)
	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	root, table, err := nonlinear.Bisection(p0, p1, b.Tol, b.Fx, b.Niter)

	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	res := map[string]interface{}{"root": root}
	if table != nil {
		res["table"] = table
	}
	handlers.Response(c, true, res, nil, http.StatusOK)
}

func FixedPoint(c *gin.Context) {
	var b struct {
		X0    string  `json:"x0"`
		Tol   float64 `json:"tol"`
		Fx    string  `json:"fx"`
		Gx    string  `json:"gx"`
		Niter int     `json:"niter"`
	}
	c.Bind(&b)

	x0, err := utils.EvalParameter(b.X0)
	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	root, table, err := nonlinear.FixedPoint(x0, b.Tol, b.Fx, b.Gx, b.Niter)

	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	res := map[string]interface{}{"root": root}
	if table != nil {
		res["table"] = table
	}
	handlers.Response(c, true, res, nil, http.StatusOK)
}

func FalsePosition(c *gin.Context) {
	var b struct {
		A     string  `json:"a"`
		B     string  `json:"b"`
		Tol   float64 `json:"tol"`
		Fx    string  `json:"fx"`
		Niter int     `json:"niter"`
	}
	c.Bind(&b)

	p0, err := utils.EvalParameter(b.A)
	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	p1, err := utils.EvalParameter(b.B)
	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	root, table, err := nonlinear.FalsePosition(p0, p1, b.Tol, b.Fx, b.Niter)

	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	res := map[string]interface{}{"root": root}
	if table != nil {
		res["table"] = table
	}
	handlers.Response(c, true, res, nil, http.StatusOK)
}

func Newton(c *gin.Context) {
	var b struct {
		X0    string  `json:"x0"`
		Tol   float64 `json:"tol"`
		Fx    string  `json:"fx"`
		Niter int     `json:"niter"`
	}
	c.Bind(&b)

	x0, err := utils.EvalParameter(b.X0)
	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	root, table, err := nonlinear.Newton(x0, b.Tol, b.Fx, b.Niter)

	if err != nil {
		handlers.Response(c, false, nil, err, http.StatusInternalServerError)
		return
	}

	res := map[string]interface{}{"root": root}
	if table != nil {
		res["table"] = table
	}
	handlers.Response(c, true, res, nil, http.StatusOK)
}
