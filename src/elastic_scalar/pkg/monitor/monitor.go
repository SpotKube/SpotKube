package monitor

import (
	"fmt"

	"github.com/SpotKube/SpotKube/src/elastic_scalar/pkg/kube"
	"github.com/robfig/cron/v3"
)

func Watch() {
	fmt.Println("starting monitor")
	c := cron.New()
	c.AddFunc("* * * * *", monitor)
	go c.Start()
}

func monitor() {
	nodesCpuUsage := kube.GetNodeCpuUsage()

}
