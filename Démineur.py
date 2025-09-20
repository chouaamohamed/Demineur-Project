import pygame
import random
import pygame_gui
import json
import pygame_gui.elements
import os

#Configuration générale
TAILLE = 600
HAUTEUR_INTERFACE = 150
gris_normal = (96,96,96)
gris_découvert = (189, 188, 188)
vert = (2, 163, 2)
noir = (0,0,0)
bleu = (41, 42, 255)
rouge = (252, 11, 11)
bleu_foncé = (0, 0, 139)
violet = (238, 130, 238)
rouge_game_over = (187, 11, 11)
vert_victoire = (0, 100, 0)

#Configuration répertoires
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
scores_chemin = os.path.join(BASE_DIR, "scores", "scores.json")

amiga_police_chemin = os.path.join(BASE_DIR, "polices", "amiga4ever.ttf")
Pixel_police_chemin = os.path.join(BASE_DIR, "polices", "Pixel Sans Serif Condensed.ttf")
minesweeper_police_chemin = os.path.join(BASE_DIR, "polices", "mine-sweeper.ttf")

drapeau_image_chemin = os.path.join(BASE_DIR, "images", "drapeau.png")
case_image_chemin = os.path.join(BASE_DIR, "images", "case.png")
decouverte_image_chemin = os.path.join(BASE_DIR, "images", "découverte.png")
bombe_image_chemin = os.path.join(BASE_DIR, "images", "bombe.png")
fausse_bombe_image_chemin = os.path.join(BASE_DIR, "images", "pas_bombe.png")
fond_menu_image_chemin = os.path.join(BASE_DIR, "images", "fond_menu.png")
fond_interface_image_chemin = os.path.join(BASE_DIR, "images", "fond_interface.png")

