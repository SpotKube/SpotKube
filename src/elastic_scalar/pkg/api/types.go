package api

type SvcDetails struct {
	Name string `json:"name"`
	Pods int    `json:"pods"`
}

type ReqBodySvc struct {
	Services []SvcDetails `json:"services_list"`
}
