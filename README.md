======================================================
Projet ALSI61 - Bases de données INGE-1-APP-BDML
======================================================

DOMAINE CHOISI
--------------
Gestion d'un système de gestion de versions de jeux vidéo esport.
Ce domaine modélise des jeux vidéo compétitifs, leurs patchs (versions),
les équipes, les joueurs, les tournois et les matchs joués.

======================================================
RÈGLES MÉTIER
======================================================

1.  Un jeu appartient à un seul éditeur. Un éditeur peut publier plusieurs jeux.
2.  Un jeu peut avoir plusieurs patchs (versions). Un patch appartient à un seul jeu.
3.  Un joueur appartient à au plus une équipe à la fois (id_equipe peut être NULL).
4.  Un tournoi est organisé pour un seul jeu. Un jeu peut avoir plusieurs tournois.
5.  Un tournoi a un prize_pool positif ou nul.
6.  Une équipe peut participer à plusieurs tournois. Un tournoi accueille plusieurs équipes
    (association participation avec attributs : date_inscription et statut).
7.  Le statut d'une participation est l'un de : 'inscrit', 'eliminé', 'vainqueur'.
8.  Un match oppose exactement deux équipes distinctes, se joue dans un tournoi précis
    et sur un patch précis (association ternaire match_esport).
9.  Un tournoi peut utiliser plusieurs patchs. Un patch peut être utilisé dans plusieurs
    tournois (table patch_tournoi avec attribut obligatoire).
10. Le genre d'un jeu est l'un de : 'FPS', 'MOBA', 'Battle Royale', 'RTS', 'Fighting'.
11. La durée d'un match est strictement positive (CHECK duree_minutes > 0).
12. Le nom d'une équipe est unique.
13. Le pseudo d'un joueur est unique.

======================================================
DICTIONNAIRE DES DONNÉES
======================================================

