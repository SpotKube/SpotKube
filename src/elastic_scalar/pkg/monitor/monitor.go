package monitor

import (
	"github.com/SpotKube/SpotKube/src/elastic_scalar/pkg/optimizer"
	"github.com/robfig/cron/v3"
	log "github.com/sirupsen/logrus"
)

func Watch() {
	log.Info("Starting the monitor")
	c := cron.New()
	c.AddFunc("5 * * * *", monitor)
	go c.Start()
}

func monitor() {
	optimizer.Run()
}
