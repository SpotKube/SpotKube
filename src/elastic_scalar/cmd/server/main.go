package main

import (
	"github.com/SpotKube/SpotKube/src/elastic_scalar/internal/monitor"
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	router := gin.Default()

	monitor.Watch()

	// Define a GET endpoint at /health
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "Hello, World!"})
	})

	router.Run(":8080")
}
