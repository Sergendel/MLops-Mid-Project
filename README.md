
# MLOps Project README



## 🚀 Project Overview

This project demonstrates an MLOps pipeline explicitly including ETL processing, batch predictions, and online predictions using Flask API, Airflow, PostgreSQL, and shared model files.

---

## 🎯 Project Goals

* **ETL Processing:** Automate data loading, transformation, and verification using Apache Airflow.
* **Batch Predictions:** Run daily batch predictions using Airflow DAGs.
* **Online Predictions:** Serve model predictions via a RESTful API built using Flask.

---

## 🖼️ Architecture Diagram

Refer to the architecture diagram below for visual details about the data flow and component interaction:

![Architecture Diagram](./Architecture.bmp)

---

## 📦 Technological Stack

* **Containers:** Docker and Docker Compose
* **Orchestration:** Apache Airflow
* **API Framework:** Flask
* **Database:** PostgreSQL (simulated company DB)
* **Data Handling:** Pandas, SQLAlchemy
* **Model and Data Transformation:** scikit-learn, custom shared modules

---

## 📁 Project Structure

* `airflow/` - Airflow container with DAGs and ETL scripts
* `flask_api/` - Flask container for serving predictions
* `company_db_setup/` - CSV data loading scripts and data files
* `shared_modules/` - Common transformation scripts and trained model (`churn_model.pickle`)
* `.env` - Environment variables for database credentials
* `config.yaml` - Project configuration paths
* `Architecture.bmp` - Project architecture visual representation

---

## ⚙️ Components

### 1️⃣ Airflow (Batch Processing)

**Airflow Container:** Automates ETL tasks and batch predictions.

#### Key DAGs

* **\[MUST RUN] Load and Verify CSV Data DAG:**

  * `airflow/dags/load_and_verify_csv_data_to_company_db_dag.py`
  * Loads CSV data into PostgreSQL, verifies the load, and tests data transformations and predictions.

* **\[OPTIONAL] ETL Pipeline DAG:**

  * `airflow/dags/etl_pipeline_dag.py`
  * Demonstrates raw ETL processing (extract-transform-load). Not mandatory for daily predictions.

* **\[MUST RUN] Batch Prediction DAG:**

  * `airflow/dags/batch_processing_dag.py`
  * Extracts data, performs transformations and predictions, stores predictions in PostgreSQL and CSV files.

#### Manual DAG Execution

* Open Airflow webserver ([http://localhost:8080](http://localhost:8080))
* Use provided credentials (`admin` and generated password from Airflow logs)
* Manually trigger necessary DAGs

### 2️⃣ Flask API (Online Predictions)

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

### 3️⃣ PostgreSQL Container (Simulated Company DB)

Stores data loaded from CSV and prediction results.

---

## 🔑 Environment Configuration (`.env`)

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
docker-compose build --no-cache && docker-compose up --build
```

### Airflow Authentication:

* Check the Airflow container logs for generated admin password:

```bash
docker-compose logs airflow
```

### Manual DAG Execution:

Trigger these DAGs manually from Airflow UI:

1. `load_and_verify_csv_data_to_company_db_dag`
2. `batch_processing_dag`

---

## ✅ Best Practices

* Sensitive credentials should be managed via `.env`.
* Regularly verify predictions and transformations for model drift and data integrity.

---

**Happy MLOps-ing! 🚀📊**







the oroject imncludes 3 main compinents: 
1. Airflow container that runs data etl 
2. flaskapi container for predictions 
3. company db (here we simulate it postgresql container
4 model - located ion shared model fodler and will be used bopth nt airflow and flask api 


BATCH processing (AIRFLOW)
1. load vsv data to simuklated company db datadase. 
folder company_db_setup ocludes the csv data files (see data_files subfolder) and two skripts (company_db_setup/load_csv_to_db.py and company_db_setup/verify_data.py)  that used to upload the csv files into postgresql db and verify the data is loaded corectly/ 

2. airflow dags: 

1. MUST RUN : airflow/dags/load_and_verify_csv_data_to_company_db_dag.py  - this dag is to load vsv file in to sumulated companydb. it loads the data, verify it  , and also it make another important test - it takes a row from the data  transform it (using shared_modules/transform.py in shared folder) and runs prediction by appliing shared_modules/model/churn_model.pickle on the procecced data

2. OPTIONALL: airflow/dags/etl_pipeline_dag.py  - this is the "real" etl . it extracts the raw data from companydb, transforms it and loads back to cpmpany db. the 2 skripts  extract and load are located in folder airflow, while the transform is located in shared module folder shared_modules/model/verify_model_transform.py 
Actually we do not use this etl in real batch thet requred by assigment. 

3. MUST RUN: airflow/dags/batch_processing_dag.py   runs the etl (extracts data from postgresql, trnasforms it,  run model (predictions ) loads the results PostgreSQL (tableX_predictions) + CSV files (company_db_setup/data_files/predictions)  )

.env 
put the credentials here, you can just rename the .env_exampllt to .env . (_i dont use any private keys so i put it in git, iotherwhse it a very bad porcatice)

config.yaml - used for setting like paths and so on 

how to run : 
we use single docker=compose file to up all the 3 containers (airflow, postgresql and flaskapi)]

docker-compose down -v --remove-orphans   
rm -rf ./db_data
docker-compose build --no-cache && docker-compose up --build

find the airflow credentials (look for the line  Simple auth manager | Password for user 'admin': ****************) 

manually trigger dags :
 1. airflow/dags/load_and_verify_csv_data_to_company_db_dag.py  to  upload data to simulated company db 
 2. airflow/dags/batch_processing_dag.py to run daily batch predicxtions 


Online predictions (Flask)

health test 
curl http://localhost:5000/health

prediction: curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"TotalCharges": 500.0, "Contract": "Month-to-month", "PhoneService": "Yes", "tenure": 10}'




