import re

def choix_de_laction():
    print("Menu de connexion")
    print("1. Creer un compte")
    print("2. Se connecter")
    choix = input()
    return choix

def nouveau_compte():
    print("Menu creation de compte")
    print("Entrez un nom d'usager")
    nomUsager = input()
    print("Entrez un mot de passe")
    motDePasse = input()
    ##valide = verifierValiditeNouveauCompte(nomUsager, motDePasse)


def connection_utilisateur():
    print("Connexion de l'utilisateur")
    print("Entrez votre nom d'usager")
    nomUsager = input()
    ##print("Entrez votre mot de passe")
    ##motDePasse = input()
    ##valide = verifierValiditeCompteExistant(nomUsager, motDePasse)
    ##if valide :





if __name__ == "__main__":
    action = int(choix_de_laction())
    if action == 1:
        nouveau_compte()

    if action == 2:
        connection_utilisateur()


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
    return True, "ok"