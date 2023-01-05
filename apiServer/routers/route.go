package routers

// NewRouter provides new router
func NewRouter() http.Handler {

	// Global middleware
	router := gorouter.New(
	)
	router.NotFound(json.NotFound())
	router.NotAllowed(json.NotAllowed())

	router.GET("/", handlers.BuildListUserHandler(repository))


	return router