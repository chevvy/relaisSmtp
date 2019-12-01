import smtplib, re, socket, optparse, sys
import re
import os
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

##def verifierValiditeNouveauCompte():
