package metricPredictor

import (
	u "github.com/SpotKube/SpotKube/apiServer/pkg/helpers"
	res "github.com/SpotKube/SpotKube/apiServer/pkg/helpers/api/v1"
)

type cpuPredictor struct {
	rps string `json:"rps"`
	cpu string `json:"cpu"`
}

type memoryPredictor struct {
	rps    string `json:"rps"`
	memory string `json:"memory"`
}

type metricPredictorService struct {
	cpuPredictor    cpuPredictor
	memoryPredictor memoryPredictor
}

func (mps *metricPredictorService) predictCpu(filepath string) map[string]interface{} {
	// read csv and do the prediction

}

func (mps *metricPredictorService) predictMemory(filepath string) map[string]interface{} {
	// read csv and predict

}

func (mps *metricPredictorService) predict(filepath string) map[string]interface{} {
	mps.predictCpu(filepath)
	mps.predictMemory(filepath)

	metricData := res.PredictorResponse{
		rps:    mps.cpuPredictor.rps,
		cpu:    mps.cpuPredictor.cpu,
		memory: mps.memoryPredictor.memory,
	}
	response := u.Message(0, "Metrics predicted succssfully")
	response["data"] = metricData
	return response

}
