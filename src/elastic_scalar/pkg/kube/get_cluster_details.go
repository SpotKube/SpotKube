package kube

import (
	"context"

	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func GetPods() *v1.PodList {
	pods, err := clientset.CoreV1().Pods("default").List(context.Background(), metav1.ListOptions{})
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
