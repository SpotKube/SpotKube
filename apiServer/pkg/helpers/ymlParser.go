package helpers

type Rps struct {
	Rps    int    `yaml: "rps"`
	Cpu    string `yaml: "cpu"`
	Memory string `yaml: "memory"`
}
type Service struct {
	Name   string `yaml:"name"`
	MaxRps Rps    `yaml:"maxRps"`
	MinRps Rps    `yaml:"minRps"`
}
type Pods struct {
	MaxCpu    string `yaml:"maxCpu"`
	MaxMemory string `yaml:"maxMemory"`
}

type Resources struct {
	Pods Pods `yaml:"pods"`
}

type Config struct {
	Services  []Service `yaml:"services"`
	Resources Resources `yaml:"resources"`
}
