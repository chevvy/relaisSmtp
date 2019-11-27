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


if __name__ == "__main__":
    action = int(choix_de_laction())
    if action == 1:
        nouveau_compte()
    if action == 2:
        connection_utilisateur()
