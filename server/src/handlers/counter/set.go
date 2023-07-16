package counter

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"server/src/database"
	"server/src/models"
	"server/src/mqtt"
)

func SetHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	if user := r.Header.Get("user"); user != id {
		http.Error(w, "unauthorized for this counter", http.StatusUnauthorized)
		return
	}

	var counterIn models.CounterIn
	err := json.NewDecoder(r.Body).Decode(&counterIn)
	if err != nil {
		http.Error(w, "error in reading body", http.StatusBadRequest)
		return
	}

	err = setCounter(id, counterIn)
	if err != nil {
		http.Error(w, "error in setting counter", http.StatusInternalServerError)
		return
	}

	err = publishMqtt(id)
	if err != nil {
		log.Println(err)
	}

	return
}

func setCounter(id string, counter models.CounterIn) (err error) {
	return database.UpdateCounter(id, counter)
}

func publishMqtt(id string) (err error) {
	counterOut, err := database.GetCounter(id)
	if err != nil {
		return err
	}
	err = mqtt.Publish(id, counterOut)
	return err
}
