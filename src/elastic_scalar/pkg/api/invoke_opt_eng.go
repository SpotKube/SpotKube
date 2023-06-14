package api

import (
	"bytes"
	"io/ioutil"
	"net/http"

	log "github.com/sirupsen/logrus"
)

func InvokeOptimizationEngine(services map[string]int, cpuUsageOfPodsInOtherNS float64) {
	jsonData := convertToJson(services, cpuUsageOfPodsInOtherNS)
	// Make an HTTP GET request to the API endpoint
	response, err := http.Post("http://127.0.0.1:8000/update_aws_cloud", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Error("Error:", err)
		return
	}
	defer response.Body.Close()

	// Read the response body
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Error("Error:", err)
		return
	}
	log.Info("Response body: ", string(body))
}
