package auth

import (
	"crypto/sha256"
	"fmt"
	"net/http"
	"server/src/database"
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
	passwordHash := fmt.Sprintf("%x", sha256.Sum256([]byte(password)))
	isAuth, err := database.HasUserWithPasswordHash(username, passwordHash)
	return isAuth && err == nil
}