class Menu:
    def __init__(self): #options initiales pour avoir un menu
        pygame.init()

        #rendu tes textes pour l'écran principal
        self.texte = pygame.font.Font(Pixel_police_chemin, 70).render("Démineur", True, bleu_foncé)  #Texte écran
        self.texte_prénom1 = pygame.font.Font(Pixel_police_chemin, 20).render("Chouaa Mohamed - 23105", True, noir)
        self.texte_prénom2 = pygame.font.Font(Pixel_police_chemin, 20).render("Bicha Anis - 23076", True, noir)

        self.texte_rect = self.texte.get_rect(center=(TAILLE // 2, 75))
        self.texte_rect_prénom1 = self.texte_prénom1.get_rect(center=(TAILLE // 2, 125))
        self.texte_rect_prénom2 = self.texte_prénom2.get_rect(center=(TAILLE // 2, 150))

        self.fondMenu = pygame.image.load(fond_menu_image_chemin) #on charge l'image en fond

        self.fenetre = pygame.display.set_mode((TAILLE, TAILLE))
        pygame.display.set_caption("Menu Démineur")
        self.manager = pygame_gui.UIManager((TAILLE, TAILLE))
        self.clock = pygame.time.Clock()
        self.play = False

        # Ajouter les boutons
        self.bouton_jouer = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((TAILLE // 3, TAILLE // 3, 200, 50)),
            text='Jouer',
            manager=self.manager
        )
        self.bouton_quitter = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((TAILLE // 3, TAILLE // 3 + 70, 200, 50)),
            text='Quitter',
            manager=self.manager
        )

        # Liste déroulante pour choisir la taille de la grille
        self.choix_taille_grille = pygame_gui.elements.UIDropDownMenu(
            options_list=["10x10", "20x20", "30x30"],
            starting_option="20x20",
            relative_rect=pygame.Rect((TAILLE // 3, TAILLE // 3 + 140, 200, 30)),
            manager=self.manager
        )

        self.choix_densité_bombe = pygame_gui.elements.UIDropDownMenu(
            options_list=["Débutant", "Novice", "Pro", "Fou malade"],
            starting_option="Novice",
            relative_rect=pygame.Rect((TAILLE // 3, TAILLE // 3 + 175, 200, 30)),
            manager=self.manager
        )

        self.colonnes_selectionnees = 20 #on met cette valeur par défaut sinon le jeu arrive pas à prendre en compte le elif en dessous
        self.densité_bombe = 2*self.colonnes_selectionnees #la mm    
        self.densite_choisie = "Novice"  #la mm

    def update_densité_bombe(self):
        #Met à jour la densité des bombes en fonction de la taille de la grille et de la densité choisie
        if self.densite_choisie == "Débutant":
            self.densité_bombe = 1 * self.colonnes_selectionnees
        elif self.densite_choisie == "Novice":
            self.densité_bombe = 2 * self.colonnes_selectionnees
        elif self.densite_choisie == "Pro":
            self.densité_bombe = 3 * self.colonnes_selectionnees
        elif self.densite_choisie == "Fou malade":
            self.densité_bombe = 9 * self.colonnes_selectionnees

    def run(self):
        running = True
        while running:
            delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.bouton_jouer:
                        self.play = True
                        running = False  # Ferme le menu et démarre le jeu
                    elif event.ui_element == self.bouton_quitter:
                        running = False  # Ferme le menu sans lancer le jeu

                #boutons qui détermineront le nbr de case et de bombes dans la grille
                elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED: #si les choix de grille et de bombes ont été cliqués
                    if event.ui_element == self.choix_taille_grille:
                        self.colonnes_selectionnees = int(event.text.split('x')[0]) #méthode pour prendre que le chiffre du texte selectionné dans la liste en haut
                        self.update_densité_bombe() #on met à jour la densité de bombe pour éviter un bug (bug qui choisira la taille de grille par défaut)

                    elif event.ui_element == self.choix_densité_bombe:
                        self.densite_choisie = event.text
                        self.update_densité_bombe()

                self.manager.process_events(event)

            self.manager.update(delta_time)
            self.fenetre.blit(self.fondMenu, (0,0)) # Fond du menu (image) positionné en 0,0
            self.fenetre.blit(self.texte, self.texte_rect)
            self.fenetre.blit(self.texte_prénom1, self.texte_rect_prénom1)
            self.fenetre.blit(self.texte_prénom2, self.texte_rect_prénom2)
            self.manager.draw_ui(self.fenetre)
            pygame.display.update()

        pygame.quit()

class Grille:
    #Classe représentant la grille du jeu

    def __init__(self, colonnes, nombre_bombes):
        self.colonnes = colonnes
        self.nombre_bombes = nombre_bombes
        self.grille = [["caché" for _ in range(colonnes)] for _ in range(colonnes)] #crée une grille avec le nbr de colonnes adéquates
        self.bombes_placées = False #on dit ça pour faire en sorte que les bombes soient placées après le 1er clic du joueur

    def placer_bombes(self, premier_clic):
        #Place les bombes aléatoirement sur la grille
        bombes_places = 0
        row_clic, col_clic = premier_clic 
        #ces coordonnées = celles du 1er clic grâce à la fonction gerer_evenements => gerer_clic_gauche => placer_bombes
        #dcp les indices row et col de gerer_clic_gauche deviennent premier_clic dans placer_bombes

        cases_interdites = set() #sert à faire en sorte que le 1er clic et ses cases voisines ne soient pas une bombe (comme dans le vrai jeu)
        for i in range(-1, 2):
            for j in range(-1, 2):
                voisin_row_clic, voisin_col_clic = row_clic + i, col_clic + j

                if 0 <= voisin_row_clic < self.colonnes and 0 <= voisin_col_clic < self.colonnes:
                    cases_interdites.add((voisin_row_clic, voisin_col_clic))

        while bombes_places < self.nombre_bombes: #condition while pour placer le nbr de bombes max imposées
            row = random.randint(0, self.colonnes - 1)
            col = random.randint(0, self.colonnes - 1)
            if self.grille[row][col] != "bombe" and (row, col) not in cases_interdites: #condition pour être sûr de pas placer une bombe sur une bombe et sur les cases interdites
                self.grille[row][col] = "bombe"
                bombes_places += 1

        self.bombes_placées = True #dis que les bombes ont été placées (à la fin de la fonction pour la fct gerer_clic_gauche)

    def devoiler_cases(self, row, col):
        #Dévoile une case et ses voisines si nécessaire
        if isinstance(self.grille[row][col], int): #si la case possède un chiffre (ce qui est le cas si elle possède des bombes voisines), on dévoile pas histoire de pas dévoiler 2 fois une case
            return
        if self.colonnes <= row < 0 or self.colonnes <= col < 0 : #si la case se trouve hors de la fenêtre de jeu, on dévoile pas
            return
        if self.grille[row][col] in {"découvert", "marqué", "bombe_marqué", "bombe"}: #si la case a déjà été découverte, marquée, ou est une bombe, on dévoile pas
            return

        bombes_voisines = 0 #on dit que c'est = 0 pour compter le nbr de bombes voisines juste en dessous
        cases_voisines = [] #liste qui permettra de stocker les coordonnées des cases voisines

        for i in range(-1, 2): #sert à traiter chacune des cases voisines
            for j in range(-1, 2):
                voisin_row, voisin_col = row + i, col + j
                if 0 <= voisin_row < self.colonnes and 0 <= voisin_col < self.colonnes: #condition pour être sûr que les cases voisines se trouvent dans le jeu
                    if self.grille[voisin_row][voisin_col] == "bombe" or self.grille[voisin_row][voisin_col] == "bombe_marqué": #si les cases voisines sont des bombes, on augmente le compteur
                        bombes_voisines += 1
                    else: #sinon on ajoute les coordonnées à la liste pour dévoiler ces cases-ci
                        cases_voisines.append((voisin_row, voisin_col))

        self.grille[row][col] = bombes_voisines if bombes_voisines > 0 else "découvert"
        #on précise ici que la case selectionnée possède des bombes voisines si jms le nbr de bombes_voisines > 0, si c'est pas le cas elle est juste découverte

        if bombes_voisines == 0: #pour le cas où elle est découverte et n'a pas de bombes voisines, on va utiliser la fct pour dévoiler les cases voisines
            #on va dévoiler les cases voisines de la case sélectionnée jusqu'à ce qu'on atteigne une case ayant un nombre de bombes voisines
            for voisin_row, voisin_col in cases_voisines:
                self.devoiler_cases(voisin_row, voisin_col) #on va recommencer le mm principe pour les cases voisines des cases voisines => fct récursive

class Interface :
    #Classe pour gérer tout ce qui est interface (partie d'en dessous)

    def __init__(self, fenetre, nombre_bombes):
        self.font_interface = pygame.font.Font(amiga_police_chemin, 25)  # Police utilisée pour afficher le texte
        self.temps_début = None  # Temps de début, va commencer qd on clique pour la 1ère fois
        self.fenetre = fenetre
        self.nombre_bombes = nombre_bombes

    def démarrer_chronomètre(self):
        # Démarre le chronomètre au moment du premier clic
        if self.temps_début is None:
            self.temps_début = pygame.time.get_ticks()

    def afficher_chronomètre(self, fenetre):
        # Calcule et affiche le temps écoulé
        if self.temps_début is None:
            temps_écoulé = 0
        else:
            temps_écoulé = (pygame.time.get_ticks() - self.temps_début) // 1000  # Convertir ms en secondes, on soustrait avec temps_début sinon lors du premier clic, le chronomètre aura démarré depuis le début du programme

        minutes = temps_écoulé // 60
        secondes = temps_écoulé % 60
        texte_temps = f"{minutes:02}:{secondes:02}"  # Format MM:SS

        texte_render = self.font_interface.render(texte_temps, True, noir)

        # Position du texte (au milieu horizontalement et sous la grille)
        fenetre.blit(texte_render, (25, TAILLE + HAUTEUR_INTERFACE // 3 - 10))

    def afficher_drapeaux_restants(self, fenetre, grille):
        nombre_drapeaux = sum(1 for row in grille.grille for case in row if case == "marqué" or case == "bombe_marqué")
        #on compte 1 par 1 dans chaque ligne de la grille => dans chaque case de la ligne => si la case est marquée par un drapeau
        drapeaux_restants = self.nombre_bombes - nombre_drapeaux
        # Calcule et affiche le nombre de bombes restantes (total bombes - cases marquées)
        
        texte_bombes = f"Drapeaux restants : {drapeaux_restants}"
        texte_render = self.font_interface.render(texte_bombes, True, noir)

        # Position du texte (à gauche en bas sous la grille)
        fenetre.blit(texte_render, (25, TAILLE + HAUTEUR_INTERFACE // 3 + 40))

    def afficher_message_game_over(self):
        # Affiche le message de Game Over au centre de l'écran
        texte = pygame.font.Font(Pixel_police_chemin, 70).render("Game Over!", True, rouge_game_over)  # Texte rouge
        texte_ombre = pygame.font.Font(Pixel_police_chemin, 70).render("Game Over!", True, noir) #texte noir pour l'ombre

        texte_rect = texte.get_rect(center=(TAILLE // 2, (TAILLE) // 2))
        texte_rect_ombre = texte_ombre.get_rect(center=(TAILLE // 2 + 5, (TAILLE) // 2 + 5))

        self.fenetre.blit(texte_ombre, texte_rect_ombre)
        self.fenetre.blit(texte, texte_rect)

        pygame.display.update()

    def afficher_message_victoire(self):
        # Affiche le message de victoire au centre de l'écran
        texte = pygame.font.Font(Pixel_police_chemin, 68).render("Tu as gagné !", True, vert_victoire)  # Texte vert
        texte_ombre = pygame.font.Font(Pixel_police_chemin, 68).render("Tu as gagné !", True, noir)

        texte_rect = texte.get_rect(center=(TAILLE // 2, (TAILLE) // 2))
        texte_rect_ombre = texte_ombre.get_rect(center=(TAILLE // 2 + 5, (TAILLE) // 2 + 5))

        self.fenetre.blit(texte_ombre, texte_rect_ombre)
        self.fenetre.blit(texte, texte_rect)
        pygame.display.update()

class Score: #classe servant à calculer les temps

    fondMenu = pygame.image.load(fond_menu_image_chemin) #pour lancer l'image de fond à l'affichage des scores

    def afficher_boite_saisie(self, fenetre, temps_ecoule, callback_enregistrement):
            # Affiche une boîte de dialogue pour entrer le pseudo
            manager = pygame_gui.UIManager((TAILLE, TAILLE + HAUTEUR_INTERFACE))
            boite_saisie = pygame_gui.elements.UITextEntryLine( #boite de texte servant à mettre son pseudo
                relative_rect=pygame.Rect((TAILLE // 3, TAILLE // 2 + 100, 200, 30)),
                manager=manager
            )
            bouton_valider = pygame_gui.elements.UIButton( #bouton pour valider le pseudo
                relative_rect=pygame.Rect((TAILLE // 3, TAILLE // 2 + 140, 200, 50)),
                text='Valider',
                manager=manager
            )

            running = True
            pseudo_validé = False #on dit que c'est False car au moment de la confirmation le True servira à changer d'écran (voir fonction vérifier_victoire)
            while running:
                delta_time = pygame.time.Clock().tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == bouton_valider:
                        pseudo = boite_saisie.text
                        if pseudo.strip():  # Si le pseudo n'est pas vide
                            callback_enregistrement(pseudo, temps_ecoule)
                            pseudo_validé = True
                            running = False  #La boîte de dialogue arrête de fonctionner car pseudo_validé = True

                    manager.process_events(event)

                manager.update(delta_time)
                manager.draw_ui(fenetre)
                pygame.display.update()

            if pseudo_validé: #condition pour laisser place à la fonction afficher_meilleur_temps
                fenetre.blit(self.fondMenu, (0,0))  #se met par dessus le jeu entier pour afficher le score
                pygame.display.update()
    
    def enregistrer_temps(pseudo, temps): #fonction qui va enregistrer le score du joueur (temps en sec)
        score = {"pseudo": pseudo, "temps": temps} #dictionnaire pour classer tous les scores

        try:
            #Charger les scores existants
            with open(scores_chemin, "r") as fichier: #"r" pour la lecture du fichier scores.json
                scores = json.load(fichier) #on va charger le fichier sous forme de variable
        except FileNotFoundError:
            # Si le fichier n'existe pas, créer une liste vide
            scores = []

        # Ajouter le nouveau score
        scores.append(score) #on va implémenter le nv scroe

        # Sauvegarder les scores triés par temps (meilleur temps en premier)
        scores = sorted(scores, key=lambda x: x['temps']) #lambda permet de trier la variable du temps

        with open(scores_chemin, "w") as fichier: #"w" pour écriture car on va écrire sur le fichier json le nv score
            json.dump(scores, fichier) #fonction servant à écrire sur un fichier

    def afficher_meilleur_temps(self, fenetre):
        manager = pygame_gui.UIManager((TAILLE, TAILLE + HAUTEUR_INTERFACE))

        try:
            with open(scores_chemin, "r") as fichier:
                scores = json.load(fichier)
        except FileNotFoundError:
            scores = []

        if not scores:
            scores_str = "Aucun score enregistré pour le moment." #si y a 0 score écrit ils vont écrire ça
        else:
            scores_str = "<b>Meilleurs scores :</b><br>" #<b> permet d'écrire en gras
            for score in scores:
                scores_str += f"{score['pseudo']} - {score['temps']} secondes<br>" #on va citer chaque score disponible. ici <br> signifie retour à la ligne

        # Création du panneau et de la boîte de texte
        score_panneau = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((25, 25), (550, 250)),
            manager=manager
        )

        score_texte = pygame_gui.elements.UITextBox( #on écrit en html car la fonction UITextBox (qui marche dcp avec de l'HTML) permet de scroller tous les scores possibles
            html_text=scores_str,
            relative_rect=pygame.Rect((0, 0), (550, 250)),
            manager=manager,
            container=score_panneau
        )

        bouton_quitter = pygame_gui.elements.UIButton( #bouton quitter pour quitter oslm
            relative_rect=pygame.Rect((TAILLE // 3, TAILLE // 2 + 200, 200, 50)),
            text='Quitter',
            manager=manager
        )

        running = True
        while running:
            delta_time = pygame.time.Clock().tick(60) / 1000.0 #sert à calculer le temps entre chaque image (pour 1s), servira donc à mettre à jour la fonction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == bouton_quitter:
                    running = False  # Quitte l'affichage des scores

                manager.process_events(event)

            manager.update(delta_time)
            manager.draw_ui(fenetre)
            pygame.display.update()
   
class Démineur:
    #Classe principale pour gérer le jeu

    def __init__(self, colonnes, nombre_bombes):
        pygame.init()
        self.colonnes = colonnes #on le met entre parenthèses dans la fct init pour le remplacer par le nbr de colonnes du menu à la fin du code
        self.distance_e_colonnes = TAILLE // self.colonnes #on le redéfinit ici pour que les fct prennent le self.colonnes et pas la valeur globale
        self.nombre_bombes = nombre_bombes
        self.fenetre = pygame.display.set_mode((TAILLE, TAILLE + HAUTEUR_INTERFACE))
        pygame.display.set_caption("Démineur")
        self.grille = Grille(self.colonnes, nombre_bombes)
        self.play = True
        self.interface = Interface(self.fenetre, self.nombre_bombes)  # Création de l'interface
        self.score = Score()
        self.fondInterface = pygame.image.load(fond_interface_image_chemin)

        #pour charger les images dans le jeu
        self.drapeauImage = pygame.image.load(drapeau_image_chemin)
        self.drapeau_redimensionne = pygame.transform.scale(self.drapeauImage, (self.distance_e_colonnes, self.distance_e_colonnes))

        self.caseImage = pygame.image.load(case_image_chemin)
        self.case_redimensionne = pygame.transform.scale(self.caseImage, (self.distance_e_colonnes, self.distance_e_colonnes))

        self.decouverteImage = pygame.image.load(decouverte_image_chemin)
        self.decouverte_redimensionne = pygame.transform.scale(self.decouverteImage, (self.distance_e_colonnes, self.distance_e_colonnes))

        self.bombeImage = pygame.image.load(bombe_image_chemin)
        self.bombe_redimensionne = pygame.transform.scale(self.bombeImage, (self.distance_e_colonnes, self.distance_e_colonnes))

        self.faussebombeImage = pygame.image.load(fausse_bombe_image_chemin)
        self.faussebombe_redimensionne = pygame.transform.scale(self.faussebombeImage, (self.distance_e_colonnes, self.distance_e_colonnes))


        #si on laisse la taille de la police tel quel les chiffres vont êtres trop grands/trop petits qd on changera de taille de grille 
        if self.colonnes == 10:
            taille_police = 30
        elif self.colonnes == 20:
            taille_police = 15
        elif self.colonnes == 30:
            taille_police = 10

        self.font = pygame.font.Font(minesweeper_police_chemin, taille_police)
        

    def afficher_grille(self):
        #Affiche la grille dans la fenêtre
        self.fenetre.blit(self.fondInterface, (0,600)) #couleur qd on lance le jeu

        for row in range(self.colonnes):
            for col in range(self.colonnes):
                rect = pygame.Rect(col * self.distance_e_colonnes, row * self.distance_e_colonnes, self.distance_e_colonnes, self.distance_e_colonnes)
                #va dessiner pour chaque colonne et chaque ligne des rectangles en fct du nbr de lignes et de la distance entre ces lignes
                case = self.grille.grille[row][col] #on va considérer la case actuelle comme une variable case pour pouvoir choisir la couleur

                self.fenetre.blit(self.case_redimensionne, rect.topleft) #image des cases non découvertes

                if case == "marqué": #couleur pour le drapeau
                    self.fenetre.blit(self.drapeau_redimensionne, rect.topleft)
                elif case == "bombe_marqué": #la mm mais la case a été nommée différemment pour pas de bug dans la classe Grille
                    self.fenetre.blit(self.drapeau_redimensionne, rect.topleft)
                elif case == "découvert" or isinstance(case, int): #couleur pour la case découverte
                    self.fenetre.blit(self.decouverte_redimensionne, rect.topleft)
                    if isinstance(case, int) and case > 0: #et si jms la case possède un chiffre => fct pour dessiner le chiffre
                        self.afficher_chiffre(row, col, case)

        self.dessiner_grille() #fct servant à dessiner la grille (colonnes et lignes en noir)
        self.interface.afficher_chronomètre(self.fenetre)  # Affiche le chronomètre
        self.interface.afficher_drapeaux_restants(self.fenetre, self.grille)  # Affiche le nombre de bombes restantes
        pygame.display.update()

    def dessiner_grille(self):
        #Dessine la grille avec des lignes noires
        for i in range(self.colonnes):
            x = y = i * self.distance_e_colonnes #on va multiplier le nbr de colonnes à la distance e colonnes pour obtenir leurs coordonnées
            pygame.draw.line(self.fenetre, gris_normal, (x, 0), (x, TAILLE)) #on va tracer les lignes verticales de x (début) à x fin et de 0 à TAILLE (pour y)
            pygame.draw.line(self.fenetre, gris_normal, (0, y), (TAILLE, y)) #on va tracer les lignes horizontales de y début à y fin et de 0 à TAILLE (pour x)

    def afficher_chiffre(self, row, col, bombes_voisines):
        #Affiche le nombre de bombes voisines au centre d'une case
        if bombes_voisines == 1:
            color = bleu #on change de couleur en fonction du nombre de bombes voisines --> ici bleu
            division_x = 2.7 #positionement des chiffres sur la case différente à cause de la police d'écriture

        elif bombes_voisines == 2:
            color = vert
            division_x = 3.5
                    
        elif bombes_voisines == 3:
            color = rouge
            division_x = 3.5
                    
        elif bombes_voisines == 4:
            color = bleu_foncé
            division_x = 3.5

        else:
            color = noir
            division_x = 3.5

        text = self.font.render(str(bombes_voisines), True, color) #va faire un rendu du nbr de bombes_voisines avec l'option lissage et la couleur
        self.fenetre.blit(text, (col * self.distance_e_colonnes + self.distance_e_colonnes // division_x, row * self.distance_e_colonnes + self.distance_e_colonnes // 6))
        #sert à positionner le texte en fct de la case sélectionnée

    def vérifier_victoire(self):
        # Vérifie si toutes les bombes ont été marquées correctement
        for row in range(self.colonnes):
            for col in range(self.colonnes):
                case = self.grille.grille[row][col]
                if case == "bombe" or case == "marqué" or case == "caché":  #Conditions pour savoir si le joueur a gagné : si la case c'est encore une bombe cachée, ou une case marquée mais sans bombe, ou tout simplement une case cachée, le joueur n'a pas encore gagné
                    return False
        

        # Si la victoire est confirmée
        temps_ecoule = (pygame.time.get_ticks() - self.interface.temps_début) // 1000
        self.interface.afficher_message_victoire()

        self.score.afficher_boite_saisie(
            self.fenetre,
            temps_ecoule,
            lambda pseudo, temps: Score.enregistrer_temps(pseudo, temps)
        )

        self.score.afficher_meilleur_temps(self.fenetre)

        return True

    def gérer_evenements(self):
        #Gère les événements du joueur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #pour avoir les coordonnées de la case cliquée
                x, y = pygame.mouse.get_pos()

                if y < 600:
                    
                    row, col = y // self.distance_e_colonnes, x // self.distance_e_colonnes

                    if event.button == 1:  # Clic gauche
                        self.gérer_clic_gauche(row, col)
                    elif event.button == 3:  # Clic droit
                        self.gérer_clic_droit(row, col)

    def gérer_clic_gauche(self, row, col):
        #Gère un clic gauche sur la grille

        if not self.grille.bombes_placées:
            self.grille.placer_bombes((row, col)) #si le bombes_placées = False, on va placer les bombes => condition pour pas toucher une bombe dès le 1er clic
            self.interface.démarrer_chronomètre()  # Démarre le chronomètre

        case = self.grille.grille[row][col] #coordonnées de la case sélectionnée par la fct
        if case == "bombe":
            self.réveler_bombes()
            self.interface.afficher_message_game_over()  # Affiche le message de Game Over
            pygame.time.delay(2000)
            self.play = False
        else:
            self.grille.devoiler_cases(row, col)

    def gérer_clic_droit(self, row, col):
        #Gère un clic droit pour marquer ou dé-marquer une case
        nombre_drapeaux = sum(1 for row in self.grille.grille for case in row if case == "marqué" or case == "bombe_marqué") #on remet la mm ligne de code que dans la fct afficher_drapeaux_restants

        case = self.grille.grille[row][col]
        if case == "caché" and nombre_drapeaux < self.nombre_bombes: #condition pour pas qu'il y ait plus de drapeaux que de bombes
            self.grille.grille[row][col] = "marqué"
        elif case == "marqué":
            self.grille.grille[row][col] = "caché"
        elif case == "bombe"and nombre_drapeaux < self.nombre_bombes:
            self.grille.grille[row][col] = "bombe_marqué"
        elif case == "bombe_marqué":
            self.grille.grille[row][col] = "bombe"

    def réveler_bombes(self):
        #Révèle toutes les bombes de la grille
        for row in range(self.colonnes):
            for col in range(self.colonnes):
                if self.grille.grille[row][col] == "bombe":
                    rect = pygame.Rect(col * self.distance_e_colonnes, row * self.distance_e_colonnes, self.distance_e_colonnes, self.distance_e_colonnes) #décris ce que sera un rectangle pour la ligne de code suivante
                    self.fenetre.blit(self.bombe_redimensionne, rect.topleft) #dessine en rouge le rectange sélectionné is jms c'est une bombe => toutes les bombes seront révélées
                elif self.grille.grille[row][col] == "marqué":
                    rect = pygame.Rect(col * self.distance_e_colonnes, row * self.distance_e_colonnes, self.distance_e_colonnes, self.distance_e_colonnes) #décris ce que sera un rectangle pour la ligne de code suivante
                    self.fenetre.blit(self.faussebombe_redimensionne, rect.topleft) #dessine en violet tous les drapeaux qui ne sont pas des bombes
        pygame.display.update()

    def run(self):
        #Boucle principale du jeu
        while self.play:
            
            self.gérer_evenements()
            self.afficher_grille()
            pygame.display.update()
            pygame.time.Clock().tick(60)

            if self.vérifier_victoire(): #c'est pour faire quitter le jeu qd t'as gagné
                self.play = False


if __name__ == "__main__": #sert à limiter le lancement de ce code dans le cas où on l'importe dans un autre fichier
    menu = Menu()
    menu.run()

    if menu.play: #condition pour que le vrai jeu soit lancé
        jeu = Démineur(menu.colonnes_selectionnees, menu.densité_bombe)
        jeu.run() #sert à lancer la classe Démineur