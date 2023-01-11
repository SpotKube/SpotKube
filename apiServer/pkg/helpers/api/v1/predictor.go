package v1resources

type PredictorResponse struct {
	rps    string `json:"rps"`
	cpu    string `json:"cpu"`
	memory string `json:"memory"`
}
