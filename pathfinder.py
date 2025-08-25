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

        # A* Pathfinding colors
        self.open_color = (0, 150, 255) # Blue
        self.closed_color = (255, 165, 0) # Orange
        self.path_color = (255, 255, 0) # Yellow

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
                # Start finding a path event
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.start_node != None and self.end_node != None:
                            self.reset_grid()
                            self.find_path()
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

        # Account for the initial offset on left and top.
        adjusted_x = mouse_x - offset
        adjusted_y = mouse_y - offset

        # calculate the grid column and row.
        col = adjusted_x // grid_gap_x
        row = adjusted_y // grid_gap_y

        # Check if the calculated indices are within the grid bounds.
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            # Now check if the click was actually inside the node's rect.
            node = self.grid[row][col]
            if node.node_rect.collidepoint(mouse_pos):
                return node
        
        return None

    def find_path(self):
        # A list of nodes to be evaluated, sorted by f_cost.
        open_set = []
        # A set of nodes already evaluated.
        closed_set = set()

        # Start the algorithm
        self.start_node.g_cost = 0
        self.start_node.calculate_h_cost(self.end_node)
        open_set.append(self.start_node) # Add the start node

        # Main loop for A*
        while open_set:
            # Sort the set and get the node with lowest f_cost.
            open_set.sort()
            current_node = open_set.pop(0)

            # Move the current node the the closed set.
            closed_set.add(current_node)
            current_node.color = self.closed_color

            # If the current node is the end node, you found the path.
            if current_node == self.end_node:
                self.reconstruct_path(current_node)
                self.start_node.color = self.start_color
                self.end_node.color = self.end_color
                print('Path found!')
                return
            
            # Iterate trhough the neighbors of the current node.
            for neighbor in self.get_neighbors(current_node):
                # If the neighbor is not walkable or has been evaluated, skip it.
                if not neighbor.walkable or neighbor in closed_set:
                    continue

                # The g_cost to the neighbor is the g_cost of the current node + 1
                new_g_cost = current_node.g_cost + 1

                # If a better path to the neighbor is found:
                if new_g_cost < neighbor.g_cost:
                    # Update neighbor's costs and parent.
                    neighbor.parent = current_node
                    neighbor.g_cost = new_g_cost
                    neighbor.calculate_h_cost(self.end_node)

                    # Add the neighbor to the open set if isn't already there.
                    if neighbor not in open_set:
                        open_set.append(neighbor)
                        neighbor.color = self.open_color

        print('No path found.')   

    def get_neighbors(self, node):
        neighbors = []
        row, col = node.grid_coordinates

        # Directions: up, down, left, right.
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for d_row, d_col in directions:
            neighbor_row, neighbor_col = row + d_row, col + d_col

            # Check if the neighbor is within the grid bounds.
            if 0 <= neighbor_row < len(self.grid) and 0 <= neighbor_col < len(self.grid[0]):
                neighbor = self.grid[neighbor_row][neighbor_col]
                neighbors.append(neighbor)

        return neighbors

    def reconstruct_path(self, current_node):
        temp_node = current_node
        while temp_node.parent:
            temp_node.color = self.path_color
            temp_node = temp_node.parent

    # After finding a path, clears all nodes
    def reset_grid(self):
        for row in self.grid:
            for node in row:
                if node.walkable:
                    node.color = self.walkable_color
                    # Reset all the A* costs and parent
                    node.g_cost = float('inf')
                    node.h_cost = float('inf')
                    node.f_cost = float('inf')
                    node.parent = None


if __name__ == '__main__':
    game = PathfinderApp()