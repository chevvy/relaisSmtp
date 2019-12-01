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

    def read(self):
        """ Lit la réponse envoyé sur le socket """
        return self.socket.recv(1024)

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
        ObjetReseau.__init__(self, p_ip, p_port)

    def execution_client_courriel(self, type_execution):
        info_connexion_serveur = (self.ip, self.port)
        self.socket.connect(info_connexion_serveur)
        # reception et assignation des clées
        self.socket.send(self.conversion_string_to_byte(type_execution))
        if type_execution == "creation":
            login_info = nouveau_compte()

        if type_execution == "connexion":
            login_info = connection_utilisateur()

        # recepetion et assignation de la base

        self.socket.close()


def envoi_courriel(expediteur, destinataire, sujet, text):
    print("Data : ")


def choix_de_laction():
    print("Menu de connexion")
    print("1. Créer un compte")
    print("2. Se connecter")
    choix = input()
    return choix


def courriel_test():
    envoi_courriel("sirpat@hotmail.com", "vincentcjobin@gmail.com")


def nouveau_compte():
    print("Menu creation de compte")
    print("Entrez un nom d'usager")
    nom_usager = input()
    print("Entrez un mot de passe")
    mot_de_passe = input()
    return nom_usager, mot_de_passe

    ##creationValide = verifierValiditeNouveauCompte(nomUsager, motDePasse)


def connection_utilisateur():
    print("Connexion de l'utilisateur")
    print("Entrez votre nom d'usager")
    nom_usager = input()
    print("Entrez votre mot de passe")
    mot_de_passe = input()

    return nom_usager, mot_de_passe
    ##connectionValide = verifierValiditeCompteExistant(nomUsager, motDePasse)


def menu_principal():
    quitter = False
    while not quitter:
        print("Menu principal")
        print("1. Consultation de courriels")
        print("2. Envoi de courriels")
        print("3. Statistiques")
        print("4. Quitter")
        choix = input()
        if choix == 1:
            pass
        if choix == 2:
            pass
        if choix == 3:
            pass
        if choix == 4:
            quitter = True


if __name__ == "__main__":

    action = int(choix_de_laction())
    if action == 1:
        client = Client("127.0.0.1", 1400)
        client.execution_client_courriel("creation")

    if action == 2:
        client = Client("127.0.0.1", 1400)
        client.execution_client_courriel("connexion")

