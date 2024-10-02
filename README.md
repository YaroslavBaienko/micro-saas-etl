# ETL Micro SaaS - CSV Data Pipeline

## Overview

**ETL Micro SaaS** is a lightweight and scalable service designed to extract, transform, and load data from CSV files. The system combines the strengths of Python (for data manipulation and API management) and Go (for high-performance data processing), allowing it to handle complex ETL tasks efficiently. This microservice-based application is ideal for small to medium-sized businesses that need reliable and fast data pipelines.

## Key Features

- **Extract**: Reads data from CSV files.
- **Transform**: Cleans, filters, and processes data using a combination of Python and Go, leveraging Go for high-performance data tasks.
- **Load**: Saves the transformed data into a new CSV file or loads it into a MySQL database.
- **API-Driven**: Interact with the ETL pipeline via a high-performance FastAPI backend, with Go handling CPU-intensive operations.
- **Scalable and Containerized**: Fully containerized using Docker and deployable on Kubernetes for large-scale workloads.

## Technology Stack

- **Backend**: Python (FastAPI, Pandas) for API and basic transformations.
- **High-Performance Processing**: Go (for fast, efficient data processing).
- **Database**: MySQL (for data storage).
- **DevOps**: Docker, Kubernetes, Jenkins (for CI/CD), Prometheus, Grafana (for monitoring).

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Docker**
- **Docker Compose**

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/YaroslavBaienko/micro-saas-etl.git
   cd micro-saas-etl
   ```

2. **Build and run the Docker containers**:

   ```bash
   docker-compose up --build
   ```

## API Usage

### Upload CSV for processing:

- **Endpoint**: `/upload`
- **Method**: POST
- **Body**: Multipart form-data, with file containing the CSV file.
- **Example**:

  ```bash
   curl -F 'file=@hotel_bookings.csv' http://localhost:8000/upload
  ```

### Process Data with Go:

High-performance processing tasks are delegated to the Go service. The API automatically decides when to offload processing tasks to Go based on data size and complexity.

### Process and download transformed CSV:

The processed file will be saved and available for download via the API after transformation.

## Configuration

The application is configurable through environment variables set in the `docker-compose.yml` file or passed to the Docker containers:

### MySQL Configuration:

- `MYSQL_USER`: MySQL database username (default: etl_user).
- `MYSQL_PASSWORD`: MySQL database password (default: etl_password).
- `MYSQL_DATABASE`: MySQL database name (default: etl_database).
- `MYSQL_ROOT_PASSWORD`: MySQL root password (default: rootpassword).

## Project Structure

```
micro-saas-etl/
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── go_service/
│   ├── main.go
│   ├── go.mod
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Go Integration for High-Performance Processing

Key data processing tasks, such as sorting large datasets or performing complex calculations, are handled by the Go service to ensure optimal performance. The FastAPI service delegates these operations to the Go service via HTTP requests when necessary.

### Example Go Code for Processing:

```go
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

```

## Deployment

The service is containerized using Docker and can be deployed to any cloud or local infrastructure.

### Kubernetes Deployment:

To deploy to Kubernetes, use the provided Kubernetes YAML configuration files:

```bash
kubectl apply -f k8s/
```

## Monitoring & Logging

- The application comes with integrated monitoring using Prometheus and Grafana to track key metrics.
- ELK Stack or Loki can be used for log aggregation.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Additional Information

- Python Version: 3.9
- Go Version: 1.18
- MySQL Version: Latest (specified in docker-compose.yml)

## Troubleshooting

### Common Issues:

- If the app container exits with an error related to python-multipart, ensure that python-multipart is included in requirements.txt.
- Verify that the correct Python version is used (python:3.9-slim in the Dockerfile) to maintain compatibility with FastAPI.

### Logs:

Check container logs using:

```bash
docker-compose logs app
docker-compose logs go_service
docker-compose logs db
```

### Database Access:

To access the MySQL database inside the container and see sctructure:

```bash
docker exec -it etl_db mysql -u etl_user -p
# Enter password: etl_password

mysql> USE etl_database;
mysql> SHOW TABLES;
DESCRIBE data_table;
```

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any inquiries or issues, please open an issue on the GitHub repository or contact the maintainer at zerhug@gmail.com @YaroslavBaienko.
