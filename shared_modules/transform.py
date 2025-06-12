import pandas as pd
from abc import ABC, abstractmethod

class BaseTransformer(ABC):
    """
    Abstract base class explicitly defining the transformation interface.
    """

    @abstractmethod
    def transform(self, dataset: pd.DataFrame) -> pd.DataFrame:
        pass


class ChurnDataTransformer(BaseTransformer):
    """
    Concrete transformer explicitly performing data transformations
    required for churn prediction.
    """

    def transform(self, dataset: pd.DataFrame) -> pd.DataFrame:
        mean_total_charges = 2279

        # Explicitly fillna and replace using .loc
        dataset.loc[:, 'TotalCharges'] = dataset['TotalCharges'].fillna(mean_total_charges)
        dataset.loc[:, 'TotalCharges'] = dataset['TotalCharges'].replace(' ', mean_total_charges).astype(float)

        # Explicitly drop NaNs safely
        dataset = dataset.dropna(subset=['Contract']).copy()

        # Explicitly fillna using .loc
        dataset.loc[:, 'PhoneService'] = dataset['PhoneService'].fillna('No')
        dataset.loc[:, 'tenure'] = dataset['tenure'].fillna(dataset['tenure'].mean())

        # Explicit mapping explicitly using .loc
        dataset.loc[:, 'PhoneService'] = dataset['PhoneService'].map({'Yes': 1, 'No': 0})

        # Explicitly create contract dummies safely
        contract_dummies = pd.get_dummies(dataset['Contract'], dtype=int)
        dataset = pd.concat([dataset, contract_dummies], axis=1)

        # Explicitly ensure required columns
        result_columns = ['TotalCharges', 'Month-to-month', 'One year', 'Two year', 'PhoneService', 'tenure']

        for col in ['Month-to-month', 'One year', 'Two year']:
            if col not in dataset.columns:
                dataset[col] = 0

        return dataset[result_columns]


if __name__ == "__main__":
    import os
    import yaml

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    with open(os.path.join(PROJECT_ROOT, 'config.yaml'), 'r') as file:
        config = yaml.safe_load(file)

    INPUT_CSV_PATH = os.path.join(PROJECT_ROOT, "./company_db_setup/data_files/raw_data/database_input.csv")
    OUTPUT_CSV_PATH = os.path.join(PROJECT_ROOT, "./company_db_setup/data_files/transformed_output.csv")


    df = pd.read_csv(INPUT_CSV_PATH)

    transformer = ChurnDataTransformer()
    transformed_df = transformer.transform(df)

    transformed_df.to_csv(OUTPUT_CSV_PATH, index=False)

    print(f"✅ Explicitly transformed data saved to {OUTPUT_CSV_PATH}")
