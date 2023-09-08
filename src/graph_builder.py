import networkx as nx

class GraphBuilder:
    def __init__(self, data_loader, data_preprocessing):
        self.data_loader = data_loader
        self.data_preprocessing = data_preprocessing

    def build_graph(self):
        # Chargement des données
        drugs_data = self.data_loader.load_drugs_data()
        pubmed_csv_data = self.data_loader.load_pubmed_csv_data()
        pubmed_json_data = self.data_loader.load_pubmed_json_data()
        clinical_trials_data = self.data_loader.load_clinical_trials_data()

        # Prétraitement des données
        drugs_data = self.data_preprocessing.preprocess_drugs_data()
        pubmed_csv_data, pubmed_json_data = self.data_preprocessing.preprocess_pubmed_data()
        clinical_trials_data = self.data_preprocessing.preprocess_clinical_trials_data()

        # Création du graphe
        graph = nx.Graph()

        # Ajout des médicaments comme nœuds
        for _, row in drugs_data.iterrows():
            drug_id = row['atccode']
            drug_name = row['drug']
            graph.add_node(drug_id, type='drug', name=drug_name)

        # Ajout des publications PubMed comme nœuds
        for _, row in pubmed_csv_data.iterrows():
            pubmed_id = row['id']
            pubmed_title = row['title']
            graph.add_node(pubmed_id, type='pubmed', title=pubmed_title)

        # Ajout des essais cliniques comme nœuds
        for _, row in clinical_trials_data.iterrows():
            clinical_trial_id = row['id']
            clinical_trial_title = row['scientific_title']
            graph.add_node(clinical_trial_id, type='clinical_trial', title=clinical_trial_title)

        # Création des arêtes entre les médicaments et les publications PubMed
        for _, row in pubmed_csv_data.iterrows():
            pubmed_id = row['id']
            pubmed_title = row['title']
            drug_mentions = row['drug_mentions']
            if drug_mentions > 0:
                # Trouver les médicaments mentionnés dans le titre
                mentioned_drugs = self.find_mentioned_drugs(pubmed_title, drugs_data)
                # Créer des arêtes entre la publication et les médicaments mentionnés
                for drug_id, drug_name in mentioned_drugs:
                    graph.add_edge(pubmed_id, drug_id, relation='mentioned_in', drug_name=drug_name)

        # Création des arêtes entre les médicaments et les essais cliniques
        for _, row in clinical_trials_data.iterrows():
            clinical_trial_id = row['id']
            clinical_trial_title = row['scientific_title']
            # Trouver les médicaments mentionnés dans le titre
            mentioned_drugs = self.find_mentioned_drugs(clinical_trial_title, drugs_data)
            # Créer des arêtes entre l'essai clinique et les médicaments mentionnés
            for drug_id, drug_name in mentioned_drugs:
                graph.add_edge(clinical_trial_id, drug_id, relation='mentioned_in', drug_name=drug_name)

        return graph

    def find_mentioned_drugs(self, text, drugs_data):
        # Fonction pour trouver les médicaments mentionnés dans un texte
        mentioned_drugs = []
        for _, row in drugs_data.iterrows():
            drug_id = row['atccode']
            drug_name = row['drug']
            if drug_name.lower() in text.lower():
                mentioned_drugs.append((drug_id, drug_name))
        return mentioned_drugs
