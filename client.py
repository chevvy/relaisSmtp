import smtplib
from email.mime.text import MIMEText


def envoi_courriel(expediteur, destinataire, sujet, text):
    print("Data : ")
    text = ""
    temp = input()
    while temp != ".":
        text += temp + "\n"
        temp = input()
    # creation d’un objet courriel avec MIMEText
    msg = MIMEText(text)
    msg["From"] = expediteur
    msg["To"] = destinataire
    msg["Subject"] = sujet
    # envoi du courriel grace au protocole SMTP et au serveur de l’universite Laval
    try:
        smtp_connection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)  # à changer pour le serveur
        smtp_connection.sendmail(expediteur, destinataire, msg.as_string())
        smtp_connection.quit()
        print("Message envoye")
    except:
        print("L’envoi n’a pas pu etre effectue. ")


def choix_de_laction():
    print("Menu de connexion")
    print("1. Creer un compte")
    print("2. Se connecter")
    choix = input()
    return choix


def courriel_test():
    envoi_courriel("sirpat@hotmail.com", "vincentcjobin@gmail.com")


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
