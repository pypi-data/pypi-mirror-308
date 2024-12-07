from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import zipfile
import os


class Decriptage:

    def __init__(self, aes_key_hex, iv_hex):
        """
            call Instance of Decriptage
        """
        self.encrypted_zip_path =None
        self.setKeys(aes_key_hex, iv_hex)
    
    def setKeys(self, aes_key_hex, iv_hex):
        """call Instance of Decriptage_F15 
            aes_key_hex <- string of aes
            iv_hex <-  string of pwd
        """
        self.aes_key_hex = aes_key_hex
        self.iv_hex  = iv_hex
        try:
            self.__set_AES()
        except Exception as e:
            print(e)

    def __set_AES(self):
        """
        define parameter of AEPS
        # Convert keys hexa to bytes
        """
        self.aes_key = bytes.fromhex(self.aes_key_hex)
        self.iv = bytes.fromhex(self.iv_hex)

    def setFile_encripted(self,encrypted_path_file,derypted_path_file, path_unzip):
        """
            Path to of files 
            encrypted_path_file::
            derypted_path_file::
            path_unzip
        """
        self.encrypted_zip_path = encrypted_path_file
        self.decrypted_zip_path = derypted_path_file
        self.extraction_path = path_unzip

    def decrypt_file(self, input_path, output_path,path_unzip):

        self.setFile_encripted(input_path,output_path, path_unzip)

        with open(input_path, 'rb') as encrypted_file:
            cipher = AES.new(self.aes_key, AES.MODE_CBC, self.iv)
            encrypted_data = encrypted_file.read()
            
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
            
            with open(output_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)

    def unzip_file(self):
        
        # Extract all file in zip file
        with zipfile.ZipFile(self.decrypted_zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extraction_path)

        # Obtenir la liste des noms des fichiers extraits
        extracted_files = zip_ref.namelist()
        return extracted_files



