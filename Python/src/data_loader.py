import os
import pandas as pd
import json


class DataLoader:
    def __init__(self, data_dir="C:/Users/alexzaza/Downloads/Test Data Eng/Python_test_DE/"):  # Utilisez ".." pour remonter d'un niveau
        self.data_dir = data_dir

    def load_csv_data(self, filename):
        file_path = os.path.join(self.data_dir, filename)
        return pd.read_csv(file_path)

    def load_json_data(self, file_name):
        file_path = os.path.join(self.data_dir, file_name)
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    def load_drugs_data(self):
        return self.load_csv_data("drugs.csv")

    def load_pubmed_csv_data(self):
        return self.load_csv_data("pubmed.csv")

    def load_pubmed_json_data(self):
        return self.load_json_data("pubmed.json")

    def load_clinical_trials_data(self):
        return self.load_csv_data("clinical_trials.csv")


if __name__ == "__main__":
    # Exemple d'utilisation
    data_loader = DataLoader()
    drugs_data = data_loader.load_drugs_data()
    pubmed_csv_data = data_loader.load_pubmed_csv_data()
    pubmed_json_data = data_loader.load_pubmed_json_data()
    clinical_trials_data = data_loader.load_clinical_trials_data()