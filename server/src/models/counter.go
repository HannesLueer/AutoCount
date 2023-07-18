package models

type CounterOut struct {
	ID          string `json:"id"`
	DisplayName string `json:"displayName"`
	CurrentCars int64  `json:"currentCars"`
	MaxCars     int64  `json:"maxCars"`
}

type CounterIn struct {
	CurrentCars int64 `json:"currentCars"`
}
