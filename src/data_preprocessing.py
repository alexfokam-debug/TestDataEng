from dateutil import parser
from unidecode import unidecode
import pandas as pd


# Classe de prétraitement générique
class Preprocessor:
    def __init__(self, data_loader):
        self.data_loader = data_loader

    # Méthode de prétraitement générique
    def preprocess(self, data, date_column=None, text_column=None, text_cleanup=True):
        # Convertir la colonne de date en datetime si spécifiée
        if date_column:
            data[date_column] = data[date_column].apply(lambda x: parser.parse(x, fuzzy=True))
        # Appliquer le nettoyage de texte si spécifié
        if text_column:
            if text_cleanup:
                data[text_column] = data[text_column].apply(self.clean_text)
            # Convertir le texte en minuscules
            data[text_column] = data[text_column].str.lower()
        return data

    # Méthode de nettoyage de texte générique
    @staticmethod
    def clean_text(text):
        # Gérer les cas où la valeur est nulle
        if pd.isnull(text):
            return ""
        # Utiliser unidecode pour gérer les caractères accentués
        text = unidecode(text)
        # Supprimer tous les caractères non alphabétiques ou non espacés
        text = ''.join(e for e in text if e.isalpha() or e.isspace())
        return text


# Classe principale de prétraitement des données
class DataPreprocessing:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        # Créer une instance de la classe Preprocessor pour le prétraitement générique
        self.preprocessor = Preprocessor(data_loader)

    # Méthode de prétraitement des données de médicaments
    def preprocess_drugs_data(self):
        drugs_data = self.data_loader.load_drugs_data()
        # Supprimez les doublons et réindexez
        drugs_data = drugs_data.drop_duplicates().reset_index(drop=True)

        return drugs_data

    # Méthode de prétraitement des données PubMed
    def preprocess_pubmed_data(self):
        pubmed_csv_data = self.data_loader.load_pubmed_csv_data()
        # Appliquez le prétraitement générique aux données
        pubmed_csv_data = self.preprocessor.preprocess(pubmed_csv_data, date_column='date', text_column='journal')
        # Créez la colonne 'drug_mentions' en fonction des données traitées
        pubmed_csv_data['drug_mentions'] = pubmed_csv_data['journal'].str.count('médicament|drogue|remède')

        pubmed_json_data = self.data_loader.load_pubmed_json_data()
        return pubmed_csv_data, pubmed_json_data

    # Méthode de prétraitement des données des essais cliniques
    def preprocess_clinical_trials_data(self):
        clinical_trials_data = self.data_loader.load_clinical_trials_data()
        # Appliquez le prétraitement générique aux données
        clinical_trials_data = self.preprocessor.preprocess(clinical_trials_data, date_column='date',
                                                            text_column='journal')
        # Appliquez des transformations spécifiques au journal
        clinical_trials_data.at[7, 'journal'] = clinical_trials_data.at[7, 'journal'][:-3]
        return clinical_trials_data
