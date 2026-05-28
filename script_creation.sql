-- ============================================================
-- Projet ALSI61 - Gestion d'un système de versions de jeux vidéo esport
-- script_creation.sql : DDL + DML
-- ============================================================

CREATE DATABASE IF NOT EXISTS esport_versions;
USE esport_versions;

-- Suppression des tables dans l'ordre inverse des dépendances
DROP TABLE IF EXISTS patch_tournoi;
DROP TABLE IF EXISTS participation;
DROP TABLE IF EXISTS match_esport;
DROP TABLE IF EXISTS tournoi;
DROP TABLE IF EXISTS joueur;
DROP TABLE IF EXISTS patch;
DROP TABLE IF EXISTS jeu;
DROP TABLE IF EXISTS editeur;
DROP TABLE IF EXISTS equipe;

-- ============================================================
-- DDL
-- ============================================================

CREATE TABLE editeur (
    id_editeur INT PRIMARY KEY AUTO_INCREMENT,
    nom        VARCHAR(100) NOT NULL,
    pays       VARCHAR(50)  NOT NULL,
    site_web   VARCHAR(200)
);

CREATE TABLE jeu (
    id_jeu     INT PRIMARY KEY AUTO_INCREMENT,
    nom        VARCHAR(100) NOT NULL,
    genre      VARCHAR(50)  NOT NULL CHECK (genre IN ('FPS','MOBA','Battle Royale','RTS','Fighting')),
    date_sortie DATE         NOT NULL,
    id_editeur INT          NOT NULL,
    FOREIGN KEY (id_editeur) REFERENCES editeur(id_editeur)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE patch (
    id_patch    INT PRIMARY KEY AUTO_INCREMENT,
    numero      VARCHAR(20)  NOT NULL,
    date_sortie DATE         NOT NULL,
    notes       TEXT,
    id_jeu      INT          NOT NULL,
    FOREIGN KEY (id_jeu) REFERENCES jeu(id_jeu)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE equipe (
    id_equipe  INT PRIMARY KEY AUTO_INCREMENT,
    nom        VARCHAR(100) NOT NULL UNIQUE,
    pays       VARCHAR(50)  NOT NULL,
    date_creation DATE      NOT NULL
);

CREATE TABLE joueur (
    id_joueur  INT PRIMARY KEY AUTO_INCREMENT,
    pseudo     VARCHAR(50)  NOT NULL UNIQUE,
    nom_reel   VARCHAR(100) NOT NULL,
    nationalite VARCHAR(50) NOT NULL,
    date_naissance DATE     NOT NULL,
    role       VARCHAR(50)  NOT NULL,
    id_equipe  INT,
    FOREIGN KEY (id_equipe) REFERENCES equipe(id_equipe)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE tournoi (
    id_tournoi INT PRIMARY KEY AUTO_INCREMENT,
    nom        VARCHAR(150) NOT NULL,
    lieu       VARCHAR(100) NOT NULL,
    date_debut DATE         NOT NULL,
    date_fin   DATE         NOT NULL,
    prize_pool DECIMAL(12,2) NOT NULL CHECK (prize_pool >= 0),
    id_jeu     INT          NOT NULL,
    FOREIGN KEY (id_jeu) REFERENCES jeu(id_jeu)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Association ternaire : un match oppose deux équipes sur un patch donné
CREATE TABLE match_esport (
    id_match      INT PRIMARY KEY AUTO_INCREMENT,
    date_match    DATE         NOT NULL,
    duree_minutes INT          NOT NULL CHECK (duree_minutes > 0),
    score_equipe1 INT          NOT NULL DEFAULT 0,
    score_equipe2 INT          NOT NULL DEFAULT 0,
    id_equipe1    INT          NOT NULL,
    id_equipe2    INT          NOT NULL,
    id_patch      INT          NOT NULL,
    id_tournoi    INT          NOT NULL,
    FOREIGN KEY (id_equipe1)  REFERENCES equipe(id_equipe)   ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_equipe2)  REFERENCES equipe(id_equipe)   ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_patch)    REFERENCES patch(id_patch)     ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tournoi)  REFERENCES tournoi(id_tournoi) ON DELETE CASCADE  ON UPDATE CASCADE
);

-- Table de participation : équipes inscrites à un tournoi (association porteuse d'attribut)
CREATE TABLE participation (
    id_equipe  INT  NOT NULL,
    id_tournoi INT  NOT NULL,
    date_inscription DATE NOT NULL,
    statut     VARCHAR(20) NOT NULL DEFAULT 'inscrit' CHECK (statut IN ('inscrit','eliminé','vainqueur')),
    PRIMARY KEY (id_equipe, id_tournoi),
    FOREIGN KEY (id_equipe)  REFERENCES equipe(id_equipe)   ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tournoi) REFERENCES tournoi(id_tournoi) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Association ternaire entre patch et tournoi : indique quel patch est utilisé dans quel tournoi
CREATE TABLE patch_tournoi (
    id_patch   INT NOT NULL,
    id_tournoi INT NOT NULL,
    obligatoire TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (id_patch, id_tournoi),
    FOREIGN KEY (id_patch)   REFERENCES patch(id_patch)     ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tournoi) REFERENCES tournoi(id_tournoi) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- DML - Jeu de données
-- ============================================================

INSERT INTO editeur (nom, pays, site_web) VALUES
('Riot Games',    'USA',         'https://www.riotgames.com'),
('Valve',         'USA',         'https://www.valvesoftware.com'),
('Blizzard',      'USA',         'https://www.blizzard.com'),
('Activision',    'USA',         'https://www.activision.com'),
('Nexon',         'Corée du Sud','https://www.nexon.com');

INSERT INTO jeu (nom, genre, date_sortie, id_editeur) VALUES
('League of Legends', 'MOBA',        '2009-10-27', 1),
('Valorant',          'FPS',         '2020-06-02', 1),
('Counter-Strike 2',  'FPS',         '2023-09-27', 2),
('Overwatch 2',       'FPS',         '2022-10-04', 3),
('StarCraft II',      'RTS',         '2010-07-27', 3);

INSERT INTO patch (numero, date_sortie, notes, id_jeu) VALUES
('14.1',  '2024-01-10', 'Rééquilibrage ADC',        1),
('14.2',  '2024-01-24', 'Nerf jungle',              1),
('14.3',  '2024-02-07', 'Buff support',             1),
('8.0',   '2024-01-09', 'Nouveau agent Iso',        2),
('8.04',  '2024-02-13', 'Corrections de bugs',      2),
('1.4',   '2024-01-15', 'Ajout nouvelle map',       3),
('1.5',   '2024-02-20', 'Rééquilibrage armes',      3),
('2.0',   '2023-12-01', 'Saison 4 début',           4),
('5.11',  '2024-01-30', 'Patch équilibre LoTV',     5);

INSERT INTO equipe (nom, pays, date_creation) VALUES
('T1',            'Corée du Sud', '2012-02-14'),
('Cloud9',        'USA',          '2012-08-16'),
('G2 Esports',    'Europe',       '2014-07-16'),
('Fnatic',        'Europe',       '2004-07-23'),
('NaVi',          'Ukraine',      '2009-12-29'),
('Team Liquid',   'USA',          '2000-01-01'),
('Evil Geniuses', 'USA',          '1999-07-01'),
('100 Thieves',   'USA',          '2017-10-25');

INSERT INTO joueur (pseudo, nom_reel, nationalite, date_naissance, role, id_equipe) VALUES
('Faker',    'Lee Sang-hyeok',  'Coréen',   '1996-05-07', 'Mid',     1),
('Gumayusi', 'Lee Min-hyeong',  'Coréen',   '2000-07-19', 'ADC',     1),
('Ruler',    'Park Jae-hyuk',   'Coréen',   '1998-02-09', 'ADC',     2),
('jdm64',    'Joshua Merry',    'Américain','1996-10-26', 'Support', 2),
('NiKo',     'Nikola Kovac',    'Bosnien',  '1997-02-16', 'Rifler',  3),
('Hunter',   'Hunter Mira',     'Bosnien',  '1999-11-23', 'Rifler',  3),
('s1mple',   'Oleksandr Kostyliev','Ukrainien','1997-10-02','AWPer', 5),
('electronic','Denis Sharipov', 'Russe',    '1998-01-19', 'Rifler',  5),
('cadiaN',   'Casper Nielsen',  'Danois',   '1993-10-30', 'IGL',     4),
('mezii',    'William Merriman','Britannique','1999-08-19','Rifler', 4),
('shox',     'Richard Papillon','Français', '1992-02-12', 'Rifler',  NULL),
('kennyS',   'Kenny Schrub',    'Français', '1995-09-19', 'AWPer',   NULL);

INSERT INTO tournoi (nom, lieu, date_debut, date_fin, prize_pool, id_jeu) VALUES
('Worlds 2024',               'Corée du Sud', '2024-09-25','2024-11-02', 2250000.00, 1),
('LEC Spring 2024',           'Berlin',       '2024-01-13','2024-04-14',  200000.00, 1),
('VCT Masters Madrid',        'Madrid',       '2024-03-11','2024-03-24',  500000.00, 2),
('IEM Katowice 2024',         'Katowice',     '2024-01-31','2024-02-11', 1000000.00, 3),
('ESL Pro League S19',        'Malte',        '2024-03-20','2024-04-07',  850000.00, 3),
('Overwatch League 2024',     'Los Angeles',  '2024-02-01','2024-06-30',  750000.00, 4);

INSERT INTO participation (id_equipe, id_tournoi, date_inscription, statut) VALUES
(1, 1, '2024-09-01', 'vainqueur'),
(2, 1, '2024-09-01', 'eliminé'),
(3, 1, '2024-09-01', 'eliminé'),
(4, 1, '2024-09-01', 'eliminé'),
(1, 2, '2024-01-05', 'eliminé'),
(2, 2, '2024-01-05', 'vainqueur'),
(3, 3, '2024-03-01', 'vainqueur'),
(4, 3, '2024-03-01', 'eliminé'),
(5, 4, '2024-01-15', 'vainqueur'),
(6, 4, '2024-01-15', 'eliminé'),
(5, 5, '2024-03-10', 'eliminé'),
(7, 5, '2024-03-10', 'vainqueur'),
(6, 5, '2024-03-10', 'eliminé'),
(8, 2, '2024-01-05', 'eliminé');

INSERT INTO patch_tournoi (id_patch, id_tournoi, obligatoire) VALUES
(3, 1, 1),
(2, 1, 0),
(1, 2, 1),
(2, 2, 1),
(4, 3, 1),
(5, 3, 0),
(6, 4, 1),
(7, 5, 1),
(8, 6, 1);

-- Association ternaire match_esport : équipe1 vs équipe2, sur un patch, dans un tournoi
INSERT INTO match_esport (date_match, duree_minutes, score_equipe1, score_equipe2, id_equipe1, id_equipe2, id_patch, id_tournoi) VALUES
('2024-09-26', 45, 2, 0, 1, 2, 3, 1),
('2024-09-27', 60, 1, 2, 3, 4, 3, 1),
('2024-09-30', 52, 2, 1, 1, 3, 3, 1),
('2024-01-14', 38, 2, 0, 1, 8, 1, 2),
('2024-01-15', 42, 2, 1, 2, 8, 2, 2),
('2024-03-12', 55, 1, 2, 3, 4, 4, 3),
('2024-03-13', 48, 2, 0, 3, 4, 4, 3),
('2024-02-01', 90, 2, 1, 5, 6, 6, 4),
('2024-02-03', 85, 0, 2, 5, 6, 6, 4),
('2024-03-21', 70, 2, 0, 7, 5, 7, 5);
