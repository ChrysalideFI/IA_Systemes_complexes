import random
from feu import Feu
from color import Color
from queue import PriorityQueue

class Robot:
    def __init__(self):
        self.symbole = Color.CYAN + 'R' + Color.END
        self.eau_max = 3  # Quantité d'eau maximale
        self.eau_actuelle = self.eau_max

    def se_deplacer(self, grille, position_actuelle):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1)  # Haut, Bas, Gauche, Droite
        ]
        x, y = position_actuelle
        random.shuffle(directions)  # Mélanger les directions pour un mouvement aléatoire

        print(f"Robot essaie de se déplacer depuis {position_actuelle}")
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grille) and 0 <= ny < len(grille):
                # Vérifiez que la case cible est vide et non occupée par un autre robot
                if grille[nx][ny] == '*' and not isinstance(grille[nx][ny], Robot):
                    return nx, ny  # Retourner la nouvelle position valide

        print("Aucune position valide, le robot reste en place.")
        return x, y  # Si aucun mouvement valide, rester en place


    def eteindre_feu(self, grille, position_actuelle):
        if self.eau_actuelle <= 0:
            print("Le robot n'a plus d'eau et doit se recharger.")
            return False

        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1)  # Haut, Bas, Gauche, Droite
        ]
        x, y = position_actuelle

        # Parcourir les cases adjacentes
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grille) and 0 <= ny < len(grille[0]) and isinstance(grille[nx][ny], Feu):
                # Remplacer l'objet Feu par une case vide
                grille[nx][ny] = '*'
                self.eau_actuelle -= 1
                print(f"Feu éteint à la position ({nx}, {ny}), eau restante : {self.eau_actuelle}")
                return True  # Feu éteint avec succès

        return False  # Aucun feu éteint
    
    def recharger(self):
        print("Le robot se recharge en eau.")
        self.eau_actuelle = self.eau_max
        
    def chercher_chemin(self, depart, objectif, taille, grille):
        """Trouve un chemin du point de départ au point objectif en évitant les obstacles."""
        def heuristique(a, b):
            # Distance de Manhattan
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def voisins(position):
            x, y = position
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < taille and 0 <= ny < taille and grille[nx][ny] == '*':
                    yield (nx, ny)
                    
        
        # Initialisation
        frontier = PriorityQueue()
        frontier.put((0, depart))
        came_from = {depart: None}
        cost_so_far = {depart: 0}

        while not frontier.empty():
            _, current = frontier.get()

            if current == objectif:
                break

            for next in voisins(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristique(next, objectif)
                    frontier.put((priority, next))
                    came_from[next] = current

        # Reconstruire le chemin
        chemin = []
        current = objectif
        while current is not None:
            chemin.append(current)
            current = came_from.get(current)
        chemin.reverse()

        return chemin