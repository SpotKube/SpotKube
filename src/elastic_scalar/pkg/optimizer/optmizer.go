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
	cpuUsageOfDSInOtherNs := 0.0

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
			dsSvcs := kube.GetDaemonSetSvc(v)

			// Search whether the pod is daemonset or not
			for _, podCpuUsage := range podsCpuUsage {
				var dsName string
				var isDaemonSet bool
				for dsK, dsV := range dsSvcs {
					dsName = dsK
					for _, pod := range dsV.Pods {
						if pod == podCpuUsage.PodName {
							isDaemonSet = true
							break
						}
					}
					if isDaemonSet {
						break
					}
				}

				if !isDaemonSet {
					cpuUsageOfPodsInOtherNs += podCpuUsage.CpuUsage
				} else {
					if !dsSvcs[dsName].IsUsed {
						// Here we are considering only the first daemonset's cpu usage, need to change this to consider all daemonsets and find the max cpu usage
						cpuUsageOfDSInOtherNs += podCpuUsage.CpuUsage
						dsTemp := dsSvcs[dsName]
						dsTemp.IsUsed = true
						dsSvcs[dsName] = dsTemp
					}
				}

			}
		}
	}

	log.Info("Total CPU usage: ", totalCpuUsage)
	log.Info("Number of pods: ", numOfPods)
	log.Info("Services: ", services)
	log.Info("CPU usage of pods in other namespaces: ", cpuUsageOfPodsInOtherNs)
	log.Info("CPU usage of daemonsets in other namespaces: ", cpuUsageOfDSInOtherNs)

	return CalcUsage{
		TotalCpu:                totalCpuUsage,
		NumOfPods:               numOfPods,
		Services:                services,
		CpuUsageOfpodsInOtherNs: cpuUsageOfPodsInOtherNs,
		CpuUsageOfDSInOtherNs:   cpuUsageOfDSInOtherNs,
	}
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
	namespaces["monitoring"] = "monitoring"
	namespaces["kube-flannel"] = "kube-flannel"

	totalCpuUsage := calculateTotalCpuUsage(namespaces)
	totalCpuCapacity := calculateTotalCpuCapacity()
	if totalCpuUsage.TotalCpu > 0.3*totalCpuCapacity {
		log.Warn("Total CPU usage is greater than total CPU capacity")
		// Invoke optimization engine to scale up
		log.Info("Invoking optimization engine")
		api.InvokeOptimizationEngine(totalCpuUsage.Services, totalCpuUsage.CpuUsageOfpodsInOtherNs, totalCpuUsage.CpuUsageOfDSInOtherNs)
	} else if totalCpuUsage.TotalCpu < 0.1*totalCpuCapacity {
		log.Warn("Total CPU usage is less than 50% of total CPU capacity")
		// Invoke optimization engine to scale down
		// log.Info("Invoking optimization engine")
		// api.InvokeOptimizationEngine(totalCpuUsage.Services, totalCpuUsage.CpuUsageOfpodsInOtherNs, totalCpuUsage.CpuUsageOfDSInOtherNs)
	} else {
		log.Info("Total CPU usage is less than total CPU capacity")
	}
}
