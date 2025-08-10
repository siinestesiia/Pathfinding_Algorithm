import pygame
from sys import exit


''' Main class for running the app. '''
class GameApp():
    def __init__(self):
        pygame.init()
        screen_width, screen_height = 1000, 800
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('PathFinder')
        self.clock = pygame.time.Clock()
        
        # Node related
        self.node_size = (50, 50)
        self.node_offset = 5 # Space between nodes.


        self.run_app()

        # # Pathfinding variables --------------------------------------
        # ''' Cost from starting node to current node (traveled distance) '''
        # g_cost = 0 
        # ''' Estimated cost from current node to target node '''
        # h_cost = 0
        # ''' total estimated cost of the path '''
        # f_cost = g_cost + h_cost


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

            ''' Draw the nodes in the grid from the list each frame '''
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
        for y_index in range(rows):
            row = []
            for x_index in range(cols):
                node_coordinates = (x_index * grid_gap_x + offset,
                                    y_index * grid_gap_y + offset)
                new_node = Node(self.node_size, node_coordinates, True)
                row.append(new_node)

            self.grid.append(row)


    def select_node(self, mouse_pos, mouse_button):
        node = self.get_node_from_pos(mouse_pos)
        
        # Check if the mouse clicked on node or gap in the grid
        if node:
            # Left click
            if mouse_button == 1: 
                print(f'Left Button pressed at {mouse_pos}!')
                print(node.node_rect)      
    
            # Right click
            elif mouse_button == 3:
                print(f'Right Button pressed at {mouse_pos}!')
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


# --------------------------------------------------------------------------------

''' Represent a point in the grid for the pathfinding algorithm. '''
class Node():
    def __init__(self, node_size, coordinates, walkable):
        self.walkable = walkable
        self.node_rect = pygame.Rect((coordinates), node_size)

    def draw_node(self, screen_surf):
        if self.walkable:
            node_color = (150, 150, 150, 255) # Light grey.
        else:
            node_color = (50, 50, 50, 255) # Dark grey.

        pygame.draw.rect(screen_surf, node_color, self.node_rect)

    def toggle_walkable(self):
        self.walkable = not self.walkable

# ------------------------------------------------------------------------------


if __name__ == '__main__':
    game = GameApp()