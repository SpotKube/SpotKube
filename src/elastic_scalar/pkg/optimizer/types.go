package optimizer

type CalcUsage struct {
	TotalCpu                float64
	NumOfPods               int
	Services                map[string]int
	CpuUsageOfpodsInOtherNs float64
	CpuUsageOfDSInOtherNs   float64
}
