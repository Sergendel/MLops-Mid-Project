
# MLOps Project README



## 🚀 Project Overview

This project implements a robust and comprehensive Machine Learning Operations (MLOps) pipeline
 for a customer churn prediction model. 
It involves data extraction, transformation, and loading (ETL), batch and real-time prediction capabilities,
 and continuous monitoring with automated alerts to ensure reliability and accuracy.


---

## 🎯 Project Goals

* **ETL Processing:** Automate data loading, transformation, and verification using Apache Airflow.
* **Batch Predictions:** Run daily batch predictions using Airflow DAGs.
* **Real Time Predictions:** Serve model predictions via a RESTful API built using Flask.
* **Monitoring and Alerts:** Track data drift and model performance using Evidently AI.
---

## 🖼️ Architecture Diagram

Refer to the architecture diagram below for visual details about the data flow and component interaction:

![Architecture Diagram](./Architecture.bmp)

---

## 📦 Technological Stack

* **Containers & Orchestration:** Docker and Docker Compose
* **Orchestration:** Apache Airflow
* **API Framework:** Flask
* **Database:** PostgreSQL (simulated company DB)
* **Data Handling:** Pandas, SQLAlchemy
* **Model and Data Transformation:** scikit-learn
* **Monitoring::** Track data drift and model performance using Evidently AI.

---

## 📁 Project Structure

* `airflow/` - Airflow container with DAGs and ETL scripts
* `flask_api/` - Flask container for serving predictions
* `company_db_setup/` - simulates Compnay's database (PostgreSQL) and populates it using provided csv files.
* `shared_modules/` - Shared transform script of ETL and pretrained model (`churn_model.pickle`)
* `.env` - Environment variables for database credentials
* `config.yaml` - Project configuration paths
* `Architecture.bmp` - Project architecture visual representation

---

## ⚙️ Components

### Airflow (Batch Processing)

**Airflow Container:** Automates ETL tasks and batch predictions.

#### Key DAGs

* **\[MUST RUN] Load and Verify CSV Data DAG:**
Simulates company's data base therefore should be executed beforte the ETL pipeline or daily batchprocessing.

  * `airflow/dags/load_and_verify_csv_data_to_company_db_dag.py`
  * Loads CSV data into PostgreSQL, verifies the load, and tests data transformations and predictions.

* **\[OPTIONAL] ETL Pipeline DAG:**

  * `airflow/dags/etl_pipeline_dag.py`
  * Demonstrates raw ETL processing (extract-transform-load). Not mandatory for daily predictions.

* **\[MUST RUN] Batch Prediction DAG:**

  * `airflow/dags/batch_processing_dag.py`
  * Extracts raw data from db , performs transformations and predictions, loads predictions in PostgreSQL and local CSV files.

* **\[MUST RUN] Historical Predictions Update DAG (Used for data/model drift monitoring):**

  * `airflow/dags/update_historical_predictions_dag.py`
  * Epdates historical data with model predictions for accurate drift monitoring. Scheduled weekly/monthly or run manually.  

#### Manual DAG Execution

