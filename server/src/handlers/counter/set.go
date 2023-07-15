package counter

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"net/http"
	"server/src/models"
)

func SetHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	if user := r.Header.Get("user"); user != id {
		http.Error(w, "unauthorized for this counter", http.StatusUnauthorized)
		return
	}

	var counter models.CounterIn
	err := json.NewDecoder(r.Body).Decode(&counter)
	if err != nil {
		http.Error(w, "error in reading body", http.StatusBadRequest)
		return
	}

	err = setCounter(id, counter)
	if err != nil {
		http.Error(w, "error in setting counter", http.StatusInternalServerError)
		return
	}

	return
}

func setCounter(id string, counter models.CounterIn) (err error) {
	//TODO: implement
	return nil
}
