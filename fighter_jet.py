import pygame
import math


class FighterJet:
    def __init__(self, id, position, velocity, max_speed, max_force, perception_radius):
        self.id = id
        self.position = list(position)  # [x, y]
        self.velocity = list(velocity)  # [vx, vy]
        self.acceleration = [0, 0]
        self.max_speed = max_speed
        self.max_force = max_force
        self.perception_radius = perception_radius

    def flock(self, jets):
        alignment = self.align(jets)
        cohesion = self.cohere(jets)
        separation = self.separate(jets)

        # Pondération des forces
        self.acceleration[0] += alignment[0] + cohesion[0] + separation[0]
        self.acceleration[1] += alignment[1] + cohesion[1] + separation[1]

    def update(self):
        # Ajouter l'accélération à la vitesse
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        # Limiter la vitesse au maximum autorisé
        speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if speed > self.max_speed:
            self.velocity[0] = (self.velocity[0] / speed) * self.max_speed
            self.velocity[1] = (self.velocity[1] / speed) * self.max_speed

        # Mettre à jour la position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Réinitialiser l'accélération après chaque mise à jour
        self.acceleration = [0, 0]

    def avoid_obstacles(self, obstacles):
        """
        Méthode pour éviter les obstacles.
        obstacles : liste de tuples (x, y, width, height)
        """
        steer = [0, 0]
        for obs in obstacles:
            obs_x, obs_y, obs_width, obs_height = obs
            obs_center = (obs_x + obs_width / 2, obs_y + obs_height / 2)

            # Distance entre le jet et l'obstacle
            distance_x = obs_center[0] - self.position[0]
            distance_y = obs_center[1] - self.position[1]
            distance = math.sqrt(distance_x**2 + distance_y**2)

            # Si l'obstacle est dans la perception du jet
            if distance < self.perception_radius:
                # Calculer une force d'évitement
                steer[0] -= distance_x / distance  # Repousse dans la direction opposée
                steer[1] -= distance_y / distance

        # Limiter la force de l'évitement
        magnitude = math.sqrt(steer[0]**2 + steer[1]**2)
        if magnitude > self.max_force:
            steer[0] = (steer[0] / magnitude) * self.max_force
            steer[1] = (steer[1] / magnitude) * self.max_force

        # Ajouter la force d'évitement à l'accélération
        self.acceleration[0] += steer[0]
        self.acceleration[1] += steer[1]

    def seek_target(self, targets):
        """
        Méthode pour poursuivre les cibles.
        targets : liste de positions [(x, y), ...]
        """
        for target in targets:
            desired = [target[0] - self.position[0], target[1] - self.position[1]]
            distance = math.sqrt(desired[0]**2 + desired[1]**2)

            # Normaliser le vecteur désiré
            if distance > 0:
                desired[0] = (desired[0] / distance) * self.max_speed
                desired[1] = (desired[1] / distance) * self.max_speed

            # Calculer la force de steering
            steer = [desired[0] - self.velocity[0], desired[1] - self.velocity[1]]

            # Limiter la force
            magnitude = math.sqrt(steer[0]**2 + steer[1]**2)
            if magnitude > self.max_force:
                steer[0] = (steer[0] / magnitude) * self.max_force
                steer[1] = (steer[1] / magnitude) * self.max_force

            # Ajouter à l'accélération
            self.acceleration[0] += steer[0]
            self.acceleration[1] += steer[1]
            break  # Ne cible qu'une cible à la fois

    # Méthodes align, cohere et separate à définir ou adapter si nécessaire
    def align(self, jets):
        # Exemple d'alignement (simple)
        return [0, 0]

    def cohere(self, jets):
        # Exemple de cohésion (simple)
        return [0, 0]

    def separate(self, jets):
        # Exemple de séparation (simple)
        return [0, 0]
