import serveur
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

