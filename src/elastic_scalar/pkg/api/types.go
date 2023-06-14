package api

type SvcDetails struct {
	Name string `json:"name"`
	Pods int    `json:"pods"`
}

type ReqBodySvc struct {
	Services                []SvcDetails `json:"services_list"`
	CpuUsageOfPodsInOtherNS float64      `json:"cpu_usage_of_pods_in_other_ns"`
	CpuUsageOfDSInOtherNS   float64      `json:"cpu_usage_of_ds_in_other_ns"`
}
