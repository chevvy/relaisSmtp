import smtplib, re, socket, optparse, sys
import re
import os
from hashlib import sha256
from email.mime.text import MIMEText


def conversion_byte_to_string(byte_a_convertir, encodage="utf-8"):
    """
    Converti un byte reçu en argument vers un string et le retourne
    :param encodage: l'encodage (par défaut UTF-8)
    :param byte_a_convertir: un string de character ou chiffre
    :return: string: le string converti
    """
    string_converti = byte_a_convertir.decode(encodage)
    return string_converti


def conversion_string_to_byte(element_a_convertir, encodage="utf-8"):
    """
    Converti un string en byte, encoder dans un encodage spécifique (par défaut = UTF-8)
    :param encodage:
    :param element_a_convertir:
    :return:
    """
    string = str(element_a_convertir)
    return str.encode(string, encodage)


def initialisation_serveur():
    # choisissez le port avec l’option -p
    global validation
    utilisateur_courant = None
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
    i = 0
    while True:
        # un client se connecte au serveur
        # s est un nouveau socket pour interagir avec le client
        (s, address) = serversocket.accept()
        utilisateur_valide_connecte = False
        # affichage du nombre de connection au serveur
        i += 1
        print(str(i) + "e connexion au serveur")

        # Reception des logins
        mode_action = s.recv(1024).decode()
        print(mode_action)

        # TODO vérification de la validité des login des utilisateurs
        login_info = s.recv(1024).decode()
        print(login_info)
        user_et_mdp = login_info.split(" ")
        print(user_et_mdp)
        if mode_action == "creation":
            validation = verifier_validite_nouveau_compte(user_et_mdp[0], user_et_mdp[1])

        if mode_action == "connexion":
            validation = verifier_validite_compte_existant(user_et_mdp[0], user_et_mdp[1])

        s.send(conversion_string_to_byte(str(validation[0]) + '/' + validation[1]))  # envoi de la validation

        if validation[0]:  # utilisateur connecté
            utilisateur_courant = user_et_mdp[0]
            choix_user = 0
            while choix_user != 4:
                choix_user = s.recv(1024).decode()  # recepetion du choix de l'utilisateur
                if choix_user != '':
                    choix_user = int(choix_user)
                    if choix_user == 1:
                        liste_des_courriels = (formater_courriels(liste_courriels(utilisateur_courant)))
                        s.send(conversion_string_to_byte(liste_des_courriels))  # envoi liste des courriels
                        courriel_desire = s.recv(1024).decode()  # choix de l'utilisateur pour le courriel
                        courriel = lire_courriel(utilisateur_courant, int(courriel_desire))
                        s.send(conversion_string_to_byte(courriel))
                    if choix_user == 2:
                        info_courriel = s.recv(1024).decode()
                        info_courriel = info_courriel.split('/')
                        courriel = creation_du_courriel(utilisateur_courant, info_courriel)
                        envoie_du_courriel(courriel, s, utilisateur_courant)


                    if choix_user == 3:
                        stats = statistiques(utilisateur_courant)
                        s.send(conversion_string_to_byte(stats))

        utilisateur_courant = None  # retire l'utilisateur courant


def creation_du_courriel(utilisateur, info_courriel):

    courriel = MIMEText(info_courriel[0])
    courriel["From"] = utilisateur + "@superfuntimes.com"
    courriel["To"] = info_courriel[1]
    courriel["Subject"] = info_courriel[2]
    return courriel

def envoie_du_courriel(courriel, sock, utilisateur):
    if utilisateur in liste_utilisateurs():
        # TODO faire un courriel local
        msg = "courriel local pas implémenté"
        sock.send(msg)
    else:
        try:
            smtp_connection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
            smtp_connection.sendmail(courriel["From"], courriel["To"], courriel.as_string())
            smtp_connection.quit()
            msg = "Le courriel a bien ete envoye! "
            sock.send(msg.encode())
        except:
            msg = "L’envoi n’a pas pu etre effectué. "
            sock.send(msg.encode())
            msg = "Au revoir!\n"
            sock.send(msg.encode())
            sock.close()


def liste_courriels(utilisateur):
    (_, _, courriels) = next(os.walk(os.getcwd() + "/" + utilisateur))
    courriels.remove("config.txt")
    return courriels


def formater_courriels(courriels):
    courriels_formates = ""
    compte = 0
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
    if re.search(r" ", mdp):
        return False, "Le mot de passe ne doit pas contenir d'espace."
    if not re.search(r".{6}", mdp) or re.search(r".{13}", mdp):
        return False, "Le mot de passe doit contenir entre 6 et 12 caractères."
    if not re.search(r".*\d.*\d.*", mdp):
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
            return True, "Connexion acceptée et le compte a été créé"
        else:
            string_retour = (mdp_est_conforme(mot_de_passe))[1]
            return False, "Connexion échouée :" + string_retour


def verifier_validite_compte_existant(nom_utilisateur, mot_de_passe):
    if nom_utilisateur == "":
        return False, "Connexion échouée : Le nom d'usager ne peut pas être vide"
    if nom_utilisateur in liste_utilisateurs():
        mot_de_passe_hache = sha256(mot_de_passe.encode()).hexdigest()
        with open(os.getcwd() + '/' + nom_utilisateur + '/' + 'config.txt') as f:
            mot_de_passe_client = f.readline()
        if mot_de_passe_client is not None:
            if mot_de_passe_client == mot_de_passe_hache:
                return True, "Connexion acceptée"
            else:
                return False, "Connexion échouée : Le mot de passe ne correspond pas"
    else:
        return False, "Connexion échouée : Le nom d'usager n'existe pas"


def statistiques(utilisateur):
    courriels = liste_courriels(utilisateur)
    out = "Votre dossier contient " + str(len(courriels)) + " courriels.\n"
    taille = sum(os.path.getsize(utilisateur + "/" + f) for f in os.listdir(os.getcwd() + "/" + utilisateur))
    out += "Votre dossier pèse " + str(taille) + " octets.\n"
    out += "Liste des courriels : \n\n" + formater_courriels(courriels)
    return out


if __name__ == "__main__":
    initialisation_serveur()
