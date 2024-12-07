import pandas as pd
import json
from .Database import BDD
from .Flux import QueryFlux
from .Decryptage import Decriptage
import xml.etree.ElementTree as ET

class DataAnalysis_enedis(BDD, QueryFlux, Decriptage):
    """
    Classe combinant les fonctionnalités d'analyse de données, d'accès à une base de données,
    et de gestion des flux de fichiers spécifiques.
    """
    
    def __init__(self, path_settings="", flux_name="", path_unzip="", path_decrypted="", aes_key_hex="", iv_hex="", data=None, **kwargs):
        """
        Initialise une instance de la classe DataAnalysis_enedis.

        Args:
            path_settings (str): Chemin vers le fichier de configuration contenant les paramètres nécessaires 
                                 pour se connecter à la base de données et configurer les flux.
            flux_name (str): Nom du flux à gérer.
            path_unzip (str): Chemin vers le dossier où les fichiers décompressés seront placés.
            path_decrypted (str): Chemin vers le dossier où les fichiers décryptés seront stockés.
            data (optional): Données initiales pour remplir le DataFrame.
            **kwargs: Paramètres supplémentaires pour initialiser le DataFrame (ex. `columns`, `index`, etc.).
        """
        # Charger les paramètres de configuration
        self.__settings_json = self.load_settings(path_settings)
        
        # Initialiser les autres classes (BDD, QueryFlux, Decriptage)
        BDD.__init__(self, config_path=path_settings)
        QueryFlux.__init__(self, flux_name, path_unzip, path_decrypted)
        Decriptage.__init__(self, aes_key_hex, iv_hex)

        # Créer un DataFrame vide ou avec des données (selon l'argument `data`)
        if data is not None:
            self.df = pd.DataFrame(data, **kwargs)
        else:
            self.df = pd.DataFrame()

 
    def load_settings(self, config_file):
        with open(config_file) as file:
            return json.load(file)
        

    def get_content_HT(self, file_path, output_name=""):
        """
        Lit un fichier JSON contenant des mesures, transforme les données en DataFrame et les enregistre dans un fichier Excel.
        
        :param file_path: chemin du fichier JSON
        :param output_name: nom du fichier Excel de sortie
        """
        with open(file_path, "r") as read_json:
            json_content = json.load(read_json)

        json_mesure_data = json_content["mesures"][0]
        idPrm = json_mesure_data['idPrm']
        data = pd.DataFrame(json_mesure_data["contexte"])

        global_content = []

        for _ , row in data.iterrows():
            _grandeurs = row['grandeur']
            for   grandeur in _grandeurs :
                grandeurPhysique = grandeur["grandeurPhysique"]
                unite = grandeur["unite"]

                data = pd.DataFrame(grandeur)
                sous_data = data['calendrier'] 
                data = pd.DataFrame(sous_data)
                #plusieur dic dans grandeur
                for _ , row in data.iterrows():
                    idCalendrier = row.iloc[0]['idCalendrier']
                    content =  row.iloc[0]['classeTemporelle']
                    df_content = pd.DataFrame(content)
                    list_Sous_content_df = []
                    #parse le content
                    for _ , row in df_content.iterrows():
                        _json_valeur = row['valeur']
                        libelleClasseTemporelle = row['libelleClasseTemporelle']
                        Sous_content_df = pd.DataFrame(_json_valeur)
                        Sous_content_df.insert(2,"libelleClasseTemporelle",libelleClasseTemporelle )
                        Sous_content_df.insert(3,"idCalendrier",idCalendrier )
                        #append chaque partie de libelleClasseTemporelle
                        list_Sous_content_df.append(Sous_content_df)
                Sous_content_df = pd.concat(list_Sous_content_df, axis=0)
                Sous_content_df.reset_index(inplace=True)
                Sous_content_df.insert(3,"grandeurPhysique",grandeurPhysique )
                Sous_content_df.insert(3,"unite",unite )
                global_content.append(Sous_content_df)

        global_content_df = pd.concat(global_content, axis=0)
        global_content_df.reset_index(inplace=True)

        global_content_df = global_content_df[["d","v","unite","grandeurPhysique","libelleClasseTemporelle","idCalendrier","iv"]]
        global_content_df["libelleClasseTemporelle"] = global_content_df["libelleClasseTemporelle"].apply(lambda x: x.encode("latin1").decode("utf-8"))
        global_content_df.insert(0,"prm",idPrm)
        global_content_df.to_excel(f"""{output_name}.xlsx""", index=False)
        return global_content_df
    
    ################################
    ## Parse f12 fl file ###########
    ################################

    def f12_parse_xml_fl(self,path =""):
        """
        Cette fonctionne retourne un dataframe parser  prenant en compte le path du fichier fl
        """

        general_data = {}         # Pour les données de En_Tete_Flux et Rappel_En_Tete
        sous_lots_data = []       # Liste pour stocker chaque Sous_Lot
        sous_total_data = {}      # Pour les données de Sous_Total_Fichier

        try:
            # Chargement du fichier XML
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Erreur de lecture du fichier XML : {e}")

        # Extraction des données générales dans En_Tete_Flux et Rappel_En_Tete
        en_tete_flux = root.find('En_Tete_Flux')
        rappel_en_tete = root.find('Rappel_En_Tete')

        if en_tete_flux is not None:
            for child in en_tete_flux:
                general_data[child.tag] = child.text

        if rappel_en_tete is not None:
            for child in rappel_en_tete:
                general_data[child.tag] = child.text

        # Extraction des données de chaque Sous_Lot
        for sous_lot in root.findall('Sous_Lot'):
           
            unique_data = {} # Dictionnaire pour les données uniques de chaque Sous_Lot
            sous_lot_data = {
                "PS_Poste_Horosaisonnier": [],
                "Element_Valorise": [],
                "Sous_Total": {}
            }

            # Extraction des informations générales dans Sous_Lot
            for child in sous_lot:
                if child.tag not in ["PS_Poste_Horosaisonnier", "Element_Valorise", "Sous_Total"]:
                    unique_data[child.tag] = child.text

            # Extraction des données de PS_Poste_Horosaisonnier
            for ps_poste in sous_lot.findall('PS_Poste_Horosaisonnier'):
                ps_data = unique_data.copy()  # Copier les données uniques
                for child in ps_poste:
                    ps_data[child.tag] = child.text
                sous_lot_data["PS_Poste_Horosaisonnier"].append(ps_data)

            # Extraction des données de Element_Valorise
            for element_valorise in sous_lot.findall('Element_Valorise'):
                element_data = unique_data.copy()  # Copier les données uniques
                for child in element_valorise:
                    element_data[child.tag] = child.text
                sous_lot_data["Element_Valorise"].append(element_data)
            
            # Extraction des données de Sous_Total
            sous_total = sous_lot.find('Sous_Total')
            if sous_total is not None:
                sous_total_data = unique_data.copy()  # Copier les données uniques
                for child in sous_total:
                    sous_total_data[child.tag] = child.text
                sous_lot_data["Sous_Total"] = [sous_total_data]  # Sous_Total en liste

            # Ajout du Sous_Lot complet à la liste sous_lots_data
            sous_lots_data.append(sous_lot_data)

        # Création des DataFrames pour chaque section de Sous_Lot
        df_sous_lot = pd.DataFrame()

        for lot in sous_lots_data:
            # Convertir chaque partie en DataFrame
            df_ps_poste = pd.DataFrame(lot["PS_Poste_Horosaisonnier"])
            df_element_valorise = pd.DataFrame(lot["Element_Valorise"])
            df_sous_total = pd.DataFrame(lot["Sous_Total"])

            # Concaténer les DataFrames en remplissant les données manquantes par NaN
            df_lot = pd.concat([df_ps_poste, df_element_valorise, df_sous_total], ignore_index=True)
            
            # Ajouter au DataFrame principal
            df_sous_lot = pd.concat([df_sous_lot, df_lot], ignore_index=True)

        # Transformation de general_data en DataFrame et combinaison
        df_general = pd.DataFrame([general_data] * len(df_sous_lot))
        df_global = pd.concat([df_general, df_sous_lot], axis=1)

        return df_global
    
    ###########################
    ####f15 parse file ########
    ###########################


    def f15_parse_xml_fl(self,file_path):
        """Parse le fichier XML et retourne un dictionnaire de DataFrames."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Erreur de lecture du fichier XML : {e}")
            return None

        # Récupérer les données générales dans En_Tete_Flux et Rappel_En_Tete
        en_tete_flux = root.find('En_Tete_Flux')
        rappel_en_tete = root.find('Rappel_En_Tete')

        general_data = {}

        # Extraction des balises dans En_Tete_Flux
        if en_tete_flux is not None:
            for child in en_tete_flux:
                general_data[child.tag] = child.text

        # Extraction des balises dans Rappel_En_Tete
        if rappel_en_tete is not None:
            for child in rappel_en_tete:
                general_data[child.tag] = child.text

        dataframes = {}

        # Traitement des Donnees_Valorisation
        for donnees_valorisation in root.findall('Donnees_Valorisation'):
            id_prm = donnees_valorisation.find('Donnees_PRM').find('Id_PRM').text
            groupe_valorise = donnees_valorisation.find('Groupe_Valorise')
            elements = []

            # Récupération des éléments valorisés
            for element_valorise in groupe_valorise.findall('Element_Valorise'):
                element = {}
                for child in element_valorise:
                    element[child.tag] = child.text
                elements.append(element)

            # Récupérer les autres informations dans Donnees_Valorisation
            valorisation_data = {}
            for tag in ['Num_Valorisation', 'Type_Facturation', 'Total_Valorise_HT', 'Date_Debut_Part_Fixe', 'Date_Fin_Part_Fixe',
                        'Date_Debut_Part_Variable', 'Date_Fin_Part_Variable', 'Date_Effet', 'Periode_Ante_Migration']:
                valorisation_data[tag] = donnees_valorisation.find(tag).text if donnees_valorisation.find(tag) is not None else None

            # Récupération de l'Id_Releve
            id_releve = donnees_valorisation.find('Releve').find('Id_Releve').text if donnees_valorisation.find('Releve') is not None else None

            # Récupération des informations de Donnees_PRM
            prm_data = {}
            donnees_prm = donnees_valorisation.find('Donnees_PRM')
            if donnees_prm is not None:
                for child in donnees_prm:
                    prm_data[child.tag] = child.text

            # Création du DataFrame pour cet Id_PRM
            df = pd.DataFrame(elements)

            # Ajouter les colonnes des informations de valorisation et de PRM
            for key, value in {**valorisation_data, **prm_data}.items():
                df[key] = value

            # Ajouter la colonne 'Id_Releve' et remplir avec la même valeur
            if id_releve:
                df['Id_Releve'] = id_releve

            # Ajouter les données générales récupérées dans En_Tete_Flux et Rappel_En_Tete
            for key, value in general_data.items():
                df[key] = value

            # Ajouter le DataFrame à la collection de dataframes
            if id_prm in dataframes:
                # Si la clé existe, on concatène le nouveau DataFrame avec l'existant
                dataframes[id_prm] = pd.concat([dataframes[id_prm], df], ignore_index=True)

            else:
                # Si la clé n'existe pas, on l'ajoute au dictionnaire
                dataframes[id_prm] = df

        return dataframes
    

    def f15_parse_xml_fa(self, path_file):
       
        """
        This function read XML file
        """
        tree = ET.parse(path_file)
        root = tree.getroot()

        # Crée un dictionnaire pour stocker les données
        data = {}

        # Parcours les éléments du fichier XML
        for elem in root.iter():
            # Si l'élément a des attributs, les ajoute au dictionnaire
            if elem.attrib:
                for key, value in elem.attrib.items():
                    if f"{elem.tag}_{key}" not in data:
                        data[f"{elem.tag}_{key}"] = []
                    data[f"{elem.tag}_{key}"].append(value)
            # Si l'élément a du texte, l'ajoute au dictionnaire
            elif elem.text:
                if elem.tag not in data:
                    data[elem.tag] = []
                data[elem.tag].append(elem.text)

        # Crée un dataframe à partir du dictionnaire
        max_len = max(len(v) for v in data.values())
        for k, v in data.items():
            if len(v) < max_len:
                v.extend([v[-1]] * (max_len - len(v)))

        df = pd.DataFrame(data)

        return df

    ##########################
    #getter parameters #######
    ###########################
    #username, password, server
    def get_sftp_username(self):
        """
        Retourne le nom d'utilisateur SFTP défini dans le fichier de configuration JSON.

        Returns:
            str: Le nom d'utilisateur SFTP.
        """
        return self.__settings_json["sftp"]["username"]

    def get_sftp_password(self):
        """
        Retourne le mot de passe SFTP défini dans le fichier de configuration JSON.

        Returns:
            str: Le mot de passe SFTP.
        """
        return self.__settings_json["sftp"]["password"]

    def get_sftp_server(self):
        """
        Retourne l'adresse du serveur SFTP définie dans le fichier de configuration JSON.

        Returns:
            str: L'adresse du serveur SFTP.
        """
        return self.__settings_json["sftp"]["server"]

    def get_sftp_directory_f15(self):
        """
        Retourne le répertoire F15 sur le serveur SFTP, défini dans le fichier de configuration JSON.

        Returns:
            str: Le chemin du répertoire F15.
        """
        return self.__settings_json["sftp"]["directory_f15"]

    def get_sftp_directory_f12(self):
        """
        Retourne le répertoire F12 sur le serveur SFTP, défini dans le fichier de configuration JSON.

        Returns:
            str: Le chemin du répertoire F12.
        """
        return self.__settings_json["sftp"]["directory_f12"]

    def get_sftp_directory(self, name_directory=""):
        """
        Retourne le chemin d'un répertoire spécifique sur le serveur SFTP.

        Args:
            name_directory (str): Le nom du répertoire à récupérer. Ce nom doit correspondre
                                à une clé existante dans la section "sftp" du fichier de configuration.

        Returns:
            str: Le chemin du répertoire correspondant ou une chaîne vide si le nom du répertoire n'est pas spécifié.

        Raises:
            KeyError: Si le nom du répertoire spécifié n'existe pas dans la configuration.
        """
        try:
            return self.__settings_json["sftp"][name_directory]
        except KeyError:
            raise KeyError(f"Le répertoire '{name_directory}' n'existe pas dans la configuration SFTP.")

    
    def get_aes_key_decryptage(self):
        """
        Retourne la clé AES utilisée pour le décryptage, définie dans le fichier de configuration.

        Returns:
            str: La clé AES en format hexadécimal.
        """
        return self.__settings_json["decryptage"]["aes_key_hex"]

    def get_iv_decryptage(self):
        """
        Retourne le vecteur d'initialisation (IV) utilisé pour le décryptage, défini dans le fichier de configuration.

        Returns:
            str: Le vecteur d'initialisation en format hexadécimal.
        """
        return self.__settings_json["decryptage"]["iv_hex"]
