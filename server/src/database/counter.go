package database

import (
	"database/sql"
	"errors"
	"fmt"
	"server/src/models"
)

func GetCounter(siteId string) (counter models.CounterOut, err error) {
	row := DBRepo.db.QueryRow("SELECT site_id, current_cars, max_cars, display_name FROM counter WHERE site_id = ?", siteId)
	err = row.Scan(&counter.ID, &counter.CurrentCars, &counter.MaxCars, &counter.DisplayName)
	if err != nil && errors.Is(err, sql.ErrNoRows) {
		return counter, fmt.Errorf("so such row")
	}
	return counter, err
}

func UpdateCounter(id string, updated models.CounterIn) error {
	res, err := DBRepo.db.Exec("UPDATE counter SET current_cars = ? WHERE site_id = ?", updated.CurrentCars, id)
	if err != nil {
		return err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return err
	}
	if rowsAffected == 0 {
		return fmt.Errorf("0 Rows affected")
	}

	return nil
}
