from src.data_loader import DataLoader
from src.data_preprocessing import DataPreprocessing
from src.features_extraction import FeaturesExtraction
from src.graph_builder import GraphBuilder
from collections import Counter


class JournalAnalyzer:
    def __init__(self, features_extractor):
        self.features_extractor = features_extractor

    def extract_journal_with_most_mentions(self):
        # Utilisez FeaturesExtractor pour obtenir le graphe
        graph = self.features_extractor.extract_features()

        # Extrait les données des médicaments prétraitées pour obtenir la liste des médicaments
        drugs_data = self.features_extractor.drugs_data
        drug_list = drugs_data['drug'].tolist()

        # Parcourez chaque nœud du graphe pour compter les mentions de médicaments dans les journaux
        journal_mentions = Counter()
        for node in graph.nodes():
            if 'journal' in graph.nodes[node]:
                journal_text = graph.nodes[node]['journal']
                for drug in drug_list:
                    if drug.lower() in journal_text.lower():
                        journal_mentions[journal_text] += 1

        # Trouvez le journal avec le plus grand nombre de mentions de médicaments
        most_mentioned_journal = journal_mentions.most_common(1)
        return most_mentioned_journal[0] if most_mentioned_journal else None


if __name__ == "__main__":
    # Créez une instance de FeaturesExtractor en utilisant les classes DataLoader et DataPreprocessing
    data_loader = DataLoader()
    data_preprocessing = DataPreprocessing(data_loader)
    graph_builder = GraphBuilder(data_loader, data_preprocessing)
    features_extractor = FeaturesExtraction(data_loader, data_preprocessing, graph_builder)


    # Créez une instance de JournalAnalyzer en utilisant FeaturesExtractor
    journal_analyzer = JournalAnalyzer(features_extractor)

    # Utilisez JournalAnalyzer pour extraire le journal avec le plus grand nombre de mentions de médicaments
    most_mentioned_journal = journal_analyzer.extract_journal_with_most_mentions()

    if most_mentioned_journal:
        print(f"Le journal qui mentionne le plus de médicaments différents est :")
        print(most_mentioned_journal[0])
    else:
        print("Aucun journal trouvé.")
