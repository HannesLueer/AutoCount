package database

import (
	"database/sql"
	"log"
)

var DBRepo *SQLiteRepository

type SQLiteRepository struct {
	db *sql.DB
}

func NewSQLiteRepository(db *sql.DB) *SQLiteRepository {
	return &SQLiteRepository{
		db: db,
	}
}

func ConnectDatabase(dbFilepath string) {
	db, err := sql.Open("sqlite3", dbFilepath)
	if err != nil {
		log.Fatal(err)
	}
	DBRepo = NewSQLiteRepository(db)
}
