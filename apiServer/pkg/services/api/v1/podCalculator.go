package v1services

import (
	"math"

	u "github.com/SpotKube/SpotKube/apiServer/pkg/helpers"
	res "github.com/SpotKube/SpotKube/apiServer/pkg/helpers/api/v1"
)

type MaxUsage struct {
	Rps  string `json:"rps"`
	Pods int    `json:"pods"`
}

type MinUsage struct {
	Rps  string `json:"rps"`
	Pods int    `json:"pods"`
}

type PodCalculatorService struct {
	maxUsage MaxUsage
	minUsage MinUsage
}

func (pcs *PodCalculatorService) calculatePodCount(C int, M int, Pc int, Pm int, flag string) {
	var podCount int
	cpuCount := float64(C) / float64(Pc)
	memoryCount := float64(M) / float64(Pm)
	podCount = int(math.Round(math.Max(cpuCount, memoryCount)))

	if podCount == 0 {
		podCount = 1
	}

	if flag == "max" {
		pcs.maxUsage.Pods = podCount
	} else {
		pcs.minUsage.Pods = podCount
	}
}

func (pcs *PodCalculatorService) CalculatePods() map[string]interface{} {
	// read the config.yml and read the related values C, M, Pc, Pm

	// services := {
	// 	Name: "service1",
	// 	MaxRPS: {
	// 		rps:    10000,
	// 		cpu:    1000,
	// 		memory: 500,
	// 	},
	// 	MinRPS: {
	// 		rps:    100,
	// 		cpu:    10,
	// 		memory: 20,
	// 	},
	// }
	Pc := 100
	Pm := 200
	maxCpu := 1000
	maxMemory := 500
	minCpu := 10
	minMemory := 20

	pcs.calculatePodCount(maxCpu, maxMemory, Pc, Pm, "max")
	pcs.calculatePodCount(minCpu, minMemory, Pc, Pm, "min")

	podData := res.PodCalculatorResponse{
		Service: "service1",
		MaxPod:  pcs.maxUsage.Pods,
		MinPod:  pcs.minUsage.Pods,
	}
	response := u.Message(0, "Pod count calculated succssfully")
	response["data"] = podData
	return response
}
