package routes_v1

import (
	handlers_v1 "github.com/Adrephos/TheNumberForgeAPI/handlers/v1"
	"github.com/gin-gonic/gin"
)

func NonlinearEquations(router *gin.Engine) {
	v1 := router.Group("/v1")
	{
		v1.POST("/nonlinear/bisection", handlers_v1.Bisection)
		v1.POST("/nonlinear/fixed_point", handlers_v1.FixedPoint)
		v1.POST("/nonlinear/false_position", handlers_v1.FalsePosition)
	}
}
