import sys
import pandas as pd
sys.path.append("D:/Zephyr_librairie")
from DataAnalysisEnedis import DataAnalysis_enedis

ID_TEST = 3

# Initialisation de la classe avec le fichier de configuration
dataAnalysis_enedis = DataAnalysis_enedis("tests/settings.json")

match (ID_TEST):

    case 1:
        # Lire les données pour le type d'injection / soutirage HT
        data = dataAnalysis_enedis.get_content_HT("tests/data/ENEDIS_R64_P_INDEX_M073565K_00001_20241112103114_Injection.JSON", "content")
        data['d'] = pd.to_datetime(data['d'])

        # Définir les données pour l'insertion dans la base de données
        columns_json = {
            "prm": {"type": "VARCHAR", "length": 14, "nullable": True},
            "d": {"type": "DATETIME", "nullable": True},
            "v": {"type": "FLOAT", "nullable": True},
            "unite": {"type": "VARCHAR", "length": 5, "nullable": True},
            "grandeurPhysique": {"type": "VARCHAR", "length": 5, "nullable": True},
            "libelleClasseTemporelle": {"type": "VARCHAR", "length": 100, "nullable": True},
            "idCalendrier": {"type": "VARCHAR", "length": 20, "nullable": True},
            "iv": {"type": "VARCHAR", "length": 5, "nullable": True},
        }

        # Connexion et insertion dans la base de données
        dataAnalysis_enedis.connect_to_sqlServer()
        dataAnalysis_enedis.create_table("ht_injection", columns_json, None)
        dataAnalysis_enedis.insert_into("ht_injection", data)

    case 2:
        # Connexion SFTP et récupération de fichiers depuis le dossier f12
        status = dataAnalysis_enedis.connect_to_sftp(dataAnalysis_enedis.get_sftp_username(),
                                                    dataAnalysis_enedis.get_sftp_password(),
                                                    dataAnalysis_enedis.get_sftp_server())
        folders = dataAnalysis_enedis.set_root_directory()
        files_f12 = dataAnalysis_enedis.change_directory_sftp(dataAnalysis_enedis.get_sftp_directory_f12())

        dataAnalysis_enedis.setFolder_flux("fichiers_f12")
        dataAnalysis_enedis.getFiles(files_f12)

    case 3:
        # Connexion SFTP et récupération de fichiers depuis le dossier f15
        status = dataAnalysis_enedis.connect_to_sftp(dataAnalysis_enedis.get_sftp_username(),
                                                    dataAnalysis_enedis.get_sftp_password(),
                                                    dataAnalysis_enedis.get_sftp_server())
        folders = dataAnalysis_enedis.set_root_directory()
        files_f15 = dataAnalysis_enedis.change_directory_sftp(dataAnalysis_enedis.get_sftp_directory_f15())

        # Création des répertoires et décryptage de fichiers
        dataAnalysis_enedis.create_directory("fichiers_decrypters")
        dataAnalysis_enedis.create_directory("content_zip")

        dataAnalysis_enedis.setKeys(dataAnalysis_enedis.get_aes_key_decryptage(),
                                    dataAnalysis_enedis.get_iv_decryptage())

        dataAnalysis_enedis.decrypt_file("fichiers_f15\\17X100A100A0001A_F15_17X000001117366M_GRD-F139_0322_C_M_0_P_00001_20240603050837.zip",
                                          "fichiers_decrypters\\17X100A100A0001A_F15_17X000001117366M_GRD-F139_0322_C_M_0_P_00001_20240603050837.zip",
                                          "content_zip")
