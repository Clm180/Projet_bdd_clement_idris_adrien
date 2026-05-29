import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
 
# ============================================================
# Configuration de la connexion
# ============================================================
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'root',     # Modifier selon votre configuration
    'database': 'esport_versions'
}
 
COULEUR_BG        = "#f5f5f5"
COULEUR_SURFACE   = "#e8e8e8"
COULEUR_CARD      = "#ffffff"
COULEUR_ACCENT    = "#2563a8"
COULEUR_ACCENT2   = "#1a4f8a"
COULEUR_TEXTE     = "#1a1a1a"
COULEUR_TEXTE_SUB = "#555555"
COULEUR_SUCCES    = "#276749"
COULEUR_ERREUR    = "#b91c1c"
COULEUR_BORDER    = "#cccccc"
 
FONT_TITRE  = ("Segoe UI", 22, "bold")
FONT_SOUS   = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 10)
 
 
def get_connection():
    """Retourne une connexion MySQL."""
    return mysql.connector.connect(**DB_CONFIG)
 
 
# ============================================================
# Application principale
# ============================================================
 
class EsportApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion Esport - Systeme de versions")
        self.geometry("1200x750")
        self.minsize(900, 600)
        self.configure(bg=COULEUR_BG)
        self.resizable(True, True)
 
        self._construire_interface()
        self._afficher_vue("joueurs")
 
    def _construire_interface(self):
        # Barre laterale
        self.sidebar = tk.Frame(self, bg=COULEUR_SURFACE, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
 
        # Logo / titre dans la sidebar
        tk.Label(
            self.sidebar,
            text="ESPORT",
            font=("Segoe UI", 16, "bold"),
            bg=COULEUR_SURFACE,
            fg=COULEUR_ACCENT
        ).pack(pady=(28, 2))
        tk.Label(
            self.sidebar,
            text="Gestion des joueurs",
            font=FONT_SMALL,
            bg=COULEUR_SURFACE,
            fg=COULEUR_TEXTE_SUB
        ).pack(pady=(0, 24))
 
        separateur = tk.Frame(self.sidebar, bg=COULEUR_BORDER, height=1)
        separateur.pack(fill="x", padx=18, pady=(0, 18))
 
        # Boutons de navigation
        self.boutons_nav = {}
        nav_items = [
            ("joueurs",    "Joueurs",              "👥"),
            ("ajouter",    "Ajouter un joueur",    "➕"),
            ("rechercher", "Rechercher",            "🔍"),
            ("modifier",   "Modifier un joueur",   "✏️"),
            ("supprimer",  "Supprimer un joueur",  "🗑️"),
            ("classement", "Classement equipes",   "🏆"),
            ("detail",     "Detail joueur",        "📋"),
        ]
        for cle, label, icone in nav_items:
            btn = self._creer_bouton_nav(self.sidebar, icone + "  " + label, cle)
            self.boutons_nav[cle] = btn
 
        # Zone de contenu principale
        self.contenu = tk.Frame(self, bg=COULEUR_BG)
        self.contenu.pack(side="left", fill="both", expand=True)
 
    def _creer_bouton_nav(self, parent, texte, cle):
        btn = tk.Button(
            parent,
            text=texte,
            font=FONT_BODY,
            bg=COULEUR_SURFACE,
            fg=COULEUR_TEXTE,
            activebackground=COULEUR_ACCENT,
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda k=cle: self._afficher_vue(k)
        )
        btn.pack(fill="x", padx=10, pady=2)
        btn.bind("<Enter>", lambda e, b=btn, k=cle: b.configure(
            bg=COULEUR_SURFACE if self._vue_active == k else COULEUR_BORDER
        ))
        btn.bind("<Leave>", lambda e, b=btn, k=cle: b.configure(
            bg=COULEUR_ACCENT if self._vue_active == k else COULEUR_SURFACE
        ))
        return btn
 
    def _afficher_vue(self, cle):
        self._vue_active = cle
 
        # Mettre a jour les couleurs des boutons
        for k, btn in self.boutons_nav.items():
            btn.configure(
                bg=COULEUR_ACCENT if k == cle else COULEUR_SURFACE,
                fg="white" if k == cle else COULEUR_TEXTE
            )
 
        # Vider la zone de contenu
        for widget in self.contenu.winfo_children():
            widget.destroy()
 
        vues = {
            "joueurs":    VueJoueurs,
            "ajouter":    VueAjouter,
            "rechercher": VueRechercher,
            "modifier":   VueModifier,
            "supprimer":  VueSupprimer,
            "classement": VueClassement,
            "detail":     VueDetail,
        }
        vues[cle](self.contenu, self).pack(fill="both", expand=True)
 
 
# ============================================================
# Composants utilitaires
# ============================================================
 
def carte(parent, **kwargs):
    """Retourne un Frame avec le style carte."""
    f = tk.Frame(parent, bg=COULEUR_CARD, relief="flat", **kwargs)
    return f
 
 
def titre_page(parent, texte, sous_texte=""):
    """Bloc titre en haut de chaque vue."""
    zone = tk.Frame(parent, bg=COULEUR_BG)
    tk.Label(zone, text=texte, font=FONT_TITRE, bg=COULEUR_BG, fg=COULEUR_TEXTE).pack(anchor="w")
    if sous_texte:
        tk.Label(zone, text=sous_texte, font=FONT_BODY, bg=COULEUR_BG, fg=COULEUR_TEXTE_SUB).pack(anchor="w")
    return zone
 
 
def champ_label(parent, label, **kwargs):
    """Retourne un champ de saisie avec son label."""
    tk.Label(parent, text=label, font=FONT_BODY, bg=COULEUR_CARD, fg=COULEUR_TEXTE_SUB).pack(anchor="w", pady=(8, 2))
    entry = tk.Entry(
        parent,
        font=FONT_BODY,
        bg="#f9f9f9",
        fg=COULEUR_TEXTE,
        insertbackground=COULEUR_TEXTE,
        relief="solid",
        highlightthickness=0,
        **kwargs
    )
    entry.pack(fill="x", ipady=6)
    return entry
 
 
def bouton_action(parent, texte, commande, couleur=COULEUR_ACCENT):
    """Bouton d'action stylise."""
    btn = tk.Button(
        parent,
        text=texte,
        font=("Segoe UI", 10, "bold"),
        bg=couleur,
        fg="white",
        activebackground=COULEUR_ACCENT2,
        activeforeground="white",
        relief="flat",
        padx=16,
        pady=8,
        cursor="hand2",
        command=commande
    )
    btn.bind("<Enter>", lambda e: btn.configure(bg=COULEUR_ACCENT2))
    btn.bind("<Leave>", lambda e: btn.configure(bg=couleur))
    return btn
 
 
def tableau(parent, colonnes, hauteur=15):
    """Cree un Treeview stylise."""
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Esport.Treeview",
        background="#ffffff",
        foreground=COULEUR_TEXTE,
        fieldbackground="#ffffff",
        rowheight=28,
        font=FONT_BODY,
        borderwidth=0
    )
    style.configure("Esport.Treeview.Heading",
        background="#e0e0e0",
        foreground=COULEUR_TEXTE,
        font=("Segoe UI", 10, "bold"),
        relief="flat"
    )
    style.map("Esport.Treeview",
        background=[("selected", "#c7daf5")],
        foreground=[("selected", COULEUR_TEXTE)]
    )
 
    cadre = tk.Frame(parent, bg=COULEUR_BORDER, bd=1, relief="solid")
    tree = ttk.Treeview(cadre, columns=colonnes, show="headings",
                        style="Esport.Treeview", height=hauteur)
 
    scrollbar = ttk.Scrollbar(cadre, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
 
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return cadre, tree
 
 
def message_statut(parent, texte, succes=True):
    """Affiche un message de statut temporaire."""
    couleur = COULEUR_SUCCES if succes else COULEUR_ERREUR
    lbl = tk.Label(parent, text=texte, font=FONT_BODY, bg=COULEUR_BG, fg=couleur)
    lbl.pack(pady=6)
    parent.after(4000, lbl.destroy)
 
 
# ============================================================
# Vues
# ============================================================
 
class VueJoueurs(tk.Frame):
    """Liste de tous les joueurs."""
 
    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_BG)
        self.app = app
        self._construire()
 
    def _construire(self):
        zone_titre = titre_page(self, "Liste des joueurs", "Tous les joueurs enregistres dans la base")
        zone_titre.pack(fill="x", padx=30, pady=(24, 16))
 
        zone_btn = tk.Frame(self, bg=COULEUR_BG)
        zone_btn.pack(fill="x", padx=30, pady=(0, 12))
        bouton_action(zone_btn, "Actualiser", self._charger).pack(side="left")
 
        colonnes = ("ID", "Pseudo", "Nom reel", "Nationalite", "Role", "Equipe")
        cadre_tab, self.tree = tableau(self, colonnes, hauteur=18)
        cadre_tab.pack(fill="both", expand=True, padx=30, pady=(0, 20))
 
        for col in colonnes:
            self.tree.heading(col, text=col)
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Pseudo", width=140)
        self.tree.column("Nom reel", width=200)
        self.tree.column("Nationalite", width=120)
        self.tree.column("Role", width=110)
        self.tree.column("Equipe", width=180)
 
        self._charger()
 
    def _charger(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT j.id_joueur, j.pseudo, j.nom_reel, j.nationalite, j.role,
                       COALESCE(e.nom, 'Sans equipe') AS equipe
                FROM joueur j
                LEFT JOIN equipe e ON j.id_equipe = e.id_equipe
                ORDER BY j.pseudo
            """)
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            cursor.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Erreur MySQL", str(e))
 
 
class VueAjouter(tk.Frame):
    """Formulaire d'ajout d'un joueur."""
 
    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_BG)
        self.app = app
        self._construire()
 
    def _construire(self):
        zone_titre = titre_page(self, "Ajouter un joueur", "Remplissez le formulaire pour inserer un nouveau joueur")
        zone_titre.pack(fill="x", padx=30, pady=(24, 16))
 
        card = carte(self)
        card.pack(fill="x", padx=30, pady=(0, 20))
 
        zone = tk.Frame(card, bg=COULEUR_CARD, padx=28, pady=24)
        zone.pack(fill="x")
 
        self.e_pseudo    = champ_label(zone, "Pseudo *")
        self.e_nom       = champ_label(zone, "Nom reel *")
        self.e_nat       = champ_label(zone, "Nationalite")
        self.e_naissance = champ_label(zone, "Date de naissance (AAAA-MM-JJ)")
        self.e_role      = champ_label(zone, "Role")
        self.e_equipe    = champ_label(zone, "ID equipe (laisser vide si aucune)")
 
        zone_btn = tk.Frame(zone, bg=COULEUR_CARD)
        zone_btn.pack(fill="x", pady=(16, 0))
        bouton_action(zone_btn, "Ajouter le joueur", self._ajouter).pack(side="left")
 
        self.zone_statut = tk.Frame(self, bg=COULEUR_BG)
        self.zone_statut.pack(fill="x", padx=30)
 
    def _ajouter(self):
        pseudo    = self.e_pseudo.get().strip()
        nom_reel  = self.e_nom.get().strip()
        nat       = self.e_nat.get().strip()
        naissance = self.e_naissance.get().strip() or None
        role      = self.e_role.get().strip() or None
        id_eq_txt = self.e_equipe.get().strip()
        id_eq     = int(id_eq_txt) if id_eq_txt else None
 
        if not pseudo or not nom_reel:
            messagebox.showwarning("Champ obligatoire", "Le pseudo et le nom reel sont obligatoires.")
            return
 
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO joueur (pseudo, nom_reel, nationalite, date_naissance, role, id_equipe)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (pseudo, nom_reel, nat or None, naissance, role, id_eq))
            conn.commit()
            nouvel_id = cursor.lastrowid
            cursor.close()
            conn.close()
            self._vider_champs()
            message_statut(self.zone_statut, f"Joueur '{pseudo}' ajoute avec l'ID {nouvel_id}.", succes=True)
        except Error as e:
            messagebox.showerror("Erreur MySQL", str(e))
 
    def _vider_champs(self):
        for entry in (self.e_pseudo, self.e_nom, self.e_nat,
                      self.e_naissance, self.e_role, self.e_equipe):
            entry.delete(0, "end")
 
 
class VueRechercher(tk.Frame):
    """Recherche d'un joueur par pseudo ou role."""
 
    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_BG)
        self.app = app
        self._construire()
 
    def _construire(self):
        zone_titre = titre_page(self, "Rechercher un joueur", "Recherche par pseudo ou role")
        zone_titre.pack(fill="x", padx=30, pady=(24, 16))
 
        # Barre de recherche
        card = carte(self)
        card.pack(fill="x", padx=30, pady=(0, 16))
        zone = tk.Frame(card, bg=COULEUR_CARD, padx=28, pady=16)
        zone.pack(fill="x")
 
        tk.Label(zone, text="Critere de recherche", font=FONT_BODY,
                 bg=COULEUR_CARD, fg=COULEUR_TEXTE_SUB).pack(anchor="w", pady=(0, 4))
 
        ligne = tk.Frame(zone, bg=COULEUR_CARD)
        ligne.pack(fill="x")
        self.e_critere = tk.Entry(
            ligne, font=FONT_BODY, bg="#f9f9f9", fg=COULEUR_TEXTE,
            insertbackground=COULEUR_TEXTE, relief="solid",
            highlightthickness=0
        )
        self.e_critere.pack(side="left", fill="x", expand=True, ipady=6)
        self.e_critere.bind("<Return>", lambda e: self._rechercher())
 
        bouton_action(ligne, "Rechercher", self._rechercher).pack(side="left", padx=(10, 0))
 
        colonnes = ("ID", "Pseudo", "Nom reel", "Nationalite", "Role", "Equipe")
        cadre_tab, self.tree = tableau(self, colonnes, hauteur=16)
        cadre_tab.pack(fill="both", expand=True, padx=30, pady=(0, 20))
 
        for col in colonnes:
            self.tree.heading(col, text=col)
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Pseudo", width=140)
        self.tree.column("Nom reel", width=200)
        self.tree.column("Nationalite", width=120)
        self.tree.column("Role", width=110)
        self.tree.column("Equipe", width=180)
 
    def _rechercher(self):
        critere = self.e_critere.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT j.id_joueur, j.pseudo, j.nom_reel, j.nationalite, j.role,
                       COALESCE(e.nom, 'Sans equipe') AS equipe
                FROM joueur j
                LEFT JOIN equipe e ON j.id_equipe = e.id_equipe
                WHERE j.pseudo LIKE %s OR j.role LIKE %s
                ORDER BY j.pseudo
            """, (f"%{critere}%", f"%{critere}%"))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            for row in rows:
                self.tree.insert("", "end", values=row)
            if not rows:
                messagebox.showinfo("Aucun resultat", "Aucun joueur ne correspond a ce critere.")
        except Error as e:
            messagebox.showerror("Erreur MySQL", str(e))
 
 
class VueModifier(tk.Frame):
    """Modification du role ou de l'equipe d'un joueur."""
 
    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_BG)
        self.app = app
        self._construire()
 
    def _construire(self):
        zone_titre = titre_page(self, "Modifier un joueur", "Mettez a jour le role ou l'equipe d'un joueur")
        zone_titre.pack(fill="x", padx=30, pady=(24, 16))
 
        card = carte(self)
        card.pack(fill="x", padx=30, pady=(0, 20))
        zone = tk.Frame(card, bg=COULEUR_CARD, padx=28, pady=24)
        zone.pack(fill="x")
 
        self.e_id    = champ_label(zone, "ID du joueur a modifier *")
        self.e_role  = champ_label(zone, "Nouveau role (laisser vide pour ne pas changer)")
        self.e_equipe = champ_label(zone, "Nouvel ID equipe (laisser vide pour ne pas changer)")
 
        zone_btn = tk.Frame(zone, bg=COULEUR_CARD)
        zone_btn.pack(fill="x", pady=(16, 0))
        bouton_action(zone_btn, "Enregistrer les modifications", self._modifier).pack(side="left")
 
        self.zone_statut = tk.Frame(self, bg=COULEUR_BG)
        self.zone_statut.pack(fill="x", padx=30)
 
    def _modifier(self):
        id_txt = self.e_id.get().strip()
        if not id_txt.isdigit():
            messagebox.showwarning("ID invalide", "Veuillez entrer un ID numerique valide.")
            return
        id_j       = int(id_txt)
        nouveau_role = self.e_role.get().strip()
        nouvelle_eq  = self.e_equipe.get().strip()
 
        if not nouveau_role and not nouvelle_eq:
            messagebox.showwarning("Aucune modification", "Renseignez au moins un champ a modifier.")
            return
 
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if nouveau_role:
                cursor.execute("UPDATE joueur SET role = %s WHERE id_joueur = %s", (nouveau_role, id_j))
            if nouvelle_eq:
                cursor.execute("UPDATE joueur SET id_equipe = %s WHERE id_joueur = %s", (int(nouvelle_eq), id_j))
            conn.commit()
            lignes = cursor.rowcount
            cursor.close()
            conn.close()
            message_statut(self.zone_statut, f"Joueur ID {id_j} mis a jour ({lignes} ligne(s) affectee(s)).", succes=True)
        except Error as e:
            messagebox.showerror("Erreur MySQL", str(e))
 
 
class VueSupprimer(tk.Frame):
    """Suppression d'un joueur par ID."""
 
    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_BG)
        self.app = app
        self._construire()
 
    def _construire(self):
        zone_titre = titre_page(self, "Supprimer un joueur", "Cette action est irreversible")
        zone_titre.pack(fill="x", padx=30, pady=(24, 16))
 
        card = carte(self)
        card.pack(fill="x", padx=30, pady=(0, 20))
        zone = tk.Frame(card, bg=COULEUR_CARD, padx=28, pady=24)
        zone.pack(fill="x")
 
        self.e_id = champ_label(zone, "ID du joueur a supprimer *")
 
        avertissement = tk.Label(
            zone,
            text="Attention : la suppression est definitive et ne peut pas etre annulee.",
            font=FONT_SMALL,
            bg=COULEUR_CARD,
            fg=COULEUR_ACCENT2,
            wraplength=500,
            justify="left"
        )
        avertissement.pack(anchor="w", pady=(10, 0))
 
        zone_btn = tk.Frame(zone, bg=COULEUR_CARD)
        zone_btn.pack(fill="x", pady=(16, 0))
        bouton_action(zone_btn, "Supprimer le joueur", self._supprimer, couleur=COULEUR_ERREUR).pack(side="left")
 
        self.zone_statut = tk.Frame(self, bg=COULEUR_BG)
        self.zone_statut.pack(fill="x", padx=30)
 
    def _supprimer(self):
        id_txt = self.e_id.get().strip()
        if not id_txt.isdigit():
            messagebox.showwarning("ID invalide", "Veuillez entrer un ID numerique valide.")
            return
        id_j = int(id_txt)
        confirmation = messagebox.askyesno(
            "Confirmer la suppression",
            f"Etes-vous sur de vouloir supprimer le joueur avec l'ID {id_j} ?"
        )
        if not confirmation:
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM joueur WHERE id_joueur = %s", (id_j,))
            conn.commit()
            lignes = cursor.rowcount
            cursor.close()
            conn.close()
            self.e_id.delete(0, "end")
            if lignes == 0:
                message_statut(self.zone_statut, f"Aucun joueur trouve avec l'ID {id_j}.", succes=False)
            else:
                message_statut(self.zone_statut, f"Joueur ID {id_j} supprime avec succes.", succes=True)
        except Error as e:
            messagebox.showerror("Erreur MySQL", str(e))
 
 
