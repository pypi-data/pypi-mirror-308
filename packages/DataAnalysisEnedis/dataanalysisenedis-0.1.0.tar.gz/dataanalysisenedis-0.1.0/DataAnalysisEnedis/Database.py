import json
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, Date, UniqueConstraint,DateTime
from sqlalchemy.engine.reflection import Inspector

class BDD:
    def __init__(self, config_path="db_settings.json") -> None:
        """
        Initialise la connexion à la base de données en utilisant les paramètres de configuration.
        """
        # Chargement des paramètres depuis le fichier de configuration
        self.config = self.load_config(config_path)
        
        # Initialisation des attributs de connexion
        self.database = self.config.get("postgresql_database", "")
        self.user = self.config.get("postgresql_user", "")
        self.password = self.config.get("postgresql_password", "")
        self.host = self.config.get("postgresql_host", "")
        self.port = self.config.get("postgresql_port", 5432)  # valeur par défaut pour PostgreSQL

        # Création de l'objet engine
        self.engine = None #self.connect()
        self.metadata = MetaData()

    @staticmethod
    def load_config(config_path):
        """
        Charge les paramètres de configuration depuis un fichier JSON.
        """
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    def connect_to_postgresql(self, database, user, password, host, port):
        """
        Met à jour les paramètres de connexion et recrée l'objet engine.
        """
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.engine = self.connect()
    
    def connect_to_postgresql(self):
        """
        Crée une connexion à PostgreSQL avec les paramètres fournis.
        """
        self.engine = self.connect()

    def connect(self):
        """
        Crée une connexion à PostgreSQL avec les paramètres fournis.
        """
        return create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')

    def connect_to_sqlServer(self, options='-csearch_path=dbo'):
        """
        Crée une connexion à SQL Server en utilisant les paramètres de configuration.
        Si `options` est vide, utilise la valeur par défaut '-csearch_path=dbo'.
        """
        # Récupération des paramètres de connexion depuis la configuration
        server_user = self.config.get("sql_server_user", "")
        server_password = self.config.get("sql_server_password", "")
        server_host = self.config.get("sql_server_host", "")
        server_port = self.config.get("sql_server_port", 1433)
        server_database = self.config.get("sql_server_database", "")
        driver = self.config.get("sql_server_driver", "ODBC Driver 17 for SQL Server")

        # Création de la chaîne de connexion
        connection_string = f'mssql+pyodbc://{server_user}:{server_password}@{server_host}:{server_port}/{server_database}?driver={driver}'
        
        # Si options est vide, utiliser la valeur par défaut '-csearch_path=dbo'
        if not options:
            options = '-csearch_path=dbo'
        
        # Connexion avec les options spécifiées
        self.engine = create_engine(connection_string, connect_args={'options': options})
        return self.engine

    
    def create_table(self, table_name, columns_json, unique_columns=None):
        """
        Crée une table avec les colonnes spécifiées et une contrainte unique facultative.
        
        Args:
            table_name (str): Nom de la table à créer.
            columns_json (dict): Dictionnaire décrivant les colonnes et leurs propriétés (type, taille, nullable).
            unique_columns (list or None): Liste de noms de colonnes pour la contrainte unique, ou None si aucune contrainte.
        """
        inspector = Inspector(self.engine)
        
        # Vérifie si la table existe déjà
        if not inspector.has_table(table_name):
            columns = []
            
            # Parcourt chaque colonne dans columns_json
            for col_name, col_info in columns_json.items():
                col_type = col_info.get("type")
                nullable = col_info.get("nullable", True)
                length = col_info.get("length", None)
                
                # Détermine le type SQLAlchemy de la colonne
                if col_type == "VARCHAR" and length:
                    column = Column(col_name, String(length), nullable=nullable)
                elif col_type == "VARCHAR":
                    column = Column(col_name, String, nullable=nullable)
                elif col_type == "INTEGER":
                    column = Column(col_name, Integer, nullable=nullable)
                elif col_type == "FLOAT":
                    column = Column(col_name, Float, nullable=nullable)
                elif col_type == "DATE":
                    column = Column(col_name, Date, nullable=nullable)
                elif col_type == "DATETIME":
                    column = Column(col_name, DateTime, nullable=nullable)
                else:
                    raise ValueError(f"Type de colonne non supporté: {col_type}")

                columns.append(column)
            
            # Ajoute la contrainte unique si unique_columns est fourni
            if unique_columns:
                unique_constraint = UniqueConstraint(*unique_columns, name=f"unique_{table_name}")
                columns.append(unique_constraint)
            
            # Crée la table avec les colonnes et la contrainte
            table = Table(table_name, self.metadata, *columns)
            self.metadata.create_all(self.engine, [table])
            print(f"Table {table_name} créée avec succès.")


    def insert_into(self, table, data=pd.DataFrame()):
        """
        Insère les données d'un DataFrame Pandas dans une table SQL.
        
        Args:
            table (str): Nom de la table dans laquelle insérer les données.
            data (pd.DataFrame): Le DataFrame contenant les données à insérer.
        """
        if data.empty:
            print("Aucune donnée à insérer.")
            return

        try:
            # Insère le DataFrame dans la table SQL
            data.to_sql(table, self.engine, if_exists='append', index=False)
            print(f"Les données ont été insérées dans la table {table}.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données dans {table}: {e}")


    def __get_column_type(self, column_type: str):
        """
        Retourne le type de la colonne en fonction du type donné sous forme de chaîne.
        """
        type_mapping = {
            "Integer": Integer,
            "Float": Float,
            "String": String,
            "Date": Date,
            "Datetime":DateTime
        }
        return type_mapping.get(column_type, String)  # Défaut à String si non trouvé

    def getEngine(self):
        """
        Retourne l'instance actuelle de l'objet engine.
        """
        return self.engine

    def disconnect(self):
        """
        Ferme la connexion en disposant de l'engine.
        """
        if self.engine:
            self.engine.dispose()
