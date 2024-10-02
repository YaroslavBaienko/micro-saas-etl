// go_service/main.go

package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type Record struct {
	// Объявите поля, соответствующие вашему CSV
	LeadTime int `json:"lead_time"`
	// Добавьте другие поля, если необходимо
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
	for _, record := range records {
		// Пример обработки: увеличим lead_time на 1
		record.LeadTime += 1
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
