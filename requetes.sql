-- ============================================================
-- Projet ALSI61 - Gestion d'un système de versions de jeux vidéo esport
-- requetes.sql : Les 15 requêtes SQL
-- ============================================================

USE esport_versions;

-- ============================================================
-- 7.1 Requêtes de base
-- ============================================================

-- R1 : Liste de tous les joueurs triés par ordre alphabétique de pseudo
-- On affiche l'entité principale (joueur) triée alphabétiquement
SELECT id_joueur, pseudo, nom_reel, nationalite, role
FROM joueur
ORDER BY pseudo ASC;

-- R2 : Joueurs dont la date de naissance est avant 1997 (joueurs âgés)
-- Critère numérique/date sur un attribut de l'entité principale
SELECT pseudo, nom_reel, nationalite, date_naissance
FROM joueur
WHERE date_naissance < '1997-01-01'
ORDER BY date_naissance ASC;

-- R3 : Tous les patchs d'un jeu donné (ici id_jeu = 1 pour League of Legends)
-- Enregistrements liés à un identifiant passé en paramètre
SELECT p.id_patch, p.numero, p.date_sortie, p.notes
FROM patch p
WHERE p.id_jeu = 1
ORDER BY p.date_sortie ASC;

-- ============================================================
-- 7.2 Requêtes avec jointures
-- ============================================================

-- R4 : Informations combinées des joueurs et de leur équipe (INNER JOIN)
-- Seuls les joueurs ayant une équipe sont affichés
SELECT j.pseudo, j.nom_reel, j.role, e.nom AS equipe, e.pays AS pays_equipe
FROM joueur j
INNER JOIN equipe e ON j.id_equipe = e.id_equipe
ORDER BY e.nom, j.pseudo;

-- R5 : Tous les joueurs, même ceux sans équipe (LEFT JOIN)
-- Les joueurs sans équipe apparaissent avec NULL pour les colonnes d'équipe
SELECT j.pseudo, j.nom_reel, j.role, e.nom AS equipe
FROM joueur j
LEFT JOIN equipe e ON j.id_equipe = e.id_equipe
ORDER BY j.pseudo;

-- R6 : Prize pool total par jeu avec le nom du jeu (JOIN + agrégat)
-- On combine la table tournoi et jeu pour obtenir le total des prize pools par jeu
SELECT jeu.nom AS jeu, COUNT(t.id_tournoi) AS nb_tournois, SUM(t.prize_pool) AS prize_pool_total
FROM tournoi t
INNER JOIN jeu ON t.id_jeu = jeu.id_jeu
GROUP BY jeu.id_jeu, jeu.nom
ORDER BY prize_pool_total DESC;

-- ============================================================
-- 7.3 Requêtes avec agrégats (GROUP BY, HAVING)
-- ============================================================

-- R7 : Nombre de joueurs par équipe, trié par ordre décroissant
SELECT e.nom AS equipe, COUNT(j.id_joueur) AS nb_joueurs
FROM equipe e
LEFT JOIN joueur j ON e.id_equipe = j.id_equipe
GROUP BY e.id_equipe, e.nom
ORDER BY nb_joueurs DESC;

-- R8 : Équipes ayant participé à plus de 2 tournois
-- Utilisation de HAVING pour filtrer sur un agrégat
SELECT e.nom AS equipe, COUNT(p.id_tournoi) AS nb_tournois
FROM equipe e
INNER JOIN participation p ON e.id_equipe = p.id_equipe
GROUP BY e.id_equipe, e.nom
HAVING COUNT(p.id_tournoi) > 2
ORDER BY nb_tournois DESC;

-- R9 : Durée moyenne des matchs par tournoi, uniquement si la moyenne dépasse 50 minutes
-- Filtre HAVING sur une moyenne calculée
SELECT t.nom AS tournoi, AVG(m.duree_minutes) AS duree_moyenne
FROM match_esport m
INNER JOIN tournoi t ON m.id_tournoi = t.id_tournoi
GROUP BY t.id_tournoi, t.nom
HAVING AVG(m.duree_minutes) > 50
ORDER BY duree_moyenne DESC;

-- R10 : Score maximum et minimum par tournoi
-- MAX et MIN d'un attribut numérique par groupe
SELECT t.nom AS tournoi,
       MAX(m.score_equipe1 + m.score_equipe2) AS score_total_max,
       MIN(m.score_equipe1 + m.score_equipe2) AS score_total_min
FROM match_esport m
INNER JOIN tournoi t ON m.id_tournoi = t.id_tournoi
GROUP BY t.id_tournoi, t.nom
ORDER BY t.nom;

-- ============================================================
-- 7.4 Requêtes avancées
-- ============================================================

-- R11 : Tournois dont le prize pool est supérieur à la moyenne globale des prize pools
-- Sous-requête scalaire pour calculer la moyenne globale
SELECT nom, lieu, prize_pool
FROM tournoi
WHERE prize_pool > (SELECT AVG(prize_pool) FROM tournoi)
ORDER BY prize_pool DESC;

-- R12 : Équipes qui ont gagné tous leurs matchs dans un tournoi
-- NOT EXISTS : il n'existe pas de match où l'équipe a perdu
-- On considère qu'une équipe gagne si son score est supérieur à l'adversaire
SELECT DISTINCT e.nom AS equipe, t.nom AS tournoi
FROM equipe e
INNER JOIN match_esport m ON (m.id_equipe1 = e.id_equipe OR m.id_equipe2 = e.id_equipe)
INNER JOIN tournoi t ON m.id_tournoi = t.id_tournoi
WHERE NOT EXISTS (
    SELECT 1 FROM match_esport m2
    WHERE m2.id_tournoi = m.id_tournoi
      AND (
            (m2.id_equipe1 = e.id_equipe AND m2.score_equipe1 < m2.score_equipe2)
         OR (m2.id_equipe2 = e.id_equipe AND m2.score_equipe2 < m2.score_equipe1)
      )
)
ORDER BY equipe, tournoi;

-- R13 : Classement des joueurs par équipe, avec départage sur le rôle puis le pseudo
-- ORDER BY multi-colonnes
SELECT e.nom AS equipe, j.pseudo, j.role, j.nationalite
FROM joueur j
INNER JOIN equipe e ON j.id_equipe = e.id_equipe
ORDER BY e.nom ASC, j.role ASC, j.pseudo ASC;

-- R14 : Équipes ayant participé à au moins 2 jeux différents via les tournois
-- Sous-requête avec COUNT DISTINCT sur les jeux des tournois
SELECT e.nom AS equipe, COUNT(DISTINCT t.id_jeu) AS nb_jeux_differents
FROM equipe e
INNER JOIN participation p ON e.id_equipe = p.id_equipe
INNER JOIN tournoi t ON p.id_tournoi = t.id_tournoi
GROUP BY e.id_equipe, e.nom
HAVING COUNT(DISTINCT t.id_jeu) >= 2
ORDER BY nb_jeux_differents DESC;

-- R15 : Pour chaque jeu, le tournoi avec le plus grand prize pool (égalités incluses)
-- On utilise une sous-requête pour trouver le max par jeu, puis on joint pour obtenir
-- tous les tournois à ce niveau (en cas d'égalité, tous sont affichés)
SELECT jeu.nom AS jeu, t.nom AS tournoi, t.prize_pool
FROM tournoi t
INNER JOIN jeu ON t.id_jeu = jeu.id_jeu
WHERE t.prize_pool = (
    SELECT MAX(t2.prize_pool)
    FROM tournoi t2
    WHERE t2.id_jeu = t.id_jeu
)
ORDER BY jeu.nom, t.prize_pool DESC;
