import pygame
import random
import math
from fighter_jet import FighterJet

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de Chasseurs - Swarm Behavior")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

# Paramètres des chasseurs
NUM_JETS = 20
MAX_SPEED = 4
MAX_FORCE = 0.2
PERCEPTION_RADIUS = 50

# Création de la flotte de jets
jets = [
    FighterJet(
        id=i,
        position=(random.randint(0, WIDTH), random.randint(0, HEIGHT)),
        velocity=(random.uniform(-2, 2), random.uniform(-2, 2)),
        max_speed=MAX_SPEED,
        max_force=MAX_FORCE,
        perception_radius=PERCEPTION_RADIUS,
    )
    for i in range(NUM_JETS)
]

# Ajouter une liste de cibles
targets = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(5)]

# Ajouter une liste d'obstacles
obstacles = [(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 40, 40) for _ in range(3)]

# Fonction pour dessiner un jet en forme de triangle
def draw_jet(jet):
    # Calcul de l'angle de direction
    angle = math.atan2(jet.velocity[1], jet.velocity[0])
    x, y = jet.position

    # Taille du jet
    jet_size = 10

    # Points du triangle
    point1 = (x + jet_size * math.cos(angle), y + jet_size * math.sin(angle))
    point2 = (x - jet_size * math.cos(angle + math.pi / 4), y - jet_size * math.sin(angle + math.pi / 4))
    point3 = (x - jet_size * math.cos(angle - math.pi / 4), y - jet_size * math.sin(angle - math.pi / 4))

    # Dessiner le triangle
    pygame.draw.polygon(WINDOW, BLUE, [point1, point2, point3])

# Fonction pour dessiner les cibles
def draw_target(target):
    pygame.draw.circle(WINDOW, RED, target, 8)

# Fonction pour dessiner les obstacles
def draw_obstacle(obstacle):
    pygame.draw.rect(WINDOW, WHITE, obstacle)

# Fonction pour dessiner le rayon de perception
def draw_perception_radius(jet):
    pygame.draw.circle(WINDOW, CYAN, (int(jet.position[0]), int(jet.position[1])), jet.perception_radius, 1)

# Boucle principale
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # Limite à 60 FPS
        WINDOW.fill(BLACK)  # Effacer l'écran

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dessiner les cibles
        for target in targets:
            draw_target(target)

        # Dessiner les obstacles
        for obstacle in obstacles:
            draw_obstacle(obstacle)

        # Mise à jour et dessin des jets
        for jet in jets:
            jet.avoid_obstacles(obstacles)  # Éviter les obstacles
            jet.seek_target(targets)       # Attaquer les cibles
            jet.flock(jets)                # Comportement en essaim
            jet.update()                   # Mettre à jour la position et la vitesse

            # Gestion des bords de la fenêtre
            if jet.position[0] > WIDTH:
                jet.position[0] = 0
            elif jet.position[0] < 0:
                jet.position[0] = WIDTH

            if jet.position[1] > HEIGHT:
                jet.position[1] = 0
            elif jet.position[1] < 0:
                jet.position[1] = HEIGHT

            # Dessiner le jet et le rayon de perception
            draw_jet(jet)
            draw_perception_radius(jet)

        # Rafraîchir l'affichage
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
