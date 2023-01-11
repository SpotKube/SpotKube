package helpers

import (
	"encoding/json"
	"net/http"
)

// ResponseData structure
type ResponseData struct {
	Data interface{} `json:"data"`
	Meta interface{} `json:"meta"`
}

// Message returns map data
func Message(errno int, message string) map[string]interface{} {
	return map[string]interface{}{"errno": errno, "message": message}
}

// Respond returns basic response structure
func Respond(w http.ResponseWriter, data map[string]interface{}) {
	w.Header().Add("Content-Type", "application/json")
	json.NewEncoder(w).Encode(data)
}
