import pygame
import random
import sys
from datetime import datetime

pygame.init()

class Tetris:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        
        # Pygame setup
        self.cell_size = 30
        self.board_width = self.width * self.cell_size
        self.board_height = self.height * self.cell_size
        self.sidebar_width = 200
        self.screen_width = self.board_width + self.sidebar_width
        self.screen_height = self.board_height + 100
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tetris - Hello World!")
        
        # Colors
        self.colors = [
            (0, 0, 0),      # Empty - Black
            (255, 0, 0),    # I - Red
            (0, 255, 0),    # O - Green
            (0, 0, 255),    # T - Blue
            (255, 255, 0),  # S - Yellow
            (255, 0, 255),  # Z - Magenta
            (0, 255, 255),  # J - Cyan
            (255, 128, 0),  # L - Orange
        ]
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Tetris pieces (I, O, T, S, Z, J, L)
        self.pieces = [
            [['.....',
              '..#..',
              '..#..',
              '..#..',
              '..#..']],  # I piece
            [['.....',
              '.....',
              '.##..',
              '.##..',
              '.....']],  # O piece
            [['.....',
              '.....',
              '.#...',
              '###..',
              '.....'],
             ['.....',
              '.....',
              '.#...',
              '.##..',
              '.#...'],
             ['.....',
              '.....',
              '.....',
              '###..',
              '.#...'],
             ['.....',
              '.....',
              '.#...',
              '##...',
              '.#...']], # T piece rotations
            [['.....',
              '.....',
              '.##..',
              '##...',
              '.....'],
             ['.....',
              '.#...',
              '.##..',
              '..#..',
              '.....']], # S piece rotations
            [['.....',
              '.....',
              '##...',
              '.##..',
              '.....'],
             ['.....',
              '..#..',
              '.##..',
              '.#...',
              '.....']], # Z piece rotations
            [['.....',
              '.#...',
              '.###.',
              '.....',
              '.....'],
             ['.....',
              '.##..',
              '.#...',
              '.#...',
              '.....'],
             ['.....',
              '.....',
              '.###.',
              '...#.',
              '.....'],
             ['.....',
              '..#..',
              '..#..',
              '.##..',
              '.....']], # J piece rotations
            [['.....',
              '...#.',
              '.###.',
              '.....',
              '.....'],
             ['.....',
              '.#...',
              '.#...',
              '.##..',
              '.....'],
             ['.....',
              '.....',
              '.###.',
              '.#...',
              '.....'],
             ['.....',
              '.##..',
              '..#..',
              '..#..',
              '.....']]  # L piece rotations
        ]
        
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.current_x = self.width // 2 - 2
        self.current_y = 0
        self.current_rotation = 0
        
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        self.clock = pygame.time.Clock()
        
    def get_new_piece(self):
        return random.randint(0, len(self.pieces) - 1)
    
    def spawn_next_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        self.current_x = self.width // 2 - 2
        self.current_y = 0
        self.current_rotation = 0
    
    def can_move(self, dx, dy, rotation=None):
        if rotation is None:
            rotation = self.current_rotation
            
        piece = self.pieces[self.current_piece][rotation]
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == '#':
                    new_x = self.current_x + x + dx
                    new_y = self.current_y + y + dy
                    
                    if (new_x < 0 or new_x >= self.width or 
                        new_y >= self.height or 
                        (new_y >= 0 and self.board[new_y][new_x] != 0)):
                        return False
        return True
    
    def place_piece(self):
        piece = self.pieces[self.current_piece][self.current_rotation]
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == '#':
                    board_x = self.current_x + x
                    board_y = self.current_y + y
                    if board_y >= 0:
                        self.board[board_y][board_x] = self.current_piece + 1
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(self.height):
            if all(cell != 0 for cell in self.board[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [0] * self.width)
            
        cleared = len(lines_to_clear)
        self.lines_cleared += cleared
        self.score += cleared * 100 * self.level
        
        if self.lines_cleared >= self.level * 10:
            self.level += 1
            self.fall_speed = max(50, self.fall_speed - 50)
    
    def draw_board(self):
        # Draw the game board
        for y in range(self.height):
            for x in range(self.width):
                color = self.colors[self.board[y][x]]
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)
    
    def draw_piece(self):
        # Draw the current falling piece
        piece = self.pieces[self.current_piece][self.current_rotation]
        color = self.colors[self.current_piece + 1]
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == '#':
                    board_x = self.current_x + x
                    board_y = self.current_y + y
                    if 0 <= board_y < self.height and 0 <= board_x < self.width:
                        rect = pygame.Rect(board_x * self.cell_size, 
                                         board_y * self.cell_size,
                                         self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)
    
    def draw_next_piece(self):
        sidebar_x = self.board_width + 10
        next_y = 420
        preview_size = 15
        preview_width = 4 * preview_size
        preview_height = 4 * preview_size
        
        # Draw "Next:" label
        next_label = self.font.render("Next:", True, (255, 255, 255))
        self.screen.blit(next_label, (sidebar_x, next_y - 35))
        
        # Draw preview box border
        border_rect = pygame.Rect(sidebar_x - 2, next_y - 2, preview_width + 4, preview_height + 4)
        pygame.draw.rect(self.screen, (128, 128, 128), border_rect, 2)
        
        # Draw background
        bg_rect = pygame.Rect(sidebar_x, next_y, preview_width, preview_height)
        pygame.draw.rect(self.screen, (32, 32, 32), bg_rect)
        
        # Draw the next piece
        piece = self.pieces[self.next_piece][0]  # Use first rotation
        color = self.colors[self.next_piece + 1]
        
        # Calculate offset to center the piece in preview box
        piece_width = len(piece[0]) * preview_size
        piece_height = len(piece) * preview_size
        offset_x = (preview_width - piece_width) // 2
        offset_y = (preview_height - piece_height) // 2
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == '#':
                    rect = pygame.Rect(
                        sidebar_x + offset_x + x * preview_size,
                        next_y + offset_y + y * preview_size,
                        preview_size,
                        preview_size
                    )
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)
    
    def draw_ui(self):
        # Draw sidebar with game info
        sidebar_x = self.board_width + 10
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (sidebar_x, 50))
        
        # Level
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (sidebar_x, 100))
        
        # Lines
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, (255, 255, 255))
        self.screen.blit(lines_text, (sidebar_x, 150))
        
        # Controls
        controls_y = 250
        controls = [
            "Controls:",
            "←/→ - Move",
            "↓ - Soft drop",
            "↑ - Rotate",
            "Space - Hard drop",
            "ESC - Quit"
        ]
        
        for i, control in enumerate(controls):
            if i == 0:
                text = self.font.render(control, True, (255, 255, 255))
            else:
                text = self.small_font.render(control, True, (200, 200, 200))
            self.screen.blit(text, (sidebar_x, controls_y + i * 25))
        
        # Date and time at bottom
        datetime_text = self.small_font.render(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            True, (150, 150, 150)
        )
        self.screen.blit(datetime_text, (10, self.screen_height - 30))
        
        # Draw next piece preview
        self.draw_next_piece()
    
    def game_over(self):
        return not self.can_move(0, 0)
    
    def drop_piece(self):
        while self.can_move(0, 1):
            self.current_y += 1
    
    def rotate_piece(self):
        max_rotation = len(self.pieces[self.current_piece]) - 1
        new_rotation = (self.current_rotation + 1) % (max_rotation + 1)
        
        if self.can_move(0, 0, new_rotation):
            self.current_rotation = new_rotation
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Movement with key repeat delay
        if keys[pygame.K_LEFT] and self.can_move(-1, 0):
            self.current_x -= 1
            pygame.time.wait(100)
        elif keys[pygame.K_RIGHT] and self.can_move(1, 0):
            self.current_x += 1
            pygame.time.wait(100)
        elif keys[pygame.K_DOWN] and self.can_move(0, 1):
            self.current_y += 1
            pygame.time.wait(50)
    
    def run(self):
        # Show welcome message
        self.screen.fill((0, 0, 0))
        welcome_text = self.font.render("Hello, World!", True, (255, 255, 255))
        welcome_rect = welcome_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
        self.screen.blit(welcome_text, welcome_rect)
        
        tetris_text = self.font.render("Welcome to Pygame Tetris!", True, (255, 255, 255))
        tetris_rect = tetris_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(tetris_text, tetris_rect)
        
        start_text = self.small_font.render("Press any key to start...", True, (200, 200, 200))
        start_rect = start_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 50))
        self.screen.blit(start_text, start_rect)
        
        pygame.display.flip()
        
        # Wait for key press to start
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
        
        # Main game loop
        running = True
        while running and not self.game_over():
            dt = self.clock.tick(60)
            self.fall_time += dt
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.drop_piece()
            
            # Handle continuous input
            self.handle_input()
            
            # Automatic falling
            if self.fall_time >= self.fall_speed:
                if self.can_move(0, 1):
                    self.current_y += 1
                else:
                    self.place_piece()
                    self.clear_lines()
                    self.spawn_next_piece()
                self.fall_time = 0
            
            # Draw everything
            self.screen.fill((0, 0, 0))
            self.draw_board()
            self.draw_piece()
            self.draw_ui()
            pygame.display.flip()
        
        # Game over screen
        if self.game_over():
            self.screen.fill((0, 0, 0))
            game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            score_rect = final_score_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            self.screen.blit(final_score_text, score_rect)
            
            final_lines_text = self.small_font.render(f"Lines: {self.lines_cleared}  Level: {self.level}", True, (200, 200, 200))
            lines_rect = final_lines_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 30))
            self.screen.blit(final_lines_text, lines_rect)
            
            quit_text = self.small_font.render("Press ESC to quit", True, (150, 150, 150))
            quit_rect = quit_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 80))
            self.screen.blit(quit_text, quit_rect)
            
            pygame.display.flip()
            
            # Wait for quit
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        waiting = False
        
        pygame.quit()

if __name__ == "__main__":
    print("Hello, World!")
    print(f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nStarting Pygame Tetris game...")
    
    game = Tetris()
    game.run()