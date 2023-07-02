import pygame
import random


pygame.init()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)


largeur_ecran = 800
hauteur_ecran = 600


taille_cellule = 20


ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Snake By N0x")

horloge = pygame.time.Clock()


class Serpent:
    def __init__(self):
        self.longueur = 1
        self.positions = [((largeur_ecran / 2), (hauteur_ecran / 2))]
        self.direction = random.choice([1, -1, 2, -2])
        self.score = 0

    def mouvement(self):
        touches = pygame.key.get_pressed()

        if touches[pygame.K_RIGHT] and self.direction != -1:
            self.direction = 1
        elif touches[pygame.K_LEFT] and self.direction != 1:
            self.direction = -1
        elif touches[pygame.K_UP] and self.direction != 2:
            self.direction = -2
        elif touches[pygame.K_DOWN] and self.direction != -2:
            self.direction = 2

        tete = self.positions[0]
        x, y = tete

        if self.direction == 1:
            nouvelle_position = (x + taille_cellule, y)
        elif self.direction == -1:
            nouvelle_position = (x - taille_cellule, y)
        elif self.direction == 2:
            nouvelle_position = (x, y + taille_cellule)
        elif self.direction == -2:
            nouvelle_position = (x, y - taille_cellule)

        self.positions.insert(0, nouvelle_position)

        if len(self.positions) > self.longueur:
            self.positions.pop()

    def afficher(self):
        for position in self.positions:
            pygame.draw.rect(ecran, VERT, (position[0], position[1], taille_cellule, taille_cellule))

    def manger_pomme(self, pomme):
        if self.positions[0] == pomme.position:
            self.score += 1
            self.longueur += 1
            pomme.repositionner()

    def mourir(self):
        tete = self.positions[0]
        if tete[0] < 0 or tete[0] >= largeur_ecran or tete[1] < 0 or tete[1] >= hauteur_ecran:
            return True
        for position in self.positions[1:]:
            if position == tete:
                return True
        return False


class Pomme:
    def __init__(self):
        self.position = (0, 0)
        self.repositionner()

    def repositionner(self):
        self.position = (random.randint(0, largeur_ecran-taille_cellule) // taille_cellule * taille_cellule,
                         random.randint(0, hauteur_ecran-taille_cellule) // taille_cellule * taille_cellule)

    def afficher(self):
        pygame.draw.rect(ecran, ROUGE, (self.position[0], self.position[1], taille_cellule, taille_cellule))


serpent = Serpent()
pomme = Pomme()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    ecran.fill(NOIR)
    serpent.mouvement()
    serpent.manger_pomme(pomme)
    serpent.afficher()
    pomme.afficher()

    if serpent.mourir():
        pygame.quit()
        quit()

    pygame.display.update()
    horloge.tick(10)
