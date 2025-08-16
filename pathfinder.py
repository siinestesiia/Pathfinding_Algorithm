from sys import exit
import pygame
from node import Node


''' Main class for running the app. '''
class PathfinderApp():
    def __init__(self):
        pygame.init()
        screen_width, screen_height = 1000, 800
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('A* Pathfinder')
        self.clock = pygame.time.Clock()
        
        # Node related ----------------------------------------------------------
        self.node_size = (50, 50)
        self.node_offset = 5 # Gap between nodes.
        self.start_node = None
        self.end_node = None

        self.start_color = (0, 255, 0, 255) # Green color.
        self.end_color = (255, 0, 0, 255) # Red color.
        self.walkable_color = (150, 150, 150, 255) # Light grey.
        self.unwalkable_color = (50, 50, 50, 255) # Dark grey.

        self.run_app()


    def run_app(self):
        self.generate_grid()

        while True:
            # Events ------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if event.button == 1:
                        self.select_node(mouse_pos, event.button)
                    elif event.button == 3:
                        self.select_node(mouse_pos, event.button)
                if event.type == pygame.QUIT:
                    pygame.quit() # Terminate the game.
                    exit() # from sys module, to properly quit.
            # --------------------------------------------------------------   
                 
            # Main logic here ---------------------------------------------
            self.screen.fill((20, 20, 35)) # Clear the screen with a dark color

            ''' Draw the grid each frame '''
            for row in self.grid:
                for node in row:
                    node.draw_node(self.screen)

            # Update section ----------------------------------------------
            pygame.display.update()
            self.clock.tick(60) # FPS.


    ''' Generates and stores nodes in a grid (2D list) '''
    def generate_grid(self):
        screen_width, screen_height = self.screen.get_size()
        node_width, node_height = self.node_size
        offset = self.node_offset

        self.grid = [] # 2D list.
        
        grid_gap_x = node_width + offset
        grid_gap_y = node_height + offset

        # Calculate how many cols and rows fit on screen
        cols = (screen_width - offset) // grid_gap_x
        rows = (screen_height - offset) // grid_gap_y

        ''' Grid generation process '''
        # pixel_coordinates are for drawing on-screen, and grid_coordinates are
        # for the logical data.
        for y_index in range(rows):
            row = []
            for x_index in range(cols):
                pixel_coordinates = (x_index * grid_gap_x + offset,
                                    y_index * grid_gap_y + offset)
                grid_coordinates = (y_index, x_index)

                new_node = Node(self.node_size, pixel_coordinates,
                                True, grid_coordinates)
                row.append(new_node)

            self.grid.append(row)


    def select_node(self, mouse_pos, mouse_button):
        node = self.get_node_from_pos(mouse_pos)
        
        # Check if the mouse clicked on a node or a gap in the grid
        if node:
            # Left click
            if mouse_button == 1:
                # Set a new start node.
                if not self.start_node:
                    self.start_node = node
                    self.start_node.color = self.start_color
                # Set new end node but not on the start node.
                elif not self.end_node and node != self.start_node:
                    self.end_node = node
                    self.end_node.color = self.end_color
                # If both are set, clear them and set a new node
                else:
                    if self.start_node:
                        self.start_node.color = self.walkable_color # Reset color.
                        self.start_node = None
                    if self.end_node:
                        self.end_node.color = self.walkable_color # Reset color.
                        self.end_node = None
                    
                    self.start_node = node
                    self.start_node.color = self.start_color

            # Right click
            elif mouse_button == 3:
                # Only toggle if it's walkable or non-walkable.
                if node != self.start_node and node != self.end_node:
                    node.toggle_walkable()


    def get_node_from_pos(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        node_width, node_height = self.node_size
        offset = self.node_offset

        grid_gap_x = node_width + offset
        grid_gap_y = node_height + offset

        # Account for the initial offset on left and top
        adjusted_x = mouse_x - offset
        adjusted_y = mouse_y - offset

        # calculate the grid column and row
        col = adjusted_x // grid_gap_x
        row = adjusted_y // grid_gap_y

        # Check if the calculated indices are within the grid bounds
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            # Now check if the click was actually inside the node's rect
            node = self.grid[row][col]
            if node.node_rect.collidepoint(mouse_pos):
                return node
        
        return None



if __name__ == '__main__':
    game = PathfinderApp()