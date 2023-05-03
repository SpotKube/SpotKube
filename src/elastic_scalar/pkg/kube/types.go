package kube

type nodeCpuUsage struct {
	nodeName string
	cpuUsage float64
	totalCpu float64
}

type podCpuUsage struct {
	podName  string
	cpuUsage float64
	totalCpu float64
}
