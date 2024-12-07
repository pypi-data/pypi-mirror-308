
import os
import pysftp
from alive_progress import alive_bar

class QueryFlux:
    def __init__(self, flux_name="QueryF12", 
                 path_unzip="Unzip_f12",
                 path_decrypted="Decrypted_f12"
                ) -> None:
        """Iinitialisation of connetion ID"""
        self.Username =  "Mùojfebgiu" 
        self.Password = "J5xX8Gm=6y7/vYg3" 
        self.Server =  "ftp2.test.de"
        self.sftp =None
        self.folder = flux_name
        #####################################
        #### DIFFERENT FOLDERS FOR FILES ###
        ####################################
        if flux_name:
            self.create_directory(flux_name)
            self.create_directory(path_unzip)
            self.create_directory(path_decrypted)

    def setConfig(self, username, password, server):
        """This function for define ID client"""
        self.Username = username
        self.Password = password
        self.Server = server

    def set_root_directory(self):
        """This function return all folder in root"""
        if self.sftp == None:
            raise ValueError("No connection to sftp")
        folders = self.sftp.listdir_attr(".")
        list_folder =[]
        for folder in folders:
           list_folder.append(folder.filename)
        return list_folder
    
    def connect_to_sftp(self, username, password, server)->bool:
        """This function permit to access to sftp"""
        self.setConfig(username, password, server)
        status = False
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            # And authenticate with a private key
            self.sftp = pysftp.Connection(host=server, username=username, password=password, private_key=".ppk",cnopts=cnopts)
            status = True
        except Exception as e:
            print(e)
        return status
    
    def create_directory(self,directory):
        """
            Create a folder 
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully!")
            
    def change_directory_sftp(self,directory):
        """
            This function return lis of files of directory about you want change
        
        """
        self.sftp.chdir(directory)
        folders = self.sftp.listdir_attr(directory)
        list_folder =[]
        for folder in folders:
           list_folder.append(folder.filename)
        return list_folder
    
    def getFiles(self,files=[]):
        """
            1. arg -- List of path do you want download
            This function download files define in arg  
        """
        with alive_bar(len(files)) as bar:
            for file in files:
                #print(file)
                self.sftp.get(file,os.path.join(self.folder,file) )
                bar()
            
        self.disconect()

    def disconect(self):
        self.sftp.close()

    ####################
    #define setter ######
    #####################
    def setFolder_flux(self, folder_name):
        self.folder = folder_name
        self.create_directory(folder_name)