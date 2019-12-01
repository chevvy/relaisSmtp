import re
import getpass

def choix_de_laction():
    print("Menu de connexion")
    print("1. Creer un compte")
    print("2. Se connecter")
    choix = input()
    return choix

def nouveau_compte():
    print("Menu creation de compte")
    print("Entrez un nom d'usager")
    nom_usager = input()
    mdp_valide = False
    while not mdp_valide:
        print("Entrez un mot de passe")
        mot_de_passe = getpass.getpass(prompt='Mot de passe: ', stream=None)
        mdp_valide = (mdp_est_conforme(mot_de_passe))[0]
        if not mdp_valide:
            print((mdp_est_conforme(mot_de_passe))[1])

    ##creationValide = verifierValiditeNouveauCompte(nomUsager, motDePasse)


def connection_utilisateur():
    print("Connexion de l'utilisateur")
    print("Entrez votre nom d'usager")
    nom_usager = input()
    print("Entrez votre mot de passe")
    mot_de_passe = input()
    ##connectionValide = verifierValiditeCompteExistant(nomUsager, motDePasse)


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


if __name__ == "__main__":
    action = int(choix_de_laction())
    if action == 1:
        nouveau_compte()

    if action == 2:
        connection_utilisateur()
