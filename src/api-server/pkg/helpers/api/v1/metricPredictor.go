package v1resources

type PredictorResponse struct {
	Rps    string `json:"rps"`
	Cpu    string `json:"cpu"`
	Memory string `json:"memory"`
}
