package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

// Структура записи, соответствующая вашим данным
type Record struct {
	Hotel                       string  `json:"hotel"`
	IsCanceled                  int     `json:"is_canceled"`
	LeadTime                    int     `json:"lead_time"`
	ArrivalDateYear             int     `json:"arrival_date_year"`
	ArrivalDateMonth            string  `json:"arrival_date_month"`
	ArrivalDateWeekNumber       int     `json:"arrival_date_week_number"`
	ArrivalDateDayOfMonth       int     `json:"arrival_date_day_of_month"`
	StaysInWeekendNights        int     `json:"stays_in_weekend_nights"`
	StaysInWeekNights           int     `json:"stays_in_week_nights"`
	Adults                      int     `json:"adults"`
	Children                    float64 `json:"children"`
	Babies                      int     `json:"babies"`
	Meal                        string  `json:"meal"`
	Country                     string  `json:"country"`
	MarketSegment               string  `json:"market_segment"`
	DistributionChannel         string  `json:"distribution_channel"`
	IsRepeatedGuest             int     `json:"is_repeated_guest"`
	PreviousCancellations       int     `json:"previous_cancellations"`
	PreviousBookingsNotCanceled int     `json:"previous_bookings_not_canceled"`
	ReservedRoomType            string  `json:"reserved_room_type"`
	AssignedRoomType            string  `json:"assigned_room_type"`
	BookingChanges              int     `json:"booking_changes"`
	DepositType                 string  `json:"deposit_type"`
	Agent                       float64 `json:"agent"`
	Company                     float64 `json:"company"`
	DaysInWaitingList           int     `json:"days_in_waiting_list"`
	CustomerType                string  `json:"customer_type"`
	Adr                         float64 `json:"adr"`
	RequiredCarParkingSpaces    int     `json:"required_car_parking_spaces"`
	TotalOfSpecialRequests      int     `json:"total_of_special_requests"`
	ReservationStatus           string  `json:"reservation_status"`
	ReservationStatusDate       string  `json:"reservation_status_date"`
}

func processData(w http.ResponseWriter, r *http.Request) {
	// Чтение данных из тела запроса
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Cannot read request body", http.StatusBadRequest)
		return
	}

	// Парсинг данных из JSON
	var records []Record
	err = json.Unmarshal(body, &records)
	if err != nil {
		http.Error(w, "Cannot parse JSON", http.StatusBadRequest)
		return
	}

	// Здесь можно выполнить обработку данных, если это необходимо
	for i, record := range records {
		// Пример обработки: увеличим lead_time на 1
		records[i].LeadTime = record.LeadTime + 1
		// Добавьте другие операции по обработке данных, если необходимо
	}

	// Отправка успешного ответа обратно
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Data processed successfully!"))
}

func main() {
	http.HandleFunc("/process", processData)
	fmt.Println("Starting server at port 8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
}
