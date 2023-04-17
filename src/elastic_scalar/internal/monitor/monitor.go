package monitor

import (
	"fmt"
	"github.com/robfig/cron/v3"
)

func Watch() {
	fmt.Println("starting monitor")
	c := cron.New()
	c.AddFunc("* * * * *", hello)
	go c.Start()
}

func hello() {
	fmt.Println("hello")
}
