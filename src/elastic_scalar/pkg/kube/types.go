package kube

type NodeCpuUsage struct {
	NodeName string
	CpuUsage float64
	TotalCpu float64
}

type PodCpuUsage struct {
	PodName     string
	CpuUsage    float64
	TotalCpu    float64
	NodeName    string
	ServiceName string
}
