import re


def choix_de_laction():
    print("Menu de connexion")
    print("1. Creer un compte")
    print("2. Se connecter")
    choix = input()
    return choix


def nouveau_compte():
    print("Menu creation de compte")
    choix = input()


def connection_utilisateur():
    print("Connexion de l'utilisateur")
    choix = input()


def menu_principal():
    quitter = False
    while (not quitter):
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


if __name__ == "__main__":
    action = int(choix_de_laction())
    if action == 1:
        nouveau_compte()
    if action == 2:
        connection_utilisateur()
