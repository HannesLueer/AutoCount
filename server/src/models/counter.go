package models

type CounterOut struct {
	ID          string
	DisplayName string
	CurrentCars int64
	MaxCars     int64
}

type CounterIn struct {
	CurrentCars int64
}
