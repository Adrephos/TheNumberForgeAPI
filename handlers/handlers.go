package handlers

import "github.com/gin-gonic/gin"

func Response(c *gin.Context, success bool, data interface{}, err error, status int) {
	if success {
		c.JSON(status, gin.H{
			"success": success,
			"data":    data,
		})
		return
	}
	c.JSON(status, gin.H{
		"success": success,
		"error":    err.Error(),
	})
}
