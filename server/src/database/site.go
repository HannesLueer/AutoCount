package database

import (
	"database/sql"
	"errors"
	"fmt"
)

func HasUserWithPasswordHash(siteId string, passwordHash string) (has bool, err error) {
	var returnId string
	row := DBRepo.db.QueryRow("SELECT id FROM sites WHERE id = ? and password_hash = ?", siteId, passwordHash)
	err = row.Scan(&returnId)
	if err != nil && errors.Is(err, sql.ErrNoRows) {
		return false, fmt.Errorf("so such row")
	}
	return siteId == returnId, err
}
