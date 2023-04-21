package kube

import (
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/metrics/pkg/client/clientset/versioned"
)

var clientset *kubernetes.Clientset
var metricsClientset *versioned.Clientset

func init() {
	// Initialize the clientset
	rules := clientcmd.NewDefaultClientConfigLoadingRules()
	kubeconfig := clientcmd.NewNonInteractiveDeferredLoadingClientConfig(rules, &clientcmd.ConfigOverrides{})
	config, err := kubeconfig.ClientConfig()
	if err != nil {
		panic(err)
	}
	clientset = kubernetes.NewForConfigOrDie(config)

	// Initialize the clientset for metrics
	metricsClientset = versioned.NewForConfigOrDie(config)
}
