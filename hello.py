import random
import time
import os
from datetime import datetime

class Tetris:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        
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
        self.current_x = self.width // 2 - 2
        self.current_y = 0
        self.current_rotation = 0
        
    def get_new_piece(self):
        return random.randint(0, len(self.pieces) - 1)
    
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
    
    def display(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Create display board
        display_board = [row[:] for row in self.board]
        
        # Add current piece to display
        piece = self.pieces[self.current_piece][self.current_rotation]
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == '#':
                    board_x = self.current_x + x
                    board_y = self.current_y + y
                    if 0 <= board_y < self.height and 0 <= board_x < self.width:
                        display_board[board_y][board_x] = self.current_piece + 1
        
        print(f"Score: {self.score}  Level: {self.level}  Lines: {self.lines_cleared}")
        print("+" + "-" * self.width + "+")
        
        for row in display_board:
            line = "|"
            for cell in row:
                if cell == 0:
                    line += " "
                else:
                    line += "#"
            line += "|"
            print(line)
        
        print("+" + "-" * self.width + "+")
        print("Controls: A/D - move, S - drop, W - rotate, Q - quit")
    
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
    
    def run(self):
        print("Welcome to Console Tetris!")
        print("Starting in 3 seconds...")
        time.sleep(3)
        
        fall_time = 0
        fall_speed = max(1, 11 - self.level)
        
        while not self.game_over():
            self.display()
            
            # Simulate automatic falling
            fall_time += 1
            if fall_time >= fall_speed:
                if self.can_move(0, 1):
                    self.current_y += 1
                else:
                    self.place_piece()
                    self.clear_lines()
                    self.current_piece = self.get_new_piece()
                    self.current_x = self.width // 2 - 2
                    self.current_y = 0
                    self.current_rotation = 0
                    fall_speed = max(1, 11 - self.level)
                fall_time = 0
            
            # Simple input simulation (auto-play demo)
            time.sleep(0.5)
            
            # Random moves for demo
            if random.random() < 0.3:
                move = random.choice(['left', 'right', 'rotate', 'drop'])
                if move == 'left' and self.can_move(-1, 0):
                    self.current_x -= 1
                elif move == 'right' and self.can_move(1, 0):
                    self.current_x += 1
                elif move == 'rotate':
                    self.rotate_piece()
                elif move == 'drop':
                    self.drop_piece()
        
        print(f"\nGame Over! Final Score: {self.score}")
        print(f"Lines cleared: {self.lines_cleared}")
        print(f"Level reached: {self.level}")

if __name__ == "__main__":
    print("Hello, World!")
    print(f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nStarting Tetris game...")
    
    game = Tetris()
    game.run()