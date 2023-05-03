package kube

import (
	"context"
	"fmt"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func GetNodeCpuUsage() []nodeCpuUsage {
	nodes := GetNodes()
	nodesCpuUsage := make([]nodeCpuUsage, len(nodes.Items))

	for i, node := range nodes.Items {
		nodeMetrics, err := metricsClientset.MetricsV1beta1().NodeMetricses().Get(context.Background(), node.ObjectMeta.Name, metav1.GetOptions{})
		if err != nil {
			// panic(err.Error())
			continue
		}
		cpuUsage := nodeMetrics.Usage.Cpu()
		fmt.Printf("Node %s CPU usage: %f\n", node.ObjectMeta.Name, cpuUsage.AsDec())
		totalCpu := node.Status.Capacity.Cpu()
		fmt.Printf("Node %s total CPU: %f\n", node.ObjectMeta.Name, float64(totalCpu.MilliValue()))
		nodesCpuUsage[i] = nodeCpuUsage{
			nodeName: node.ObjectMeta.Name,
			cpuUsage: float64(cpuUsage.MilliValue()),
			totalCpu: float64(totalCpu.MilliValue()),
		}
	}
	return nodesCpuUsage
}

func GetPodCpuUsage() []podCpuUsage {
	pods := GetPods()
	podsCpuUsage := make([]podCpuUsage, len(pods.Items))
	for i, pod := range pods.Items {
		podMetrics, err := metricsClientset.MetricsV1beta1().PodMetricses(namespace).Get(context.Background(), pod.ObjectMeta.Name, metav1.GetOptions{})
		if err != nil {
			// panic(err.Error())
			continue
		}
		cpuUsage := podMetrics.Containers[0].Usage.Cpu()
		fmt.Printf("Pod %s CPU usage: %f\n", pod.ObjectMeta.Name, cpuUsage.AsDec())
		// Get the total CPU allocated to the pod
		totalCpu := pod.Spec.Containers[0].Resources.Requests.Cpu()
		fmt.Printf("Pod %s total CPU allocation: %f\n", pod.ObjectMeta.Name, float64(totalCpu.MilliValue()))
		podsCpuUsage[i] = podCpuUsage{
			podName:  pod.ObjectMeta.Name,
			cpuUsage: float64(cpuUsage.MilliValue()),
			totalCpu: float64(totalCpu.MilliValue()),
		}
	}
	return podsCpuUsage
}
