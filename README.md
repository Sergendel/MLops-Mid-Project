the oroject imncludes 3 main compinents: 
1. Airflow container that runs data etl 
2. flaskapi container for predictions 
3. company db (here we simulate it postgresql container
4 model - located ion shared model fodler and will be used bopth nt airflow and flask api 



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
 2. airflow/dags/etl_pipeline_dag.py  to run the etl 





