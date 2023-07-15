package auth

import (
	"net/http"
)

func IsAuthorized(handler http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		username, password, ok := r.BasicAuth()
		if !ok {
			http.Error(w, "Error parsing basic auth", http.StatusUnauthorized)
			return
		}

		if isAuthorized(username, password) {
			r.Header.Set("user", username)
			handler.ServeHTTP(w, r)
			return
		}
		http.Error(w, "Not authorized", http.StatusUnauthorized)
	}
}

func isAuthorized(username string, password string) bool {
	//TODO: implement
	return true
}
