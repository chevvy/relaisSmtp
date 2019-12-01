import smtplib, re, socket, optparse, sys
import re
import os
from hashlib import sha256
from email.mime.text import MIMEText




def initialisation_serveur():
    # choisissez le port avec l’option -p
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", action="store", dest="port", type=int, default=1400)
    port = parser.parse_args(sys.argv[1:])[0].port
    # creation d’un socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(("localhost", port))

    # demarre le socket
    serversocket.listen(5)
    print("Listening on port " + str(serversocket.getsockname()[1]))
    i=0
    while True:
        # un client se connecte au serveur
        # s est un nouveau socket pour interagir avec le client
        (s, address) = serversocket.accept()
        # affichage du nombre de connection au serveur
        i += 1
        print(str(i) + "e connexion au serveur")
        # message de bienvenue
        msg = "Bienvenue sur le serveur fkn chill de Léo, Cathou et Vincent. \nA qui dois-je envoyer un courriel? "
        s.send(msg.encode())
        # reception du courriel et verification qu’il est valide
        email_address = s.recv(1024).decode()
        while not re.search(r"^[^@]+@[^@]+\.[^@]+$", email_address):
            msg = "Saisissez une adresse courriel valide : "
            s.send(msg.encode())
            email_address = s.recv(1024).decode()

        # creation du courriel
        courriel = MIMEText("Ce courriel a ete envoye par mon serveur de courriel")
        courriel["From"] = "exercice3@glo2000.ca"
        courriel["To"] = email_address
        courriel["Subject"] = "Exercice3"

        # envoi du courriel
        try:
            smtp_connection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
            smtp_connection.sendmail(courriel["From"], courriel["To"], courriel.as_string())
            smtp_connection.quit()
            msg = "Le courriel a bien ete envoye! "
            s.send(msg.encode())
        except:
            msg = "L’envoi n’a pas pu etre effectué. "
            s.send(msg.encode())

        msg = "Au revoir!\n"
        s.send(msg.encode())
        s.close()

def liste_courriels(utilisateur):
    (_, _, courriels) = next(os.walk(os.getcwd() + "/" + utilisateur))
    courriels.remove("config.txt")
    return courriels

def formater_courriels(courriels):
    courriels_formates = ""
    compte = 1
    for courriel in courriels:
        courriels_formates += str(compte) + ". " + courriel[:-4] + "\n"
        compte += 1
    return courriels_formates

def lire_courriel(utilisateur, index):
    f = open(utilisateur + "/" + liste_courriels(utilisateur)[index])
    out = f.read()
    f.close()
    return out

def liste_utilisateurs():
    (_, utilisateurs, _) = next(os.walk(os.getcwd()))
    return utilisateurs

def mdp_est_conforme(mdp):
    if re.search(r"\s", mdp):
        return False, "Le mot de passe ne doit pas contenir d'espace ou de tabulation."
    if not re.search(r"(\S){6}", mdp) or re.search(r"(\S){13}", mdp):
        return False, "Le mot de passe doit contenir entre 6 et 12 caractères."
    if not re.search(r"\S*\d\S*\d\S*", mdp):
        return False, "Le mot de passe doit contenir au moins deux chiffres."
    if not re.search(r"[A-Z]", mdp):
        return False, "Le mot de passe doit contenir au moins une lettre majuscule."
    if not re.search(r"[a-z]", mdp):
        return False, "Le mot de passe doit contenir au moins une lettre minuscule."
    return True, ""


def verifier_validite_nouveau_compte(nom_utilisateur, mot_de_passe):
    if nom_utilisateur not in liste_utilisateurs():
        mdp_valide = (mdp_est_conforme(mot_de_passe))[0]
        if mdp_valide:
            mot_de_passe_hache = sha256(mot_de_passe.encode()).hexdigest()
            os.makedirs(os.getcwd() + '/' + nom_utilisateur)
            path_fichier_config = os.path.join(os.getcwd() + '/' + nom_utilisateur + '/' + 'config.txt')
            fichier_config = open(path_fichier_config, "w")
            fichier_config.write(mot_de_passe_hache)
            fichier_config.close()
            return "Connexion acceptée et le compte a été créé"
        else:
            stringRetour = (mdp_est_conforme(mot_de_passe))[1]
            return "Connexion échouée :" + stringRetour


def verifier_validite_compte_existant(nom_utilisateur, mot_de_passe):
    if nom_utilisateur in liste_utilisateurs():
        mot_de_passe_hache = sha256(mot_de_passe.encode()).hexdigest()
        with open(os.getcwd() + '/' + nom_utilisateur + '/' + 'config.txt') as f:
            mot_de_passe_client = f.readline()
        if mot_de_passe_client is not None:
            if mot_de_passe_client == mot_de_passe_hache:
                return "Connexion acceptée"
            else:
                return "Connexion échouée : Le mot de passe ne correspond pas"
    else:
        return "Connexion échouée : Le nom d'usager n'existe pas"


def statistiques(utilisateur):
    courriels = liste_courriels(utilisateur)
    out = "Votre dossier contient " + str(len(courriels)) + " courriels.\n"
    taille = sum(os.path.getsize(utilisateur + "/" + f) for f in os.listdir(os.getcwd() + "/" + utilisateur))
    out += "Votre dossier pèse " + str(taille) + " octets.\n"
    out += "Liste des courriels : \n\n" + formater_courriels(courriels)
    return out


if __name__ == "__main__":
    print(lire_courriel("XxX_L3OK1LL3R_XxX", 1))
    initialisation_serveur()
