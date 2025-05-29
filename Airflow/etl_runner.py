# etl_runner.py for ETL 
from shared_modules.data_preparation import prepare_data

def run_batch_etl():
    raw_data = extract_from_db()
    prepared_data = prepare_data(raw_data)
    save_to_db(prepared_data)
