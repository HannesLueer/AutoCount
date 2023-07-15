package counter

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"net/http"
	"server/src/database"
	"server/src/models"
)

func GetHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	counter, err := getCounter(id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}

	jsonResp, err := json.Marshal(counter)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(jsonResp)
	return
}

func getCounter(id string) (counter models.CounterOut, err error) {
	return database.GetCounter(id)
}
