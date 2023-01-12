package v1resources

type PodCalculatorResponse struct {
	Service string `json:"service"`
	MaxPod  int    `json:"maxPod"`
	MinPod  int    `json:"minPod"`
}
