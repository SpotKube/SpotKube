package v1services

import (
	u "github.com/SpotKube/SpotKube/apiServer/pkg/helpers"
	res "github.com/SpotKube/SpotKube/apiServer/pkg/helpers/api/v1"
)

type cpuPredictor struct {
	Rps string `json:"rps"`
	Cpu string `json:"cpu"`
}

type memoryPredictor struct {
	Rps    string `json:"rps"`
	Memory string `json:"memory"`
}

type MetricPredictorService struct {
	cpuPredictor    cpuPredictor
	memoryPredictor memoryPredictor
}

func (mps *MetricPredictorService) predictCpu(filepath string) {
	// read csv and do the prediction

}

func (mps *MetricPredictorService) predictMemory(filepath string) {
	// read csv and predict

}

func (mps *MetricPredictorService) Predict(filepath string) map[string]interface{} {
	mps.predictCpu(filepath)
	mps.predictMemory(filepath)

	// update the user_config file. nned to implement a functionality for that

	// metricData := res.PredictorResponse{
	// 	Rps:    mps.cpuPredictor.Rps,
	// 	Cpu:    mps.cpuPredictor.Cpu,
	// 	Memory: mps.memoryPredictor.Memory,
	// }

	metricData := res.PredictorResponse{
		Rps:    "10000",
		Cpu:    "1000m", // 1000m = 1 core
		Memory: "500Mi", // 1 Mebibyte = 1.049 Megabyte
	}
	response := u.Message(0, "Metrics predicted succssfully")
	response["data"] = metricData
	return response

}
