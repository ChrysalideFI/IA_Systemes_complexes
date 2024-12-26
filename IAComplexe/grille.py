import random
import threading
import time
import sys

class Grille:
    def __init__(self, taille, prob):
        self.taille = taille
        self.grille = [['*' for _ in range(taille)] for _ in range(taille)]
        self.prob = prob

    def afficher_en_place(self):
        sys.stdout.write("\033[H\033[J")  # Déplace le curseur au coin supérieur gauche et efface l'écran
        for ligne in self.grille:
            sys.stdout.write(' '.join(ligne) + "\n")
        sys.stdout.flush()

    def placer_au_hasard(self, symbole, quantite):
        places_vides = [(i, j) for i in range(self.taille) for j in range(self.taille) if self.grille[i][j] == '*']
        for _ in range(quantite):
            if not places_vides:
                print(f"Pas assez de place pour placer {symbole}")
                break
            i, j = random.choice(places_vides)
            self.grille[i][j] = symbole
            places_vides.remove((i, j))

    def voisins(self, x, y):
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        voisins = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.taille and 0 <= ny < self.taille:
                voisins.append((nx, ny))
        return voisins

    def mise_a_jour(self):
        input("Appuyer sur entrer pour continuer")
        nouvelle_grille = [ligne[:] for ligne in self.grille]

        def update_cell(i, j):
            # print(f"Thread démarré pour la cellule ({i}, {j})")
            if self.grille[i][j] == 'A':
                # Si un arbre a un voisin en feu, il prend feu
                if any(self.grille[x][y] == 'F' for x, y in self.voisins(i, j)):
                    nouvelle_grille[i][j] = 'F'
                    # print("Arbre : ", j+1, ",", i+1, " prend feu")
            elif self.grille[i][j] == 'F':
                # Un feu reste un feu
                nouvelle_grille[i][j] = 'F'
            
            elif self.grille[i][j] == '*':
                #Proba qu'une 
                if random.random() < self.prob:
                    nouvelle_grille[i][j] = "A"
                    # print("Nouvelle arbre à poussé à : ", j+1, ",", i+1)
            # print(f"Thread terminé pour la cellule ({i}, {j})")
        
        threads = []
        # start_time = time.time()
        for i in range(self.taille):
            for j in range(self.taille):
                thread = threading.Thread(target=update_cell, args=(i, j))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()
        # end_time = time.time()

        self.grille = nouvelle_grille
        # print(f"Temps d'exécution de mise_a_jour: {end_time - start_time} secondes")