Table        | Attribut         | Type SQL        | Contraintes             | Description
-------------|------------------|-----------------|-------------------------|----------------------------
editeur      | id_editeur       | INT             | PK, AUTO_INCREMENT      | Identifiant de l'éditeur
editeur      | nom              | VARCHAR(100)    | NOT NULL                | Nom de l'éditeur
editeur      | pays             | VARCHAR(50)     | NOT NULL                | Pays de l'éditeur
editeur      | site_web         | VARCHAR(200)    |                         | URL du site web
-------------|------------------|-----------------|-------------------------|----------------------------
jeu          | id_jeu           | INT             | PK, AUTO_INCREMENT      | Identifiant du jeu
jeu          | nom              | VARCHAR(100)    | NOT NULL                | Nom du jeu
jeu          | genre            | VARCHAR(50)     | NOT NULL, CHECK IN(...) | Genre du jeu
jeu          | date_sortie      | DATE            | NOT NULL                | Date de sortie commerciale
jeu          | id_editeur       | INT             | FK -> editeur           | Éditeur du jeu
-------------|------------------|-----------------|-------------------------|----------------------------
patch        | id_patch         | INT             | PK, AUTO_INCREMENT      | Identifiant du patch
patch        | numero           | VARCHAR(20)     | NOT NULL                | Numéro de version (ex: 14.1)
patch        | date_sortie      | DATE            | NOT NULL                | Date de sortie du patch
patch        | notes            | TEXT            |                         | Notes de patch (changelog)
patch        | id_jeu           | INT             | FK -> jeu, CASCADE DEL  | Jeu associé au patch
-------------|------------------|-----------------|-------------------------|----------------------------
equipe       | id_equipe        | INT             | PK, AUTO_INCREMENT      | Identifiant de l'équipe
equipe       | nom              | VARCHAR(100)    | NOT NULL, UNIQUE        | Nom de l'équipe
equipe       | pays             | VARCHAR(50)     | NOT NULL                | Pays de l'équipe
equipe       | date_creation    | DATE            | NOT NULL                | Date de création
-------------|------------------|-----------------|-------------------------|----------------------------
joueur       | id_joueur        | INT             | PK, AUTO_INCREMENT      | Identifiant du joueur
joueur       | pseudo           | VARCHAR(50)     | NOT NULL, UNIQUE        | Pseudo du joueur
joueur       | nom_reel         | VARCHAR(100)    | NOT NULL                | Nom réel du joueur
joueur       | nationalite      | VARCHAR(50)     | NOT NULL                | Nationalité du joueur
joueur       | date_naissance   | DATE            | NOT NULL                | Date de naissance
joueur       | role             | VARCHAR(50)     | NOT NULL                | Rôle en jeu (ex: ADC)
joueur       | id_equipe        | INT             | FK -> equipe, SET NULL  | Équipe actuelle (nullable)
-------------|------------------|-----------------|-------------------------|----------------------------
tournoi      | id_tournoi       | INT             | PK, AUTO_INCREMENT      | Identifiant du tournoi
tournoi      | nom              | VARCHAR(150)    | NOT NULL                | Nom du tournoi
tournoi      | lieu             | VARCHAR(100)    | NOT NULL                | Lieu du tournoi
tournoi      | date_debut       | DATE            | NOT NULL                | Date de début
tournoi      | date_fin         | DATE            | NOT NULL                | Date de fin
tournoi      | prize_pool       | DECIMAL(12,2)   | NOT NULL, CHECK >= 0    | Dotation en dollars
tournoi      | id_jeu           | INT             | FK -> jeu               | Jeu du tournoi
-------------|------------------|-----------------|-------------------------|----------------------------
match_esport | id_match         | INT             | PK, AUTO_INCREMENT      | Identifiant du match
match_esport | date_match       | DATE            | NOT NULL                | Date du match
match_esport | duree_minutes    | INT             | NOT NULL, CHECK > 0     | Durée du match
match_esport | score_equipe1    | INT             | NOT NULL, DEFAULT 0     | Score équipe 1
match_esport | score_equipe2    | INT             | NOT NULL, DEFAULT 0     | Score équipe 2
match_esport | id_equipe1       | INT             | FK -> equipe            | Première équipe
match_esport | id_equipe2       | INT             | FK -> equipe            | Deuxième équipe
match_esport | id_patch         | INT             | FK -> patch             | Patch utilisé
match_esport | id_tournoi       | INT             | FK -> tournoi, CASCADE  | Tournoi du match
-------------|------------------|-----------------|-------------------------|----------------------------
participation| id_equipe        | INT             | PK, FK -> equipe        | Équipe participante
participation| id_tournoi       | INT             | PK, FK -> tournoi       | Tournoi concerné
participation| date_inscription | DATE            | NOT NULL                | Date d'inscription
participation| statut           | VARCHAR(20)     | NOT NULL, CHECK IN(...) | Statut dans le tournoi
-------------|------------------|-----------------|-------------------------|----------------------------
patch_tournoi| id_patch         | INT             | PK, FK -> patch         | Patch concerné
patch_tournoi| id_tournoi       | INT             | PK, FK -> tournoi       | Tournoi concerné
patch_tournoi| obligatoire      | TINYINT(1)      | NOT NULL, DEFAULT 1     | Patch obligatoire (1/0)

======================================================
INSTRUCTIONS DE LANCEMENT
======================================================

Prérequis
---------
- MySQL 8.x (ou MySQL Workbench)
- Python 3.8+
- Bibliothèque mysql-connector-python

Étape 1 : Créer la base de données
-----------------------------------
Ouvrir MySQL Workbench et exécuter le fichier :
  script_creation.sql
(Ce script crée la base, les tables et insère les données.)

Étape 2 : Exécuter les requêtes
---------------------------------
Ouvrir dans MySQL Workbench :
  requetes.sql
(Exécuter les requêtes individuellement ou en bloc.)

Étape 3 : Lancer l'application Python
----------------------------------------
Installer le connecteur :
  pip install mysql-connector-python

Modifier si besoin les paramètres de connexion dans src/app.py :
  DB_CONFIG = { 'host': 'localhost', 'user': 'root', 'password': 'VOTRE_MOT_DE_PASSE', ... }

Lancer l'application :
  python src/app.py

======================================================
STRUCTURE DU DÉPÔT GITHUB
======================================================

ALSI-BDD_NOM1_NOM2_NOM3/
├── Livrable.pdf              <- Rapport (MCD, MLD, description, règles métier)
├── script_creation.sql       <- DDL + DML
├── requetes.sql              <- 15 requêtes SQL
├── src/
│   └── app_gui.py                <- Application console Python
└── README.txt                <- Ce fichier
