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
        mean_total_charges = 2279  # Explicit mean value provided by client
        dataset['TotalCharges'] = dataset['TotalCharges'].fillna(mean_total_charges)
        dataset['TotalCharges'] = dataset['TotalCharges'].replace(' ', mean_total_charges).astype(float)

        dataset = dataset.dropna(subset=['Contract'])
        dataset['PhoneService'] = dataset['PhoneService'].fillna('No')
        dataset['tenure'] = dataset['tenure'].fillna(dataset['tenure'].mean())

        dataset['PhoneService'] = dataset['PhoneService'].map({'Yes': 1, 'No': 0})

        contract_dummies = pd.get_dummies(dataset['Contract'], dtype=int)
        dataset = pd.concat([dataset, contract_dummies], axis=1)

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

    INPUT_CSV_PATH = os.path.join(PROJECT_ROOT, config['data_paths']['input_csv'])
    OUTPUT_CSV_PATH = os.path.join(PROJECT_ROOT, config['data_paths']['output_csv'])

    df = pd.read_csv(INPUT_CSV_PATH)

    transformer = ChurnDataTransformer()
    transformed_df = transformer.transform(df)

    transformed_df.to_csv(OUTPUT_CSV_PATH, index=False)

    print(f"✅ Explicitly transformed data saved to {OUTPUT_CSV_PATH}")
