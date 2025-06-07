import pandas as pd
from sqlalchemy import create_engine
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv

# Explicitly load credentials from .env
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}'


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        pass


class PostgresExtractor(BaseExtractor):
    def __init__(self, db_uri, table_name):
        self.db_uri = db_uri
        self.table_name = table_name

    def extract(self) -> pd.DataFrame:
        engine = create_engine(self.db_uri)
        query = f'SELECT * FROM {self.table_name};'
        df = pd.read_sql(query, engine)
        print(f"✅ Explicitly extracted data from '{self.table_name}'")
        return df


if __name__ == "__main__":
    extractor = PostgresExtractor(DATABASE_URI, 'table1')
    raw_df = extractor.extract()

    print("✅ Explicitly displaying extracted data:")
    print(raw_df.head())
