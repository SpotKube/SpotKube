package api

import (
	"encoding/json"

	log "github.com/sirupsen/logrus"
)

func convertToJson(services map[string]int, cpuUsageOfPodsInOtherNs float64) []byte {
	svc := make([]SvcDetails, 0)
	for k, v := range services {
		svc = append(svc, SvcDetails{Name: k, Pods: v})
	}
	reqBody := ReqBodySvc{Services: svc, CpuUsageOfPodsInOtherNS: cpuUsageOfPodsInOtherNs}
	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		log.Error("Error marshalling services: ", err)
	}
	return jsonData
}
