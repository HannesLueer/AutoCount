package main

import (
	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
	"github.com/rs/cors"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"server/src/handlers/counter"
	"server/src/helper/auth"
)

func main() {
	// load .env files
	err := godotenv.Load(
		filepath.Join("config", "db.env"),
		filepath.Join("config", "server.env"),
	)
	if err != nil {
		log.Fatal(err)
	}

	// define routes
	r := mux.NewRouter()
	apiRouter := r.PathPrefix("/api/v1").Subrouter()
	counterRouter := apiRouter.PathPrefix("/c").Subrouter()
	counterRouter.HandleFunc("/{id}", counter.GetHandler).Methods(http.MethodGet)
	counterRouter.HandleFunc("/{id}", auth.IsAuthorized(counter.SetHandler)).Methods(http.MethodPut)

	// CORS
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"*://localhost:3000"},
		AllowCredentials: true,
		Debug:            false,
		AllowedHeaders:   []string{"*"},
		AllowedMethods:   []string{http.MethodGet, http.MethodPut, http.MethodDelete, http.MethodPost},
	})
	corsMux := c.Handler(r)

	// serve
	log.Fatalln(http.ListenAndServe(":"+os.Getenv("SERVER_PORT"), corsMux))
}
