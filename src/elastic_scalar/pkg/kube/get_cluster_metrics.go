package kube

import (
	"context"
	"fmt"

	log "github.com/sirupsen/logrus"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func GetNodeCpuUsage() []NodeCpuUsage {
	nodes := GetNodes()
	nodesCpuUsage := make([]NodeCpuUsage, len(nodes.Items))

	for i, node := range nodes.Items {
		nodeMetrics, err := metricsClientset.MetricsV1beta1().NodeMetricses().Get(context.Background(), node.ObjectMeta.Name, metav1.GetOptions{})
		if err != nil {
			// panic(err.Error())
			continue
		}
		cpuUsage := nodeMetrics.Usage.Cpu()
		totalCpu := node.Status.Capacity.Cpu()
		logMsg := fmt.Sprintf("Node %s CPU usage: %f and total CPU: %f\n", node.ObjectMeta.Name, float64(cpuUsage.MilliValue()), float64(totalCpu.MilliValue()))
		log.Info(logMsg)
		nodesCpuUsage[i] = NodeCpuUsage{
			NodeName: node.ObjectMeta.Name,
			CpuUsage: float64(cpuUsage.MilliValue()),
			TotalCpu: float64(totalCpu.MilliValue()),
		}
	}
	return nodesCpuUsage
}

func GetPodCpuUsage(namespace string) []PodCpuUsage {
	pods := GetPods(namespace)
	podsCpuUsage := make([]PodCpuUsage, len(pods.Items))
	for _, pod := range pods.Items {
		podMetrics, err := metricsClientset.MetricsV1beta1().PodMetricses(namespace).Get(context.Background(), pod.ObjectMeta.Name, metav1.GetOptions{})
		if err != nil {
			// panic(err.Error())
			continue
		}
		cpuUsage := podMetrics.Containers[0].Usage.Cpu()
		// Get the total CPU allocated to the pod
		totalCpu := pod.Spec.Containers[0].Resources.Requests.Cpu()
		logMsg := fmt.Sprintf("Pod %s  CPU usage: %f and total CPU allocation: %f\n", pod.ObjectMeta.Name, float64(cpuUsage.MilliValue()), float64(totalCpu.MilliValue()))
		log.Info(logMsg)
		podsCpuUsage = append(podsCpuUsage, PodCpuUsage{
			PodName:     pod.ObjectMeta.Name,
			CpuUsage:    float64(cpuUsage.MilliValue()),
			TotalCpu:    float64(totalCpu.MilliValue()),
			NodeName:    pod.Spec.NodeName,
			ServiceName: pod.ObjectMeta.Labels["app"],
		})
	}
	return podsCpuUsage
}

// Print namespace and service name of the given daemonset
func GetDaemonSetSvc(namespace string) map[string]DsDetails {
	dsList := GetDaemonSets(namespace)
	// Create map of daemonsets in the given namespace
	serviceMap := make(map[string]DsDetails)
	for _, ds := range dsList {
		pods := make([]string, 0)
		for _, pod := range PodsAssociateWithDS(namespace, &ds) {
			pods = append(pods, pod.Name)
		}
		serviceMap[ds.Name] = DsDetails{Pods: pods, IsUsed: false}
	}
	return serviceMap
}