class VueClassement(tk.Frame):
    """Classement des equipes par nombre de victoires."""
 
    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_BG)
        self.app = app
        self._construire()
 
    def _construire(self):
        zone_titre = titre_page(self, "Classement des equipes", "Trie par nombre de victoires decroissant")
        zone_titre.pack(fill="x", padx=30, pady=(24, 16))
 
        zone_btn = tk.Frame(self, bg=COULEUR_BG)
        zone_btn.pack(fill="x", padx=30, pady=(0, 12))
        bouton_action(zone_btn, "Actualiser", self._charger).pack(side="left")
 
        colonnes = ("Rang", "Equipe", "Victoires", "Matchs joues")
        cadre_tab, self.tree = tableau(self, colonnes, hauteur=18)
        cadre_tab.pack(fill="both", expand=True, padx=30, pady=(0, 20))
 
        for col in colonnes:
            self.tree.heading(col, text=col)
        self.tree.column("Rang", width=60, anchor="center")
        self.tree.column("Equipe", width=250)
        self.tree.column("Victoires", width=120, anchor="center")
        self.tree.column("Matchs joues", width=150, anchor="center")
 
        self._charger()
 
    def _charger(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.nom AS equipe,
                       SUM(CASE
                           WHEN m.id_equipe1 = e.id_equipe AND m.score_equipe1 > m.score_equipe2 THEN 1
                           WHEN m.id_equipe2 = e.id_equipe AND m.score_equipe2 > m.score_equipe1 THEN 1
                           ELSE 0
                       END) AS victoires,
                       COUNT(m.id_match) AS matchs_joues
                FROM equipe e
                LEFT JOIN match_esport m ON (m.id_equipe1 = e.id_equipe OR m.id_equipe2 = e.id_equipe)
                GROUP BY e.id_equipe, e.nom
                ORDER BY victoires DESC, matchs_joues ASC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            for rang, row in enumerate(rows, start=1):
                self.tree.insert("", "end", values=(rang,) + row)
        except Error as e:
            messagebox.showerror("Erreur MySQL", str(e))
 
 
class VueDetail(tk.Frame):
    """Detail complet d'un joueur avec son equipe."""
 
    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_BG)
        self.app = app
        self._construire()
 
    def _construire(self):
        zone_titre = titre_page(self, "Detail d'un joueur", "Informations completes incluant les donnees d'equipe")
        zone_titre.pack(fill="x", padx=30, pady=(24, 16))
 
        # Barre de saisie de l'ID
        card_top = carte(self)
        card_top.pack(fill="x", padx=30, pady=(0, 16))
        zone_top = tk.Frame(card_top, bg=COULEUR_CARD, padx=28, pady=16)
        zone_top.pack(fill="x")
 
        tk.Label(zone_top, text="ID du joueur *", font=FONT_BODY,
                 bg=COULEUR_CARD, fg=COULEUR_TEXTE_SUB).pack(anchor="w", pady=(0, 4))
 
        ligne = tk.Frame(zone_top, bg=COULEUR_CARD)
        ligne.pack(fill="x")
        self.e_id = tk.Entry(
            ligne, font=FONT_BODY, bg="#f9f9f9", fg=COULEUR_TEXTE,
            insertbackground=COULEUR_TEXTE, relief="solid",
            highlightthickness=0, width=12
        )
        self.e_id.pack(side="left", ipady=6)
        self.e_id.bind("<Return>", lambda e: self._charger())
        bouton_action(ligne, "Afficher le detail", self._charger).pack(side="left", padx=(10, 0))
 
        # Zone d'affichage des resultats
        self.card_result = carte(self)
        self.card_result.pack(fill="both", expand=True, padx=30, pady=(0, 20))
 
    def _charger(self):
        id_txt = self.e_id.get().strip()
        if not id_txt.isdigit():
            messagebox.showwarning("ID invalide", "Veuillez entrer un ID numerique valide.")
            return
        id_j = int(id_txt)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT j.id_joueur, j.pseudo, j.nom_reel, j.nationalite,
                       j.date_naissance, j.role,
                       COALESCE(e.nom, 'Sans equipe') AS equipe,
                       COALESCE(e.pays, '-') AS pays_equipe,
                       COALESCE(CAST(e.date_creation AS CHAR), '-') AS creation_equipe
                FROM joueur j
                LEFT JOIN equipe e ON j.id_equipe = e.id_equipe
                WHERE j.id_joueur = %s
            """, (id_j,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
 
            for widget in self.card_result.winfo_children():
                widget.destroy()
 
            if not row:
                tk.Label(
                    self.card_result, text="Joueur introuvable.",
                    font=FONT_BODY, bg=COULEUR_CARD, fg=COULEUR_ERREUR, pady=20
                ).pack()
                return
 
            zone = tk.Frame(self.card_result, bg=COULEUR_CARD, padx=28, pady=24)
            zone.pack(fill="both", expand=True)
 
            champs = [
                ("ID",             str(row[0])),
                ("Pseudo",         str(row[1])),
                ("Nom reel",       str(row[2])),
                ("Nationalite",    str(row[3])),
                ("Date naissance", str(row[4])),
                ("Role",           str(row[5])),
                ("Equipe",         str(row[6])),
                ("Pays de l'equipe", str(row[7])),
                ("Creation equipe", str(row[8])),
            ]
 
            for label, valeur in champs:
                ligne = tk.Frame(zone, bg=COULEUR_CARD)
                ligne.pack(fill="x", pady=4)
                tk.Label(ligne, text=label + " :", font=("Segoe UI", 11, "bold"),
                         bg=COULEUR_CARD, fg=COULEUR_TEXTE_SUB, width=20, anchor="w").pack(side="left")
                tk.Label(ligne, text=valeur, font=FONT_BODY,
                         bg=COULEUR_CARD, fg=COULEUR_TEXTE).pack(side="left")
 
        except Error as e:
            messagebox.showerror("Erreur MySQL", str(e))
 
 
# ============================================================
# Point d'entree
# ============================================================
 
if __name__ == '__main__':
    app = EsportApp()
    app.mainloop()
