import pygame


''' Represent a point in the grid for the pathfinding algorithm. '''
class Node():
    # pixel_coordinates are for drawing on-screen, and grid_coordinates are
    # for the logical data.
    def __init__(self, node_size, pixel_coordinates, walkable, grid_coordinates):
        self.walkable = walkable
        self.node_rect = pygame.Rect((pixel_coordinates), node_size)
        self.color = (150, 150, 150, 255) # Set as light grey by default.
        self.grid_coordinates = grid_coordinates

        # Pathfinding Algorithm Data ---------------------------------------
        self.g_cost = float('inf') # Cost from starting node to current node.
        self.h_cost = float('inf') # Guess of the cost from current node to end node.
        self.f_cost = float('inf') # Total estimated cost.
        self.parent = None # Reference to the previous optimal node.


    def draw_node(self, screen_surf):
        pygame.draw.rect(screen_surf, self.color, self.node_rect)

    def toggle_walkable(self):
        self.walkable = not self.walkable

        if self.walkable:
            self.color = (150, 150, 150, 255)
        else:
            self.color = (50, 50, 50, 255)

    # Implementing the Manhattan Distance formula |x1 - x2| + |y1 - y2|
    def calculate_h_cost(self, end_node):
        # grid_coords[1] is the x (column), and grid_coord[0] is the y (row).
        dx = abs(self.grid_coordinates[1] - end_node.grid_coordinates[1])
        dy = abs(self.grid_coordinates[0] - end_node.grid_coordinates[0])
        self.h_cost = dx + dy
        self.f_cost = self.g_cost + self.h_cost

    # Less than comparison method.
    def __lt__(self, other):
        return self.f_cost < other.f_cost
