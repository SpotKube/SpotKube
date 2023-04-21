package main

import (
	"net/http"

	"github.com/SpotKube/SpotKube/src/elastic_scalar/pkg/monitor"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	monitor.Watch()
	// monitor.Kube()
	// Define a GET endpoint at /health
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "Hello, World!"})
	})

	router.Run(":8080")
}
