# ETL Micro SaaS - CSV Data Pipeline

## Overview

**ETL Micro SaaS** is a lightweight and scalable service designed to extract, transform, and load data from CSV files. The system combines the strengths of Python (for data manipulation and API management) and Go (for high-performance data processing), allowing it to handle complex ETL tasks efficiently. This microservice-based application is ideal for small- to medium-sized businesses that need reliable and fast data pipelines.

## Key Features

- **Extract**: Reads data from CSV files.
- **Transform**: Cleans, filters, and processes data using a combination of Python and Go, leveraging Go for high-performance data tasks.
- **Load**: Saves the transformed data into a new CSV file, database, or external system.
- **API-Driven**: Interact with the ETL pipeline via a high-performance FastAPI backend, with Go handling CPU-intensive operations.
- **Scalable and Containerized**: Fully containerized using Docker and deployable on Kubernetes for large-scale workloads.

## Technology Stack

- **Backend**: Python (FastAPI, Pandas) for API and basic transformations.
- **High-Performance Processing**: Go (for fast, efficient data processing).
- **DevOps**: Docker, Kubernetes, Jenkins (for CI/CD), Prometheus, Grafana (for monitoring).

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python 3.9+**
- **Go 1.18+**
- **Docker**
- **Docker Compose**
- **PostgreSQL** (optional, if using a database for loading data)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/etl-micro-saas.git
   cd etl-micro-saas
   ```

2. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Build and run the Docker containers:

   ```bash
   docker-compose up --build
   ```

### API Usage

1. **Upload CSV for processing**:

   - **Endpoint**: `/upload`
   - **Method**: `POST`
   - **Body**: Multipart form-data, with `file` containing the CSV file.

   Example:

   ```bash
   curl -F 'file=@yourfile.csv' http://localhost:8000/upload
   ```

2. **Process Data with Go**:

   - When high-performance processing is needed, Go functions are used to handle large datasets or CPU-bound transformations.
   - The API automatically decides when to offload processing tasks to Go based on data size and type.

3. **Process and download transformed CSV**:

   The processed file will be saved and available for download via the same API endpoint after transformation.

### Configuration

The application is configurable through environment variables:

- `DATA_STORAGE_PATH`: Directory path for saving uploaded and processed CSV files.
- `DATABASE_URL`: URL for connecting to a database, if applicable.

### Example ETL Flow

1. **Upload CSV**: Users upload a CSV file via the `/upload` endpoint.
2. **Transform**: Python handles smaller, lightweight transformations, while Go processes large datasets and performs CPU-heavy transformations.
3. **Load**: Processed data is saved back into a new CSV file, or loaded into a database for further analysis.

### Go Integration for High-Performance Processing

Some key data processing tasks, such as sorting large datasets or performing complex calculations, will be handled by Go to ensure optimal performance. The FastAPI service delegates these operations to Go via gRPC or REST when necessary.

#### Example Go Code for Processing:

```go
package main

import (
    "encoding/csv"
    "os"
    "log"
)

func processCSV(file string) {
    f, err := os.Open(file)
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()

    reader := csv.NewReader(f)
    records, err := reader.ReadAll()
    if err != nil {
        log.Fatal(err)
    }

    // Process data here, e.g., sort or filter
}

func main() {
    processCSV("input.csv")
}
```

### Deployment

The service is containerized using Docker and can be deployed to any cloud or local infrastructure.

### Kubernetes Deployment

To deploy to Kubernetes, use the provided Helm chart or apply the Kubernetes YAML configuration files:

```bash
kubectl apply -f k8s/
```

### Monitoring & Logging

The application comes with integrated monitoring using **Prometheus** and **Grafana** to track key metrics. **ELK Stack** or **Loki** can be used for log aggregation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
