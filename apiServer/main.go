package main

import (
	"context"
	"fmt"
	"net/http"

	"github.com/vardius/go-api-boilerplate/cmd/auth/internal/application/config"
	authhttp "github.com/vardius/go-api-boilerplate/cmd/auth/internal/interfaces/http"
	"github.com/vardius/go-api-boilerplate/pkg/application"
	httputils "github.com/vardius/go-api-boilerplate/pkg/http"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	cfg := config.FromEnv()
	fmt.Println("CONFIG:", cfg)

	router := authhttp.NewRouter(
		cfg,
	)

	app := application.New()
	app.AddAdapters(
		httputils.NewAdapter(
			&http.Server{
				Addr:         fmt.Sprintf("%s:%d", cfg.HTTP.Host, cfg.HTTP.Port),
				ReadTimeout:  cfg.HTTP.ReadTimeout,
				WriteTimeout: cfg.HTTP.WriteTimeout,
				IdleTimeout:  cfg.HTTP.IdleTimeout, // limits server-side the amount of time a Keep-Alive connection will be kept idle before being reused
				Handler:      router,
			},
		),
	)

	if cfg.App.Environment == "development" {
		app.AddAdapters(
			application.NewDebugAdapter(
				fmt.Sprintf("%s:%d", cfg.Debug.Host, cfg.Debug.Port),
			),
		)
	}

	app.WithShutdownTimeout(cfg.App.ShutdownTimeout)
	app.Run(ctx)
}
