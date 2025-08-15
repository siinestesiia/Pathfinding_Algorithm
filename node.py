import pygame


''' Represent a point in the grid for the pathfinding algorithm. '''
class Node():
    def __init__(self, node_size, coordinates, walkable):
        self.walkable = walkable
        self.node_rect = pygame.Rect((coordinates), node_size)
        self.color = (150, 150, 150, 255) # Set as light grey by default.

    def draw_node(self, screen_surf):
        pygame.draw.rect(screen_surf, self.color, self.node_rect)

    def toggle_walkable(self):
        self.walkable = not self.walkable

        if self.walkable:
            self.color = (150, 150, 150, 255)
        else:
            self.color = (50, 50, 50, 255)
