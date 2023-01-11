package v1controllers

import (
	"encoding/json"
	"io"

	u "github.com/SpotKube/SpotKube/apiServer/pkg/helpers"
	v1s "github.com/SpotKube/SpotKube/apiServer/pkg/services/api/v1"

	"github.com/gin-gonic/gin"
)

type MetricBody struct {
	File string `json:"file"`
}

// metricPredictor function will give you the predicted metrices
func MetricPredictor(c *gin.Context) {
	var metricService v1s.MetricPredictorService
	var metricBody MetricBody

	//decode the request body into struct and failed if any error occur

	err := json.NewDecoder(c.Request.Body).Decode(&metricBody)

	if err == nil || err == io.EOF {
		//call service
		resp := metricService.Predict(metricBody.File)

		//return response using api helper
		u.Respond(c.Writer, resp)

	} else if err != nil {
		u.Respond(c.Writer, u.Message(1, "Invalid request"))
		return
	}

}
