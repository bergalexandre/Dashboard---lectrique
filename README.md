# description
Script qui génère un rapport latex automatiquement. 


# requis PC pour fonctionner
Les requis logiciel sont python 3.7 et plus. Voici les librairies requise:

Pour python:
 - py -m pip install openpyxl
 - py -m pip install matplotlib
 - py -m pip install numpy
 - py -m pip install panda

Pour votre OS:
 - Python 3.7 et + (prenez dont la dernière version tant qu'à y être)
 - Git dernière version dans la variable path fonctionnel

Pour votre compte Overleaf:
 - Créez vous un compte github
 - Allez dans vos setting pis linker le compte github
 - Si vous avez une authentification overleaf externe, faîte reset votre password overleaf pis setter en un
 - récupération du rapport:
    - info: git clone https://git.overleaf.com/60dbafb3c22aac53e265b6e6
    - elec: git clone https://git.overleaf.com/60dbafb3c22aac53e265b6e6
    - mec: git clone https://git.overleaf.com/60dbafb3c22aac53e265b6e6
 - Git va vous demander le mot de passe et nom du compte.
 - si c'est pas clair, [doc officiel](https://www.overleaf.com/learn/how-to/How_do_I_connect_an_Overleaf_project_with_a_repo_on_GitHub,_GitLab_or_BitBucket%3F)



# Générer le rapport de la semaine
1. Va dans le repo git overleaf de ton pc
2. tape cmd dans la barre d'exploration (ou autre si tu préfère un autre bash, I don't care)
3. Rouler la commande py genereRapport.py
