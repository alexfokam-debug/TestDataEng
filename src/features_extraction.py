from src.data_loader import DataLoader
from src.data_preprocessing import DataPreprocessing
from src.graph_builder import GraphBuilder

class FeaturesExtraction:
    def __init__(self, data_loader, data_preprocessing, drugs_data):
        self.data_loader = data_loader
        self.data_preprocessing = data_preprocessing
        self.drugs_data = drugs_data
        self.graph_builder = graph_builder

    def extract_features(self):
        # Chargez les données brutes
        drugs_data = self.data_loader.load_drugs_data()
        pubmed_csv_data = self.data_loader.load_pubmed_csv_data()
        pubmed_json_data = self.data_loader.load_pubmed_json_data()
        clinical_trials_data = self.data_loader.load_clinical_trials_data()

        # Prétraitez les données
        drugs_data = self.data_preprocessing.preprocess_drugs_data()
        pubmed_csv_data, pubmed_json_data = self.data_preprocessing.preprocess_pubmed_data()
        clinical_trials_data = self.data_preprocessing.preprocess_clinical_trials_data()

        # Construisez le graphe
        graph = self.graph_builder.build_graph()

        return graph

# Exemple d'utilisation :
if __name__ == "__main__":
    data_loader = DataLoader()
    data_preprocessing = DataPreprocessing(data_loader)
    graph_builder = GraphBuilder(data_loader,data_preprocessing)

    features_extractor = FeaturesExtraction(data_loader, data_preprocessing, graph_builder)
    graph = features_extractor.extract_features()

