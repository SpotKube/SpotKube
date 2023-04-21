package kube

import (
	"context"
	"fmt"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

type nodeCpuUsage struct {
	nodeName string
	cpuUsage float64
	totalCps float64
}

func GetNodeCpuUsage() []nodeCpuUsage {
	nodes := GetNodes()
	nodesCpuUsage := make([]nodeCpuUsage, len(nodes.Items))

	for i, node := range nodes.Items {
		nodeMetrics, err := metricsClientset.MetricsV1beta1().NodeMetricses().Get(context.Background(), node.ObjectMeta.Name, metav1.GetOptions{})
		if err != nil {
			panic(err.Error())
		}
		cpuUsage := nodeMetrics.Usage.Cpu()
		fmt.Printf("Node %s CPU usage: %f\n", node.ObjectMeta.Name, cpuUsage.AsDec())
		totalCpu := node.Status.Capacity.Cpu()
		cpuUsagePercent := float64(cpuUsage.MilliValue()) / float64(totalCpu.MilliValue()) * 100
		fmt.Printf("Node %s CPU percentage: %f\n", node.ObjectMeta.Name, cpuUsagePercent)
		nodesCpuUsage[i] = nodeCpuUsage{
			nodeName: node.ObjectMeta.Name,
			cpuUsage: float64(cpuUsage.MilliValue()),
			totalCps: float64(totalCpu.MilliValue()),
		}
	}
	return nodesCpuUsage
}
