package monitor

import (
	"fmt"
	// "github.com/robfig/cron/v3"
	"github.com/SpotKube/SpotKube/src/elastic_scalar/pkg/kube"
)

func Watch() {
	fmt.Println("starting monitor")
	kube.GetNodeCpuUsage()
	// c := cron.New()
	// c.AddFunc("* * * * *", hello)
	// go c.Start()
}

// func hello() {
// 	fmt.Println("hello")
// }
