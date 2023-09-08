import networkx as nx
import matplotlib.pyplot as plt
from src.data_loader import DataLoader
from src.data_preprocessing import DataPreprocessing
from src.graph_builder import GraphBuilder


def main():
    # Créez une instance de DataLoader
    data_loader = DataLoader()

    # Utilisez DataLoader pour charger les données
    drugs_data = data_loader.load_drugs_data()
    pubmed_csv_data = data_loader.load_pubmed_csv_data()
    pubmed_json_data = data_loader.load_pubmed_json_data()
    clinical_trials_data = data_loader.load_clinical_trials_data()

    # Affichez les données chargées
    print("Données des médicaments chargées :")
    print(drugs_data)

    print("\nDonnées PubMed (CSV) chargées :")
    print(pubmed_csv_data)

    print("\nDonnées PubMed (JSON) chargées :")
    print(pubmed_json_data)

    print("\nDonnées des essais cliniques chargées :")
    print(clinical_trials_data)

    # Créez une instance de DataPreprocessing en utilisant la DataLoader
    data_preprocessing = DataPreprocessing(data_loader)

    # Utilisez DataPreprocessing pour effectuer des prétraitements
    preprocessed_drugs_data = data_preprocessing.preprocess_drugs_data()
    preprocessed_pubmed_csv_data, preprocessed_pubmed_json_data = data_preprocessing.preprocess_pubmed_data()
    preprocessed_clinical_trials_data = data_preprocessing.preprocess_clinical_trials_data()

    # Affichez les données prétraitées
    print("\nDonnées des médicaments après prétraitement :")
    print(preprocessed_drugs_data)

    print("\nDonnées PubMed (CSV) après prétraitement :")
    print(preprocessed_pubmed_csv_data)

    print("\nDonnées PubMed (JSON) après prétraitement :")
    print(preprocessed_pubmed_json_data)

    print("\nDonnées des essais cliniques après prétraitement :")
    print(preprocessed_clinical_trials_data)

    # Créez une instance de GraphBuilder en utilisant la DataLoader et DataPreprocessing
    graph_builder = GraphBuilder(data_loader, data_preprocessing)

    # Utilisez GraphBuilder pour construire le graphe
    graph = graph_builder.build_graph()

    # Affichez des informations sur le graphe, par exemple le nombre de nœuds et d'arêtes
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    print(f"\nGraphe construit avec {num_nodes} nœuds et {num_edges} arêtes.")

    # Créez une nouvelle figure
    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    # Dessinez le graphe
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=300, node_color="skyblue", font_size=8, font_color="black", ax=ax)

    # Affichez le graphe
    plt.show()
    # Sauvegardez le graphe au format GML (ou dans le format de votre choix)
    nx.write_gml(graph, "output/graph.gml")
    print("\nGraphe sauvegardé dans 'output/graph.gml'.")


if __name__ == "__main__":
    main()
