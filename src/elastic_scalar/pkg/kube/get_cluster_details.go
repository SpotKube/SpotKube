package kube

import (
	"context"
	"fmt"

	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func GetPods() *v1.PodList {
	pods, err := clientset.CoreV1().Pods("default").List(context.Background(), metav1.ListOptions{})
	if err != nil {
		panic(err)
	}

	for _, pod := range pods.Items {
		fmt.Println(pod.Name)
	}
	return pods
}

func GetNodes() *v1.NodeList {
	nodeList, err := clientset.CoreV1().Nodes().List(context.Background(), metav1.ListOptions{})
	if err != nil {
		panic(err)
	}
	for _, n := range nodeList.Items {
		fmt.Println(n.Name)
	}

	// newPod := &corev1.Pod{
	//   ObjectMeta: metav1.ObjectMeta{
	//     Name: "test-pod",
	//   },
	//   Spec: corev1.PodSpec{
	//     Containers: []corev1.Container{
	//       {Name: "busybox", Image: "busybox:latest", Command: []string{"sleep", "100000"}},
	//     },
	//   },
	// }

	// pod, err := clientset.CoreV1().Pods("default").Create(context.Background(), newPod, metav1.CreateOptions{})
	// if err != nil {
	//   panic(err)
	// }
	// fmt.Println(pod)
	return nodeList
}
