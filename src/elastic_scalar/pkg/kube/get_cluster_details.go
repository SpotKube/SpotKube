package kube

import (
	"context"

	appsv1 "k8s.io/api/apps/v1"
	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func GetPods(namespace string) *v1.PodList {
	pods, err := clientset.CoreV1().Pods(namespace).List(context.Background(), metav1.ListOptions{})
	if err != nil {
		panic(err)
	}

	// for _, pod := range pods.Items {
	// 	log.Println(pod.Name)
	// }
	return pods
}

func GetNodes() *v1.NodeList {
	nodeList, err := clientset.CoreV1().Nodes().List(context.Background(), metav1.ListOptions{})
	if err != nil {
		panic(err)
	}

	// for _, n := range nodeList.Items {
	// 	log.Println(n.Name)
	// }

	return nodeList
}

// List deamonsets in a namespace
func GetDaemonSets(namespace string) []appsv1.DaemonSet {
	daemonSets, err := clientset.AppsV1().DaemonSets(namespace).List(context.Background(), metav1.ListOptions{})
	if err != nil {
		panic(err)
	}

	return daemonSets.Items
}
