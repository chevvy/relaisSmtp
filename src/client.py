# coding=utf-8
import smtplib
from email.mime.text import MIMEText
import socket
import getpass


class ObjetReseau:
    def __init__(self, p_ip, p_port):
        self.ip = p_ip
        self.port = int(p_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def read(self, buffer=1024):
        """ Lit la réponse envoyé sur le socket """
        return self.socket.recv(buffer)

    def write(self, data):
        print(data)
        self.socket.send(data)

    def close(self):
        self.socket.close()

    @staticmethod
    def conversion_byte_to_string(byte_a_convertir, encodage="utf-8"):
        """
        Converti un byte reçu en argument vers un string et le retourne
        :param encodage: l'encodage (par défaut UTF-8)
        :param byte_a_convertir: un string de character ou chiffre
        :return: string: le string converti
        """
        string_converti = byte_a_convertir.decode(encodage)
        return string_converti

    @staticmethod
    def conversion_string_to_byte(element_a_convertir, encodage="utf-8"):
        """
        Converti un string en byte, encoder dans un encodage spécifique (par défaut = UTF-8)
        :param encodage:
        :param element_a_convertir:
        :return:
        """
        string = str(element_a_convertir)
        return str.encode(string, encodage)


class Client(ObjetReseau):
    def __init__(self, p_ip, p_port):
        self.objet_reseau = ObjetReseau.__init__(self, p_ip, p_port)
        self.utilisateur_courant = None

    def execution_client_courriel(self, type_execution):
        info_connexion_serveur = (self.ip, self.port)
        self.socket.connect(info_connexion_serveur)

        self.socket.send(self.conversion_string_to_byte(type_execution))  # envoi du mode dexecution

        login_info = self.connection_utilisateur()
        self.socket.send(self.conversion_string_to_byte(login_info))  # envoi du login user

        data = self.socket.recv(1024).decode()  # attente de la réponse du serveur pour la création/login
        data_liste = data.split("/")

        montrer_menu = data_liste[0]
        message_validation = data_liste[1]
        print(" message de vallidation " + message_validation)
        if montrer_menu == "True":
            self.menu_principal()

        self.socket.close()

    def envoi_courriel(self, expediteur, destinataire, sujet, text):
        print("Data : ")


    def connection_utilisateur(self):
        if action == 1:
            print("Création d'un compte")
        if action == 2:
            print("Connection à un compte")
        print("Entrez votre nom d'usager")
        nom_usager = input()
        print("Entrez votre mot de passe")
        mot_de_passe = input()
        return nom_usager + ' ' + mot_de_passe

    def menu_principal(self):
        quitter = False
        while not quitter:
            print("Menu principal")
            print("1. Consultation de courriels")
            print("2. Envoi de courriels")
            print("3. Statistiques")
            print("4. Quitter")
            choix = int(input())
            if choix == 1:
                payload = ObjetReseau.conversion_string_to_byte("1")
                self.socket.send(payload)
                liste_des_courriels = self.socket.recv(1024).decode()
                print(liste_des_courriels)
                print("Quel courriel souhaitez-vous consulter?")
                choix_courriel = input()
                payload = ObjetReseau.conversion_string_to_byte(choix_courriel)
                self.socket.send(payload)
                courriel = self.socket.recv(1024).decode('utf-8')
                print(courriel)

            if choix == 2:
                payload = ObjetReseau.conversion_string_to_byte("2")
                self.socket.send(payload)
                info_courriel = recuperer_info_courriels()
                payload = ObjetReseau.conversion_string_to_byte(info_courriel)  # envoi des infos du courriels
                self.socket.send(payload)
                reponse_serveur = self.socket.recv(1024).decode()
                print(reponse_serveur)


            if choix == 3:
                payload = ObjetReseau.conversion_string_to_byte("3")
                self.socket.send(payload)
                print(self.read(4096).decode())
            if choix == 4:
                payload = ObjetReseau.conversion_string_to_byte("4")
                self.socket.send(payload)
                quitter = True

def recuperer_info_courriels():
    print("Entrez l'adresse du destinataire : ")
    destinataire = input()
    print("Entrez le sujet : ")
    sujet = input()
    print("Entrez le corps de votre courriel : ")
    corps = input()
    return destinataire + '/' + sujet + '/' + corps


def choix_de_laction():
    print("Menu de connexion")
    print("1. Créer un compte")
    print("2. Se connecter")
    choix = input()
    return choix


if __name__ == "__main__":

    action = int(choix_de_laction())
    if action == 1:
        client = Client("127.0.0.1", 1400)
        client.execution_client_courriel("creation")

    if action == 2:
        client = Client("127.0.0.1", 1400)
        client.execution_client_courriel("connexion")
