package monitor

import (
	log "github.com/sirupsen/logrus"

	"github.com/robfig/cron/v3"
)

func Watch() {
	log.Info("Starting the monitor")
	c := cron.New()
	c.AddFunc("* * * * *", monitor)
	go c.Start()
}

func monitor() {
	// nodesCpuUsage := kube.GetNodeCpuUsage()

}
