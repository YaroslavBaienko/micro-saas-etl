// go_service/main.go

package main

import (
	"fmt"
	"net/http"
)

func processData(w http.ResponseWriter, r *http.Request) {
	// Здесь будет код для обработки данных
	fmt.Fprintf(w, "Data processed successfully!")
}

func main() {
	http.HandleFunc("/process", processData)
	fmt.Println("Starting server at port 8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
}
