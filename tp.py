import pyodbc

# Connexion à la base de données
cnxn = (
    "Driver=ODBC Driver 17 for SQL Server;"
    "Server=DESKTOP-RVFAV39\\SQLEXPRESS;"
    "Database=SocieteT;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(cnxn)
curseur = conn.cursor()


# Exercice 1
#1.	Implémenter une fonction python qui permet d’afficher les informations sur tous les produits de la table Produits (10 points) 
def lire_produits():
    try:
        # Exécute la requête pour récupérer les informations sur tous les produits
        curseur.execute('SELECT nomproduits, prixunitaire FROM Produits;')

        # Récupère toutes les lignes du résultat
        lignes = curseur.fetchall()

        # Affiche les informations sur chaque produit
        for ligne in lignes:
            nom_produit, prix_unitaire = ligne
            print(f"Produit : {nom_produit}, Prix : {prix_unitaire}")

    except pyodbc.Error as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")


# Exercice 2
#2.	Implémenter une fonction python qui permet d’afficher les informations d’un produit spécifique à partir du saisie d’un utilisateur (idProduit) (10 points) 
def afficher_info_produit():
    try:
        # Demande à l'utilisateur l'ID du produit à afficher
        id_produit = input("Entrez l'ID du produit : ")

        # Exécute la requête pour récupérer les informations sur le produit spécifié par l'utilisateur
        query = 'SELECT nomproduits, prixunitaire FROM Produits WHERE idproduits = ?;'
        curseur.execute(query, id_produit)

        # Récupère le produit (une seule ligne)
        produit = curseur.fetchone()

        # Affiche les informations du produit ou un message si aucun produit trouvé
        if produit:
            nom_produit, prix_unitaire = produit
            print(f"Informations sur le produit {id_produit}:")
            print(f"Nom : {nom_produit}, Prix : {prix_unitaire}")
        else:
            print("Aucun produit trouvé avec cet ID.")

    except pyodbc.Error as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")


# Exercice 3
#3.	Implémenter une fonction python qui permet d’insérer les informations d’un produit à partir du saisie d’un utilisateur (le nom et le prix unitaire) (10 points) 
def inserer_produit():
    try:
        # Demande à l'utilisateur les informations du produit à insérer
        nom_produit = input("Entrez le nom du produit : ")
        prix_unitaire = float(input("Entrez le prix unitaire du produit : "))

        # Exécute la requête pour insérer le nouveau produit
        query = 'INSERT INTO Produits (nomproduits, prixunitaire) VALUES (?, ?);'
        curseur.execute(query, nom_produit, prix_unitaire)
        conn.commit()

        print("Produit inséré avec succès !")

    except pyodbc.Error as e:
        # En cas d'erreur, annule la transaction et affiche un message d'erreur
        conn.rollback()
        print(f"Erreur lors de l'insertion du produit : {e}")


# Exercice 4
#4.	Implémenter une fonction python qui permet de modifier le prix unitaire d’un produit à partir du saisie d’un utilisateur (idProduit) (10 points) 
def modifier_prix_produit():
    try:
        # Demande à l'utilisateur l'ID du produit et le nouveau prix unitaire
        id_produit = input("Entrez l'ID du produit à modifier : ")
        nouveau_prix_unitaire = float(input("Entrez le nouveau prix unitaire du produit : "))

        # Exécute la requête pour mettre à jour le prix du produit
        query = 'UPDATE Produits SET prixunitaire = ? WHERE idproduits = ?;'
        curseur.execute(query, nouveau_prix_unitaire, id_produit)
        conn.commit()

        # Vérifie si des lignes ont été modifiées (produit trouvé)
        if curseur.rowcount > 0:
            print(f"Prix du produit {id_produit} mis à jour avec succès !")
        else:
            print(f"Aucun produit trouvé avec l'ID {id_produit}. Aucune modification effectuée.")

    except pyodbc.Error as e:
        # En cas d'erreur, annule la transaction et affiche un message d'erreur
        conn.rollback()
        print(f"Erreur lors de la modification du prix du produit : {e}")


# Exercice 5
#5.	Implémenter une fonction python qui permet de modifier le nom d’un produit à partir du saisie d’un utilisateur (le id) (10 points) 
def modifier_nom_produit():
    try:
        # Demande à l'utilisateur l'ID du produit et le nouveau nom
        id_produit = input("Entrez l'ID du produit à modifier : ")
        nouveau_nom = input("Entrez le nouveau nom du produit : ")

        # Exécute la requête pour mettre à jour le nom du produit
        query = 'UPDATE Produits SET nomproduits = ? WHERE idproduits = ?;'
        curseur.execute(query, nouveau_nom, id_produit)
        conn.commit()

        # Vérifie si des lignes ont été modifiées (produit trouvé)
        if curseur.rowcount > 0:
            print(f"Nom du produit {id_produit} mis à jour avec succès !")
        else:
            print(f"Aucun produit trouvé avec l'ID {id_produit}. Aucune modification effectuée.")

    except pyodbc.Error as e:
        # En cas d'erreur, annule la transaction et affiche un message d'erreur
        conn.rollback()
        print(f"Erreur lors de la modification du nom du produit : {e}")


# Exercice 6
#6.	Implémenter une fonction python qui permet de supprimer un produit à partir du saisie d’un utilisateur (le nom ou le id) (10 points) 
def supprimer_produit():
    try:
        # Demande à l'utilisateur de choisir entre supprimer par nom ou par ID
        choix = input("Voulez-vous supprimer par nom (N) ou par ID (I) ? ").upper()

        # En fonction du choix de l'utilisateur, exécute la requête de suppression
        if choix == 'N':
            nom_produit = input("Entrez le nom du produit à supprimer : ")
            query = 'DELETE FROM Produits WHERE nomproduits = ?;'
            params = (nom_produit,)
        elif choix == 'I':
            id_produit = input("Entrez l'ID du produit à supprimer : ")
            query = 'DELETE FROM Produits WHERE idproduits = ?;'
            params = (id_produit,)
        else:
            print("Choix invalide. Veuillez choisir 'N' pour le nom ou 'I' pour l'ID.")
            return

        curseur.execute(query, params)
        conn.commit()

        # Vérifie si des lignes ont été supprimées (produit trouvé)
        if curseur.rowcount > 0:
            print("Produit supprimé avec succès !")
        else:
            print("Aucun produit trouvé. Aucune suppression effectuée.")

    except pyodbc.Error as e:
        # En cas d'erreur, annule la transaction et affiche un message d'erreur
        conn.rollback()
        print(f"Erreur lors de la suppression du produit : {e}")


# Exercice 7
#7.	Implémenter un menu avec python pour faire appel aux différentes fonctions et faire le contrôle de saisie adéquat (40 points) 
def afficher_menu():
    print("----- MENU -----")
    print("1. Afficher la liste de tous les produits")
    print("2. Afficher un produit par son ID")
    print("3. Ajouter un produit")
    print("4. Modifier le prix unitaire d'un produit par son ID")
    print("5. Modifier le nom d'un produit par son ID")
    print("6. Supprimer un produit")
    print("0. Quitter le programme")


def execute_option(option):
    if option == '1':
        lire_produits()
    elif option == '2':
        afficher_info_produit()
    elif option == '3':
        inserer_produit()
    elif option == '4':
        modifier_prix_produit()
    elif option == '5':
        modifier_nom_produit()
    elif option == '6':
        supprimer_produit()
    elif option == '0':
        print("Au revoir !")
    else:
        print("Choix invalide. Veuillez choisir une option valide.")


# Boucle principale du programme
while True:
    afficher_menu()
    choix = input("Entrez votre choix (0-6) : ")

    # Si l'utilisateur choisit de quitter, termine la boucle
    if choix == '0':
        break

    # Exécute l'option choisie par l'utilisateur
    execute_option(choix)

# Fermeture du curseur et de la connexion à la base de données à la fin du programme
curseur.close()
conn.close()

