package optimizer

import (
	"github.com/SpotKube/SpotKube/src/elastic_scalar/pkg/api"
	"github.com/SpotKube/SpotKube/src/elastic_scalar/pkg/kube"
	log "github.com/sirupsen/logrus"
)

func calculateTotalCpuUsage(namespaces map[string]string) CalcUsage {
	var totalCpuUsage float64
	var numOfPods int
	services := make(map[string]int)
	cpuUsageOfPodsInOtherNs := 0.0

	for k, v := range namespaces {
		if k == "default" {
			podsCpuUsage := kube.GetPodCpuUsage(v)
			for _, podCpuUsage := range podsCpuUsage {
				if podCpuUsage.TotalCpu == 0.0 {
					log.Warn("Total CPU allocation is 0 for pod: ", podCpuUsage.PodName)
					totalCpuUsage += podCpuUsage.CpuUsage
					numOfPods++
					if podCpuUsage.ServiceName != "" {
						services[podCpuUsage.ServiceName]++ // Increment the number of pods for the service
					}

				} else {
					cpuUsageAsPercentage := podCpuUsage.CpuUsage / podCpuUsage.TotalCpu
					if cpuUsageAsPercentage > 0.6 {
						log.Warn("CPU usage is greater than 60% for pod: ", podCpuUsage.PodName)
						totalCpuUsage += 2 * podCpuUsage.TotalCpu
						numOfPods += 2
						if podCpuUsage.ServiceName != "" {
							services[podCpuUsage.ServiceName] += 2 // Increment the number of pods for the service
						}
					} else {
						totalCpuUsage += podCpuUsage.TotalCpu
						numOfPods++
						if podCpuUsage.ServiceName != "" {
							services[podCpuUsage.ServiceName]++ // Increment the number of pods for the service
						}
					}
				}
			}
		} else {
			podsCpuUsage := kube.GetPodCpuUsage(v)
			for _, podCpuUsage := range podsCpuUsage {
				cpuUsageOfPodsInOtherNs += podCpuUsage.CpuUsage
			}
		}
	}

	log.Info("Total CPU usage: ", totalCpuUsage)
	log.Info("Number of pods: ", numOfPods)
	log.Info("Services: ", services)
	log.Info("CPU usage of pods in other namespaces: ", cpuUsageOfPodsInOtherNs)

	return CalcUsage{TotalCpu: totalCpuUsage, NumOfPods: numOfPods, Services: services, CpuUsageOfpodsInOtherNs: cpuUsageOfPodsInOtherNs}
}

func calculateTotalCpuCapacity() float64 {
	var totalCpuCapacity float64
	nodes := kube.GetNodes()
	for _, node := range nodes.Items {
		totalCpuCapacity += float64(node.Status.Allocatable.Cpu().MilliValue())
	}
	log.Info("Total CPU capacity: ", totalCpuCapacity)
	return totalCpuCapacity
}

func Run() {
	namespaces := make(map[string]string)
	namespaces["default"] = "default"
	namespaces["kube-system"] = "kube-system"
	namespaces["monitoring"] = "kubernetes-dashboard"

	totalCpuUsage := calculateTotalCpuUsage(namespaces)
	totalCpuCapacity := calculateTotalCpuCapacity()
	if totalCpuUsage.TotalCpu > 0.8*totalCpuCapacity {
		log.Warn("Total CPU usage is greater than total CPU capacity")
		// Invoke optimization engine to scale up
		log.Info("Invoking optimization engine")
		api.InvokeOptimizationEngine(totalCpuUsage.Services, totalCpuUsage.CpuUsageOfpodsInOtherNs)
	} else if totalCpuUsage.TotalCpu < 0.5*totalCpuCapacity {
		log.Warn("Total CPU usage is less than 50% of total CPU capacity")
		// Invoke optimization engine to scale down
		log.Info("Invoking optimization engine")
		api.InvokeOptimizationEngine(totalCpuUsage.Services, totalCpuUsage.CpuUsageOfpodsInOtherNs)
	} else {
		log.Info("Total CPU usage is less than total CPU capacity")
	}
}