* Open Airflow webserver ([http://localhost:8080](http://localhost:8080))
* Use provided credentials (`admin` and generated password from Airflow logs)
* Manually trigger necessary DAGs

### Flask API (Online Predictions)

Provides online predictions using trained churn model.

#### Endpoints:

* **Health Check:**

```bash
curl http://localhost:5000/health
```

* **Prediction Endpoint:**

```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"TotalCharges": 500.0, "Contract": "Month-to-month", "PhoneService": "Yes", "tenure": 10}'
```


### Evidently AI (Monitoring)

Tracks data drift and model performance.

Drift Monitoring Setup:

* Generates drift reports comparing historical predictions and current prediction data.

* Historical predictions stored explicitly in PostgreSQL (table1_historical_predictions).

* Reports include both data drift and model prediction drift for comprehensive monitoring.

Report output location:
```bash
company_db_setup/data_files/evidently_report.html
```
Execution:

* Automatically triggered by Airflow DAG after batch predictions.

## Environment Configuration (`.env`)

Create `.env` from `.env_example`:

```bash
cp .env_example .env
```

Set the PostgreSQL credentials explicitly in `.env`.

---

## 🚦 Running the Project

### Build and Run Containers:

```bash
docker-compose down -v --remove-orphans
rm -rf ./db_data
docker-compose build --no-cache
docker-compose up -d

# Wait for Airflow initialization (~30 seconds)
echo " Waiting 30 seconds for Airflow to initialize..."
sleep 30

# Retrieve Airflow password from logs:
docker-compose logs airflow | grep -i "admin"
```

### Airflow Authentication:

* Check the Airflow container logs for generated admin password:

```bash
docker-compose logs airflow | grep 'Password for user admin'
```

### Manual DAG Execution:

Trigger these DAGs manually from Airflow UI (otherwise triggered automatically daily at 12:00):

1. `load_and_verify_csv_data_to_company_db_dag`
2. `batch_processing_dag`

---


**Happy MLOps-ing!**







# MLOps Project Components and Usage Instructions

## Project Components

The project consists of four main components:

1. **Airflow Container**: Handles data extraction, transformation, and loading (ETL) processes.
2. **Flask API Container**: Provides real-time model predictions.
3. **Company Database (PostgreSQL Container)**: Simulates a company database.
4. **Shared Model**: Contains the serialized RandomForest model (`churn_model.pickle`), shared by both Airflow and Flask API.

## Batch Processing with Airflow

### Step 1: Load CSV Data into Simulated Database

The folder `company_db_setup` includes CSV files in the `data_files` subdirectory, along with two Python scripts:

* `company_db_setup/load_csv_to_db.py`: Loads CSV files into PostgreSQL.
* `company_db_setup/verify_data.py`: Verifies the data is correctly loaded into the database.

### Step 2: Airflow DAGs

#### **Must Run:** `airflow/dags/load_and_verify_csv_data_to_company_db_dag.py`

* Loads CSV data into the simulated database.
* Verifies data loading.
* Performs an additional test: extracts a row from the database, transforms it using `shared_modules/transform.py`, and runs a prediction using `shared_modules/model/churn_model.pickle`.

#### **Optional:** `airflow/dags/etl_pipeline_dag.py`

* Represents a general-purpose ETL pipeline.
* Extracts raw data from the simulated database, transforms it, and loads it back into the database.
* Extraction and loading scripts are in the Airflow folder, while the transformation script is located at `shared_modules/model/verify_model_transform.py`.
* This DAG is not required for daily batch predictions.

#### **Must Run:** `airflow/dags/batch_processing_dag.py`

* Performs the main daily batch ETL processing.
* Extracts data from PostgreSQL.
* Transforms the data and performs model predictions.
* Stores prediction results back into PostgreSQL (`tableX_predictions`) and as CSV files in `company_db_setup/data_files/predictions`.

## Environment and Configuration

* **`.env`**:

  * Rename `.env_example` to `.env` and populate it with your PostgreSQL credentials.
  * **Important**: Typically, avoid including sensitive credentials in git repositories.

* **`config.yaml`**:

  * Defines paths and configurations for the project.

## Running the Project

The project uses a single `docker-compose.yaml` file to launch all three containers: Airflow, PostgreSQL, and Flask API.

Execute the following commands:

```bash
docker-compose down -v --remove-orphans
rm -rf ./db_data
docker-compose build --no-cache && docker-compose up --build
```

### Finding Airflow Credentials

Locate the Airflow credentials in the Docker logs:

```bash
docker-compose logs airflow | grep "Password for user 'admin'"
```

### Manual Trigger of DAGs

Trigger the following DAGs manually via the Airflow web interface:

1. **Load Data:** `airflow/dags/load_and_verify_csv_data_to_company_db_dag.py`
2. **Daily Predictions:** `airflow/dags/batch_processing_dag.py`

## Real-time Predictions with Flask API

### Health Check

```bash
curl http://localhost:5000/health
```

### Prediction Request

```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"TotalCharges": 500.0, "Contract": "Month-to-month", "PhoneService": "Yes", "tenure": 10}'
```

---
