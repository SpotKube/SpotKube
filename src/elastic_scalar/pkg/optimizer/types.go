package optimizer

type CalcUsage struct {
	TotalCpu  float64
	NumOfPods int
	Services  map[string]int
}

type SvcDetails struct {
	Name string `json:"name"`
	Pods int    `json:"pods"`
}
