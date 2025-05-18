import pygame
import sys
import random
import time
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
PADDLE_WIDTH = 22
PADDLE_HEIGHT = 135
MIN_PADDLE_HEIGHT = 60
PADDLE_SHRINK_RATE = 8
BALL_SIZE = 22
PADDLE_SPEED = 8

# Enable alpha blending for transparency
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

# Bot difficulty settings
BOT_DIFFICULTY = {
    'EASY': {'speed': 4, 'reaction_delay': 0.3, 'prediction_error': 100},
    'MEDIUM': {'speed': 6, 'reaction_delay': 0.15, 'prediction_error': 50},
    'HARD': {'speed': 8, 'reaction_delay': 0.05, 'prediction_error': 20},
    'ULTRA': {'speed': 10, 'reaction_delay': 0, 'prediction_error': 5}
}

# UI Constants
RING_RADIUS = 25
RING_THICKNESS = 5
RING_SPACING = 180
RING_BOTTOM_MARGIN = 45
RING_START_X = 100
TEXT_OFFSET = 35

# Score options
SCORE_OPTIONS = {
    '1': 1,
    '2': 2,
    '3': 5,
    '4': 10,
    '5': 15,
    '6': 20,
    '7': 50,
    '8': float('inf')
}

# Ball acceleration
BALL_SPEED_INCREASE = 1.05
INITIAL_BALL_SPEED = 10

# Power-up constants
POWERUP_DURATION = 5
POWERUP_COOLDOWN = 10
POWERUP_MULTIPLIER = 1.5

# Speed power-up constants
SPEED_POWERUP_DURATION = 3
SPEED_POWERUP_COOLDOWN = 15
SPEED_MULTIPLIER = 2

# Reverse power-up constants
REVERSE_POWERUP_COOLDOWN = 30

# Slow-down power-up constants
SLOW_POWERUP_DURATION = 5
SLOW_POWERUP_COOLDOWN = 20
SLOW_MULTIPLIER = 0.7

# Chaos power-up constants
CHAOS_POWERUP_DURATION = 3
CHAOS_POWERUP_COOLDOWN = 30
CHAOS_SPEED_MULTIPLIER = 4
CHAOS_SIZE_MULTIPLIER = 0.75

# Powershot constants
POWERSHOT_COOLDOWN = 15  # seconds
POWERSHOT_MULTIPLIER = 3  # Triple speed

# Pinpoint constants
PINPOINT_COOLDOWN = 10  # seconds

# Stealth ability constants
STEALTH_DURATION = 2  # seconds
STEALTH_COOLDOWN = 15  # seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
DARK_BLUE = (0, 0, 139)
BRIGHT_RED = (255, 69, 0)

# Fire effect colors
FIRE_COLORS = [
    (255, 255, 0),    # Yellow core
    (255, 165, 0),    # Orange
    (255, 69, 0),     # Red-Orange
    (255, 0, 0)       # Red outer
]

# Fire effect constants
FIRE_MIN_SPEED = INITIAL_BALL_SPEED
FIRE_MAX_SPEED = INITIAL_BALL_SPEED * 3  # Adjust based on typical max speed
FIRE_MIN_PARTICLES = 2
FIRE_MAX_PARTICLES = 5

# Explosion effect constants
EXPLOSION_DURATION = 0.5  # seconds
EXPLOSION_MIN_RADIUS = 10
EXPLOSION_MAX_RADIUS = 60
EXPLOSION_PARTICLES = 8
EXPLOSION_COLORS = [
    (255, 255, 0),   # Yellow
    (255, 165, 0),   # Orange
    (255, 69, 0),    # Red-Orange
    (255, 0, 0)      # Red
]

# Available abilities
ABILITIES = {
    '1': ('Size-up', 'Increase paddle size by 50%'),
    '2': ('Speed-up', 'Double paddle speed'),
    '3': ('Reverse', 'Reverse ball direction'),
    '4': ('Slow-down', 'Slow opponent by 30%'),
    '5': ('Chaos', 'Make opponent 400% faster but 25% smaller'),
    '6': ('Powershot', 'Triple ball speed on next paddle hit'),
    '7': ('Stealth', 'Turn ball black for 2 seconds'),
    '8': ('Pinpoint', 'Align paddle with ball position')
}

# Default keybinds (will be customizable)
DEFAULT_P1_KEYBINDS = {
    '1': pygame.K_q,  # Size-up
    '2': pygame.K_e,  # Speed-up
    '3': pygame.K_a,  # Reverse
    '4': pygame.K_d,  # Slow-down
    '5': pygame.K_2,  # Chaos
    '6': pygame.K_3,  # Powershot
    '7': pygame.K_4,  # Stealth
    '8': pygame.K_5   # Pinpoint
}

DEFAULT_P2_KEYBINDS = {
    '1': pygame.K_LEFT,    # Size-up
    '2': pygame.K_RIGHT,   # Speed-up
    '3': pygame.K_SLASH,   # Reverse
    '4': pygame.K_PERIOD,  # Slow-down
    '5': pygame.K_QUOTE,   # Chaos
    '6': pygame.K_SEMICOLON,  # Powershot
    '7': pygame.K_l,       # Stealth
    '8': pygame.K_k        # Pinpoint
}

# Key name mapping for display
KEY_NAMES = {
    pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D',
    pygame.K_e: 'E', pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H',
    pygame.K_i: 'I', pygame.K_j: 'J', pygame.K_k: 'K', pygame.K_l: 'L',
    pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O', pygame.K_p: 'P',
    pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
    pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X',
    pygame.K_y: 'Y', pygame.K_z: 'Z', pygame.K_1: '1', pygame.K_2: '2',
    pygame.K_3: '3', pygame.K_4: '4', pygame.K_5: '5', pygame.K_6: '6',
    pygame.K_7: '7', pygame.K_8: '8', pygame.K_9: '9', pygame.K_0: '0',
    pygame.K_LEFT: 'Left', pygame.K_RIGHT: 'Right', pygame.K_UP: 'Up',
    pygame.K_DOWN: 'Down', pygame.K_SPACE: 'Space', pygame.K_RETURN: 'Enter',
    pygame.K_SLASH: '/', pygame.K_PERIOD: '.', pygame.K_COMMA: ',',
    pygame.K_QUOTE: "'", pygame.K_SEMICOLON: ';', pygame.K_MINUS: '-',
    pygame.K_EQUALS: '=', pygame.K_BACKQUOTE: '`', pygame.K_TAB: 'Tab'
}

# Fonts
large_font = pygame.font.Font(None, 111)
menu_font = pygame.font.Font(None, 54)
small_font = pygame.font.Font(None, 36)

def get_random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def draw_menu():
    screen.fill(BLACK)
    title = large_font.render("PONG", True, WHITE)
    one_player = menu_font.render("Press 1 for Single Player", True, WHITE)
    two_player = menu_font.render("Press 2 for Two Players", True, WHITE)
    
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
    screen.blit(one_player, (WINDOW_WIDTH//2 - one_player.get_width()//2, 300))
    screen.blit(two_player, (WINDOW_WIDTH//2 - two_player.get_width()//2, 350))
    pygame.display.flip()

def draw_speed_menu():
    screen.fill(BLACK)
    title = large_font.render("SELECT BALL SPEED", True, WHITE)
    super_slow = menu_font.render("Press 1 for Super Slow", True, WHITE)
    slow = menu_font.render("Press 2 for Slow", True, WHITE)
    medium = menu_font.render("Press 3 for Medium", True, WHITE)
    fast = menu_font.render("Press 4 for Fast", True, WHITE)
    super_fast = menu_font.render("Press 5 for Super Fast", True, WHITE)
    back = small_font.render("Press - to go back", True, WHITE)
    
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
    screen.blit(super_slow, (WINDOW_WIDTH//2 - super_slow.get_width()//2, 250))
    screen.blit(slow, (WINDOW_WIDTH//2 - slow.get_width()//2, 300))
    screen.blit(medium, (WINDOW_WIDTH//2 - medium.get_width()//2, 350))
    screen.blit(fast, (WINDOW_WIDTH//2 - fast.get_width()//2, 400))
    screen.blit(super_fast, (WINDOW_WIDTH//2 - super_fast.get_width()//2, 450))
    screen.blit(back, (WINDOW_WIDTH//2 - back.get_width()//2, 550))
    pygame.display.flip()

def draw_winner(winner_text):
    screen.fill(BLACK)
    text = large_font.render(winner_text, True, WHITE)
    play_again = menu_font.render("Press SPACE to play again", True, WHITE)
    quit_text = menu_font.render("Press ESC to quit", True, WHITE)
    
    screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 200))
    screen.blit(play_again, (WINDOW_WIDTH//2 - play_again.get_width()//2, 300))
    screen.blit(quit_text, (WINDOW_WIDTH//2 - quit_text.get_width()//2, 350))
    pygame.display.flip()

def draw_circle_arc(surface, color, center, radius, start_angle, stop_angle, width=1):
    """Draw a circular arc using pygame's draw.arc function"""
    rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
    pygame.draw.arc(surface, color, rect, start_angle, stop_angle, width)

def draw_ability_ring(surface, center_x, center_y, cooldown_percent, active_color, inactive_color, key_name, ability_name):
    """Draw a circular cooldown indicator with key and ability name"""
    # Calculate Y position from bottom of screen
    y_pos = WINDOW_HEIGHT - RING_BOTTOM_MARGIN
    
    # Draw the background ring
    draw_circle_arc(surface, GRAY, (center_x, y_pos), RING_RADIUS, 0, 2 * math.pi, RING_THICKNESS)
    
    if cooldown_percent > 0:
        # Draw the progress arc
        angle = 2 * math.pi * cooldown_percent
        draw_circle_arc(surface, active_color if cooldown_percent == 1 else inactive_color,
                       (center_x, y_pos), RING_RADIUS, -math.pi/2, -math.pi/2 + angle, RING_THICKNESS)
    
    # Draw the key binding
    key_text = small_font.render(key_name, True, WHITE)
    key_rect = key_text.get_rect(center=(center_x, y_pos))
    surface.blit(key_text, key_rect)
    
    # Draw the ability name above the ring
    ability_text = small_font.render(ability_name, True, WHITE)
    ability_rect = ability_text.get_rect(center=(center_x, y_pos - TEXT_OFFSET))
    surface.blit(ability_text, ability_rect)

def draw_ability_selection(player_num, selected_abilities, current_ability=None, waiting_for_key=False):
    screen.fill(BLACK)
    if waiting_for_key:
        title = large_font.render(f"Press a key for {ABILITIES[current_ability][0]}", True, WHITE)
    else:
        title = large_font.render(f"Player {player_num} Select Ability {len(selected_abilities) + 1}/3", True, WHITE)
        back = small_font.render("Press - to go back", True, WHITE)
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
    
    if not waiting_for_key:
        y_pos = 150
        for key, (name, desc) in ABILITIES.items():
            if key not in selected_abilities:
                ability_text = menu_font.render(f"{key}: {name} - {desc}", True, WHITE)
                screen.blit(ability_text, (WINDOW_WIDTH//2 - ability_text.get_width()//2, y_pos))
                y_pos += 50
        screen.blit(back, (WINDOW_WIDTH//2 - back.get_width()//2, y_pos + 50))
    
    pygame.display.flip()

def select_abilities(player_num):
    selected = []
    keybinds = {}
    default_keybinds = DEFAULT_P1_KEYBINDS if player_num == 1 else DEFAULT_P2_KEYBINDS
    
    while len(selected) < 3:
        draw_ability_selection(player_num, selected)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_MINUS and selected:  # Go back
                        selected.pop()
                        if selected:  # Remove last keybind if we have any abilities selected
                            last_ability = selected[-1]
                            del keybinds[last_ability]
                        waiting = False
                        break
                    key = event.unicode
                    if key in ABILITIES and key not in selected:
                        selected.append(key)
                        # Now wait for keybind
                        draw_ability_selection(player_num, selected, key, True)
                        waiting_for_key = True
                        while waiting_for_key:
                            for keybind_event in pygame.event.get():
                                if keybind_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if keybind_event.type == pygame.KEYDOWN:
                                    if keybind_event.key == pygame.K_MINUS:  # Don't allow minus key
                                        continue
                                    if keybind_event.key in KEY_NAMES:
                                        keybinds[key] = keybind_event.key
                                        waiting_for_key = False
                                        waiting = False
                                    elif keybind_event.key == pygame.K_ESCAPE:
                                        # Use default keybind if ESC is pressed
                                        keybinds[key] = default_keybinds[key]
                                        waiting_for_key = False
                                        waiting = False
    return selected, keybinds

def draw_score_selection():
    screen.fill(BLACK)
    title = large_font.render("SELECT WINNING SCORE", True, WHITE)
    back = small_font.render("Press - to go back", True, WHITE)
    
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
    
    y_pos = 150
    for key, score in SCORE_OPTIONS.items():
        score_text = "Infinite" if score == float('inf') else str(score)
        text = menu_font.render(f"{key}: {score_text} points", True, WHITE)
        screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, y_pos))
        y_pos += 50
    
    screen.blit(back, (WINDOW_WIDTH//2 - back.get_width()//2, y_pos + 50))
    pygame.display.flip()

def countdown_timer():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        count_text = large_font.render(str(i), True, WHITE)
        screen.blit(count_text, (WINDOW_WIDTH//2 - count_text.get_width()//2, 
                                WINDOW_HEIGHT//2 - count_text.get_height()//2))
        pygame.display.flip()
        time.sleep(1)
    
    screen.fill(BLACK)
    go_text = large_font.render("GO!", True, WHITE)
    screen.blit(go_text, (WINDOW_WIDTH//2 - go_text.get_width()//2, 
                         WINDOW_HEIGHT//2 - go_text.get_height()//2))
    pygame.display.flip()
    time.sleep(0.5)

def draw_difficulty_menu():
    screen.fill(BLACK)
    title = large_font.render("SELECT BOT DIFFICULTY", True, WHITE)
    easy = menu_font.render("Press 1 for Easy", True, WHITE)
    medium = menu_font.render("Press 2 for Medium", True, WHITE)
    hard = menu_font.render("Press 3 for Hard", True, WHITE)
    ultra = menu_font.render("Press 4 for Ultra Hard", True, WHITE)
    back = small_font.render("Press - to go back", True, WHITE)
    
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
    screen.blit(easy, (WINDOW_WIDTH//2 - easy.get_width()//2, 250))
    screen.blit(medium, (WINDOW_WIDTH//2 - medium.get_width()//2, 300))
    screen.blit(hard, (WINDOW_WIDTH//2 - hard.get_width()//2, 350))
    screen.blit(ultra, (WINDOW_WIDTH//2 - ultra.get_width()//2, 400))
    screen.blit(back, (WINDOW_WIDTH//2 - back.get_width()//2, 500))
    pygame.display.flip()

def draw_mode_menu():
    screen.fill(BLACK)
    title = large_font.render("SELECT GAME MODE", True, WHITE)
    normal = menu_font.render("Press 1 for Normal Mode", True, WHITE)
    shatter = menu_font.render("Press 2 for Shatter Mode", True, WHITE)
    description = small_font.render("In Shatter Mode, paddles shrink by 5% on each hit!", True, WHITE)
    
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
    screen.blit(normal, (WINDOW_WIDTH//2 - normal.get_width()//2, 300))
    screen.blit(shatter, (WINDOW_WIDTH//2 - shatter.get_width()//2, 350))
    screen.blit(description, (WINDOW_WIDTH//2 - description.get_width()//2, 450))
    pygame.display.flip()

def draw_paddle_shrink_menu():
    screen.fill(BLACK)
    title = large_font.render("PADDLE SHRINK ON POINT", True, WHITE)
    enable = menu_font.render("Press 1 to Enable", True, WHITE)
    disable = menu_font.render("Press 2 to Disable", True, WHITE)
    back = small_font.render("Press - to go back", True, WHITE)
    
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
    screen.blit(enable, (WINDOW_WIDTH//2 - enable.get_width()//2, 300))
    screen.blit(disable, (WINDOW_WIDTH//2 - disable.get_width()//2, 350))
    screen.blit(back, (WINDOW_WIDTH//2 - back.get_width()//2, 450))
    pygame.display.flip()

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_time = time.time()
        self.particles = []
        
        # Create particles with random angles
        for _ in range(EXPLOSION_PARTICLES):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 2)
            self.particles.append({
                'angle': angle,
                'speed': speed,
                'size': EXPLOSION_MIN_RADIUS,
                'x': self.x,  # Initialize position
                'y': self.y
            })
    
    def update(self):
        current_time = time.time()
        progress = (current_time - self.start_time) / EXPLOSION_DURATION
        
        if progress >= 1:
            return True  # Explosion is complete
        
        # Update each particle
        for particle in self.particles:
            # Expand size
            particle['size'] = EXPLOSION_MIN_RADIUS + (EXPLOSION_MAX_RADIUS - EXPLOSION_MIN_RADIUS) * progress
            
            # Move particle outward
            distance = particle['speed'] * progress * EXPLOSION_MAX_RADIUS
            particle['x'] = self.x + math.cos(particle['angle']) * distance
            particle['y'] = self.y + math.sin(particle['angle']) * distance
        
        return False
    
    def draw(self, surface):
        current_time = time.time()
        progress = (current_time - self.start_time) / EXPLOSION_DURATION
        
        if progress >= 1:
            return
        
        for particle in self.particles:
            try:
                # Calculate alpha based on progress (fade out)
                alpha = int(255 * (1 - progress))
                
                # Skip if particle is completely transparent
                if alpha <= 0:
                    continue
                    
                # Create surface for the particle with alpha channel
                size = int(particle['size'] * 2)
                if size <= 0:  # Skip if size is invalid
                    continue
                    
                particle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                
                # Draw multiple circles with different colors and sizes for each particle
                for i, color in enumerate(EXPLOSION_COLORS):
                    size_factor = 1 - (i * 0.2)  # Each inner circle is slightly smaller
                    radius = int(particle['size'] * size_factor)
                    if radius <= 0:  # Skip if radius is invalid
                        continue
                    particle_color = (*color, alpha)
                    pygame.draw.circle(particle_surface, particle_color, 
                                     (int(particle['size']), int(particle['size'])), radius)
                
                # Draw the particle surface
                surface.blit(particle_surface, 
                           (int(particle['x'] - particle['size']),
                            int(particle['y'] - particle['size'])))
            except (pygame.error, TypeError, ValueError) as e:
                continue  # Skip this particle if any error occurs

class PongGame:
    def __init__(self, two_player_mode=False, ball_speed=INITIAL_BALL_SPEED, winning_score=10, bot_difficulty='MEDIUM', paddle_shrink_enabled=True):
        self.two_player_mode = two_player_mode
        self.initial_ball_speed = ball_speed
        self.current_ball_speed = ball_speed
        self.player_color = WHITE
        self.opponent_color = WHITE
        self.ball_color = WHITE
        self.player_height = PADDLE_HEIGHT
        self.opponent_height = PADDLE_HEIGHT
        self.winning_score = winning_score
        self.bot_difficulty = bot_difficulty
        self.paddle_shrink_enabled = paddle_shrink_enabled
        self.last_ai_update = time.time()
        self.target_y = None
        self.last_ai_ability_check = time.time()
        self.active_explosions = []  # List to track active explosions
        
        # Initialize scores
        self.player_score = 0
        self.opponent_score = 0
        
        # Get player abilities and keybinds
        self.player_abilities, self.player_keybinds = select_abilities(1)
        if two_player_mode:
            self.opponent_abilities, self.opponent_keybinds = select_abilities(2)
        else:
            available_abilities = list(ABILITIES.keys())
            self.opponent_abilities = random.sample(available_abilities, 3)
            self.opponent_keybinds = {ability: pygame.K_0 for ability in self.opponent_abilities}
        
        # Power-up states
        self.reset_powerup_states()
        self.reset_game()

    def reset_powerup_states(self):
        # Size power-up state
        self.player_powerup_active = False
        self.opponent_powerup_active = False
        self.player_powerup_start = 0
        self.opponent_powerup_start = 0
        self.player_last_powerup = 0
        self.opponent_last_powerup = 0
        
        # Speed power-up state
        self.player_speed_powerup_active = False
        self.opponent_speed_powerup_active = False
        self.player_speed_powerup_start = 0
        self.opponent_speed_powerup_start = 0
        self.player_last_speed_powerup = 0
        self.opponent_last_speed_powerup = 0

        # Reverse power-up state
        self.player_last_reverse = 0
        self.opponent_last_reverse = 0

        # Slow-down power-up state
        self.player_slow_active = False
        self.opponent_slow_active = False
        self.player_slow_start = 0
        self.opponent_slow_start = 0
        self.player_last_slow = 0
        self.opponent_last_slow = 0

        # Chaos power-up state
        self.player_chaos_active = False
        self.opponent_chaos_active = False
        self.player_chaos_start = 0
        self.opponent_chaos_start = 0
        self.player_last_chaos = 0
        self.opponent_last_chaos = 0
        self.player_original_height = self.player_height
        self.opponent_original_height = self.opponent_height

        # Powershot state
        self.player_powershot_active = False
        self.opponent_powershot_active = False
        self.player_last_powershot = 0
        self.opponent_last_powershot = 0

        # Stealth state
        self.player_stealth_active = False
        self.opponent_stealth_active = False
        self.player_stealth_start = 0
        self.opponent_stealth_start = 0
        self.player_last_stealth = 0
        self.opponent_last_stealth = 0

        # Pinpoint state
        self.player_last_pinpoint = 0
        self.opponent_last_pinpoint = 0

    def reset_game(self):
        # Create game objects
        self.player = pygame.Rect(50, WINDOW_HEIGHT//2 - self.player_height//2, 
                                PADDLE_WIDTH, self.player_height)
        self.opponent = pygame.Rect(WINDOW_WIDTH - 50 - PADDLE_WIDTH, 
                                  WINDOW_HEIGHT//2 - self.opponent_height//2, 
                                  PADDLE_WIDTH, self.opponent_height)
        self.ball = pygame.Rect(WINDOW_WIDTH//2 - BALL_SIZE//2, 
                              WINDOW_HEIGHT//2 - BALL_SIZE//2, 
                              BALL_SIZE, BALL_SIZE)
        
        # Reset ball speed to initial value
        self.current_ball_speed = self.initial_ball_speed
        self.ball_speed_x = self.current_ball_speed * random.choice((1, -1))
        self.ball_speed_y = self.current_ball_speed * random.choice((1, -1))
        
        # Reset ball color
        self.ball_color = WHITE
        
        # Change paddle colors
        self.player_color = get_random_color()
        self.opponent_color = get_random_color()
        
        # Clear any active explosions
        self.active_explosions = []

    def activate_powerup(self, is_player):
        current_time = time.time()
        if is_player:
            if not self.player_powerup_active and current_time - self.player_last_powerup >= POWERUP_COOLDOWN:
                self.player_powerup_active = True
                self.player_powerup_start = current_time
                self.player_last_powerup = current_time
                self.player.height = int(self.player_height * POWERUP_MULTIPLIER)
        else:
            if not self.opponent_powerup_active and current_time - self.opponent_last_powerup >= POWERUP_COOLDOWN:
                self.opponent_powerup_active = True
                self.opponent_powerup_start = current_time
                self.opponent_last_powerup = current_time
                self.opponent.height = int(self.opponent_height * POWERUP_MULTIPLIER)

    def activate_speed_powerup(self, is_player):
        current_time = time.time()
        if is_player:
            if not self.player_speed_powerup_active and current_time - self.player_last_speed_powerup >= SPEED_POWERUP_COOLDOWN:
                self.player_speed_powerup_active = True
                self.player_speed_powerup_start = current_time
                self.player_last_speed_powerup = current_time
        else:
            if not self.opponent_speed_powerup_active and current_time - self.opponent_last_speed_powerup >= SPEED_POWERUP_COOLDOWN:
                self.opponent_speed_powerup_active = True
                self.opponent_speed_powerup_start = current_time
                self.opponent_last_speed_powerup = current_time

    def activate_reverse_powerup(self, is_player):
        current_time = time.time()
        if is_player:
            if current_time - self.player_last_reverse >= REVERSE_POWERUP_COOLDOWN:
                self.ball_speed_x *= -1
                self.ball_speed_y *= -1
                self.player_last_reverse = current_time
        else:
            if current_time - self.opponent_last_reverse >= REVERSE_POWERUP_COOLDOWN:
                self.ball_speed_x *= -1
                self.ball_speed_y *= -1
                self.opponent_last_reverse = current_time

    def activate_slow_powerup(self, is_player):
        current_time = time.time()
        if is_player:
            if not self.player_slow_active and current_time - self.player_last_slow >= SLOW_POWERUP_COOLDOWN:
                self.opponent_slow_active = True
                self.player_slow_start = current_time
                self.player_last_slow = current_time
                self.opponent_color = BLUE
        else:
            if not self.opponent_slow_active and current_time - self.opponent_last_slow >= SLOW_POWERUP_COOLDOWN:
                self.player_slow_active = True
                self.opponent_slow_start = current_time
                self.opponent_last_slow = current_time
                self.player_color = BLUE

    def activate_chaos_powerup(self, is_player):
        current_time = time.time()
        if is_player:
            if not self.opponent_chaos_active and current_time - self.player_last_chaos >= CHAOS_POWERUP_COOLDOWN:
                self.opponent_chaos_active = True
                self.player_chaos_start = current_time
                self.player_last_chaos = current_time
                # Reduce opponent's paddle size
                self.opponent.height = int(self.opponent_height * CHAOS_SIZE_MULTIPLIER)
        else:
            if not self.player_chaos_active and current_time - self.opponent_last_chaos >= CHAOS_POWERUP_COOLDOWN:
                self.player_chaos_active = True
                self.opponent_chaos_start = current_time
                self.opponent_last_chaos = current_time
                # Reduce player's paddle size
                self.player.height = int(self.player_height * CHAOS_SIZE_MULTIPLIER)

    def activate_powershot(self, is_player):
        current_time = time.time()
        if is_player:
            if not self.player_powershot_active and current_time - self.player_last_powershot >= POWERSHOT_COOLDOWN:
                self.player_powershot_active = True
                self.player_last_powershot = current_time
        else:
            if not self.opponent_powershot_active and current_time - self.opponent_last_powershot >= POWERSHOT_COOLDOWN:
                self.opponent_powershot_active = True
                self.opponent_last_powershot = current_time

    def activate_stealth(self, is_player):
        current_time = time.time()
        if is_player:
            if not self.player_stealth_active and current_time - self.player_last_stealth >= STEALTH_COOLDOWN:
                self.player_stealth_active = True
                self.player_stealth_start = current_time
                self.player_last_stealth = current_time
                self.ball_color = BLACK
        else:
            if not self.opponent_stealth_active and current_time - self.opponent_last_stealth >= STEALTH_COOLDOWN:
                self.opponent_stealth_active = True
                self.opponent_stealth_start = current_time
                self.opponent_last_stealth = current_time
                self.ball_color = BLACK

    def activate_pinpoint(self, is_player):
        current_time = time.time()
        if is_player:
            if current_time - self.player_last_pinpoint >= PINPOINT_COOLDOWN:
                # Align player paddle with ball's y position
                self.player.centery = self.ball.centery
                # Keep paddle within screen bounds
                if self.player.top < 0:
                    self.player.top = 0
                if self.player.bottom > WINDOW_HEIGHT:
                    self.player.bottom = WINDOW_HEIGHT
                self.player_last_pinpoint = current_time
        else:
            if current_time - self.opponent_last_pinpoint >= PINPOINT_COOLDOWN:
                # Align opponent paddle with ball's y position
                self.opponent.centery = self.ball.centery
                # Keep paddle within screen bounds
                if self.opponent.top < 0:
                    self.opponent.top = 0
                if self.opponent.bottom > WINDOW_HEIGHT:
                    self.opponent.bottom = WINDOW_HEIGHT
                self.opponent_last_pinpoint = current_time

    def update_powerups(self):
        current_time = time.time()
        
        # Update size powerup
        if self.player_powerup_active and current_time - self.player_powerup_start >= POWERUP_DURATION:
            self.player_powerup_active = False
            self.player.height = self.player_height
            
        if self.opponent_powerup_active and current_time - self.opponent_powerup_start >= POWERUP_DURATION:
            self.opponent_powerup_active = False
            self.opponent.height = self.opponent_height

        # Update speed powerup
        if self.player_speed_powerup_active and current_time - self.player_speed_powerup_start >= SPEED_POWERUP_DURATION:
            self.player_speed_powerup_active = False
            
        if self.opponent_speed_powerup_active and current_time - self.opponent_speed_powerup_start >= SPEED_POWERUP_DURATION:
            self.opponent_speed_powerup_active = False

        # Update slow powerup
        if self.player_slow_active and current_time - self.player_slow_start >= SLOW_POWERUP_DURATION:
            self.player_slow_active = False
            self.player_color = WHITE
            
        if self.opponent_slow_active and current_time - self.opponent_slow_start >= SLOW_POWERUP_DURATION:
            self.opponent_slow_active = False
            self.opponent_color = WHITE

        # Update chaos powerup
        if self.player_chaos_active and current_time - self.opponent_chaos_start >= CHAOS_POWERUP_DURATION:
            self.player_chaos_active = False
            self.player.height = self.player_height
            
        if self.opponent_chaos_active and current_time - self.player_chaos_start >= CHAOS_POWERUP_DURATION:
            self.opponent_chaos_active = False
            self.opponent.height = self.opponent_height

        # Update stealth powerup
        if self.player_stealth_active and current_time - self.player_stealth_start >= STEALTH_DURATION:
            self.player_stealth_active = False
            if not self.opponent_stealth_active:  # Only reset color if opponent's stealth isn't active
                self.ball_color = WHITE
                
        if self.opponent_stealth_active and current_time - self.opponent_stealth_start >= STEALTH_DURATION:
            self.opponent_stealth_active = False
            if not self.player_stealth_active:  # Only reset color if player's stealth isn't active
                self.ball_color = WHITE

    def draw_powerup_meters(self):
        current_time = time.time()
        
        # Calculate the number of abilities for proper spacing
        p1_abilities = sum(1 for x in ['1', '2', '3', '4', '5', '6', '7', '8'] if x in self.player_abilities)
        p2_abilities = sum(1 for x in ['1', '2', '3', '4', '5', '6', '7', '8'] if x in self.opponent_abilities)
        
        # Calculate starting positions to center the groups of abilities
        p1_total_width = (p1_abilities - 1) * RING_SPACING
        p1_start_x = RING_START_X
        
        p2_total_width = (p2_abilities - 1) * RING_SPACING
        p2_start_x = WINDOW_WIDTH - RING_START_X - p2_total_width
        
        # Draw Player 1 abilities
        x_pos = p1_start_x
        if '1' in self.player_abilities:
            self.draw_size_meter(current_time, True, x_pos)
            x_pos += RING_SPACING
        if '2' in self.player_abilities:
            self.draw_speed_meter(current_time, True, x_pos)
            x_pos += RING_SPACING
        if '3' in self.player_abilities:
            self.draw_reverse_meter(current_time, True, x_pos)
            x_pos += RING_SPACING
        if '4' in self.player_abilities:
            self.draw_slow_meter(current_time, True, x_pos)
            x_pos += RING_SPACING
        if '5' in self.player_abilities:
            self.draw_chaos_meter(current_time, True, x_pos)
            x_pos += RING_SPACING
        if '6' in self.player_abilities:
            self.draw_powershot_meter(current_time, True, x_pos)
            x_pos += RING_SPACING
        if '7' in self.player_abilities:
            self.draw_stealth_meter(current_time, True, x_pos)
            x_pos += RING_SPACING
        if '8' in self.player_abilities:
            self.draw_pinpoint_meter(current_time, True, x_pos)
        
        # Draw Player 2/Bot abilities
        x_pos = p2_start_x
        if '1' in self.opponent_abilities:
            key_name = "BOT" if not self.two_player_mode else KEY_NAMES[self.opponent_keybinds['1']]
            self.draw_size_meter(current_time, False, x_pos, key_name)
            x_pos += RING_SPACING
        if '2' in self.opponent_abilities:
            key_name = "BOT" if not self.two_player_mode else KEY_NAMES[self.opponent_keybinds['2']]
            self.draw_speed_meter(current_time, False, x_pos, key_name)
            x_pos += RING_SPACING
        if '3' in self.opponent_abilities:
            key_name = "BOT" if not self.two_player_mode else KEY_NAMES[self.opponent_keybinds['3']]
            self.draw_reverse_meter(current_time, False, x_pos, key_name)
            x_pos += RING_SPACING
        if '4' in self.opponent_abilities:
            key_name = "BOT" if not self.two_player_mode else KEY_NAMES[self.opponent_keybinds['4']]
            self.draw_slow_meter(current_time, False, x_pos, key_name)
            x_pos += RING_SPACING
        if '5' in self.opponent_abilities:
            key_name = "BOT" if not self.two_player_mode else KEY_NAMES[self.opponent_keybinds['5']]
            self.draw_chaos_meter(current_time, False, x_pos, key_name)
            x_pos += RING_SPACING
        if '6' in self.opponent_abilities:
            key_name = "BOT" if not self.two_player_mode else KEY_NAMES[self.opponent_keybinds['6']]
            self.draw_powershot_meter(current_time, False, x_pos, key_name)
            x_pos += RING_SPACING
        if '7' in self.opponent_abilities:
            key_name = "BOT" if not self.two_player_mode else KEY_NAMES[self.opponent_keybinds['7']]
            self.draw_stealth_meter(current_time, False, x_pos, key_name)
            x_pos += RING_SPACING
        if '8' in self.opponent_abilities:
            key_name = "BOT" if not self.two_player_mode else KEY_NAMES[self.opponent_keybinds['8']]
            self.draw_pinpoint_meter(current_time, False, x_pos, key_name)

    def draw_size_meter(self, current_time, is_player, x_pos, key_name=None):
        if is_player:
            cooldown_remaining = max(0, POWERUP_COOLDOWN - (current_time - self.player_last_powerup))
            cooldown_percent = (POWERUP_COOLDOWN - cooldown_remaining) / POWERUP_COOLDOWN
            key_name = KEY_NAMES[self.player_keybinds['1']]
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GREEN, RED, key_name, "Size-up")
        else:
            cooldown_remaining = max(0, POWERUP_COOLDOWN - (current_time - self.opponent_last_powerup))
            cooldown_percent = (POWERUP_COOLDOWN - cooldown_remaining) / POWERUP_COOLDOWN
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GREEN, RED, key_name, "Size-up")

    def draw_speed_meter(self, current_time, is_player, x_pos, key_name=None):
        if is_player:
            cooldown_remaining = max(0, SPEED_POWERUP_COOLDOWN - (current_time - self.player_last_speed_powerup))
            cooldown_percent = (SPEED_POWERUP_COOLDOWN - cooldown_remaining) / SPEED_POWERUP_COOLDOWN
            key_name = KEY_NAMES[self.player_keybinds['2']]
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            BLUE, ORANGE, key_name, "Speed-up")
        else:
            cooldown_remaining = max(0, SPEED_POWERUP_COOLDOWN - (current_time - self.opponent_last_speed_powerup))
            cooldown_percent = (SPEED_POWERUP_COOLDOWN - cooldown_remaining) / SPEED_POWERUP_COOLDOWN
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            BLUE, ORANGE, key_name, "Speed-up")

    def draw_reverse_meter(self, current_time, is_player, x_pos, key_name=None):
        if is_player:
            cooldown_remaining = max(0, REVERSE_POWERUP_COOLDOWN - (current_time - self.player_last_reverse))
            cooldown_percent = (REVERSE_POWERUP_COOLDOWN - cooldown_remaining) / REVERSE_POWERUP_COOLDOWN
            key_name = KEY_NAMES[self.player_keybinds['3']]
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            YELLOW, PINK, key_name, "Reverse")
        else:
            cooldown_remaining = max(0, REVERSE_POWERUP_COOLDOWN - (current_time - self.opponent_last_reverse))
            cooldown_percent = (REVERSE_POWERUP_COOLDOWN - cooldown_remaining) / REVERSE_POWERUP_COOLDOWN
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            YELLOW, PINK, key_name, "Reverse")

    def draw_slow_meter(self, current_time, is_player, x_pos, key_name=None):
        if is_player:
            cooldown_remaining = max(0, SLOW_POWERUP_COOLDOWN - (current_time - self.player_last_slow))
            cooldown_percent = (SLOW_POWERUP_COOLDOWN - cooldown_remaining) / SLOW_POWERUP_COOLDOWN
            key_name = KEY_NAMES[self.player_keybinds['4']]
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            DARK_BLUE, BRIGHT_RED, key_name, "Slow-down")
        else:
            cooldown_remaining = max(0, SLOW_POWERUP_COOLDOWN - (current_time - self.opponent_last_slow))
            cooldown_percent = (SLOW_POWERUP_COOLDOWN - cooldown_remaining) / SLOW_POWERUP_COOLDOWN
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            DARK_BLUE, BRIGHT_RED, key_name, "Slow-down")

    def draw_chaos_meter(self, current_time, is_player, x_pos, key_name=None):
        if is_player:
            cooldown_remaining = max(0, CHAOS_POWERUP_COOLDOWN - (current_time - self.player_last_chaos))
            cooldown_percent = (CHAOS_POWERUP_COOLDOWN - cooldown_remaining) / CHAOS_POWERUP_COOLDOWN
            key_name = KEY_NAMES[self.player_keybinds['5']]
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GREEN, RED, key_name, "Chaos")
        else:
            cooldown_remaining = max(0, CHAOS_POWERUP_COOLDOWN - (current_time - self.opponent_last_chaos))
            cooldown_percent = (CHAOS_POWERUP_COOLDOWN - cooldown_remaining) / CHAOS_POWERUP_COOLDOWN
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GREEN, RED, key_name, "Chaos")

    def draw_powershot_meter(self, current_time, is_player, x_pos, key_name=None):
        if is_player:
            cooldown_remaining = max(0, POWERSHOT_COOLDOWN - (current_time - self.player_last_powershot))
            cooldown_percent = (POWERSHOT_COOLDOWN - cooldown_remaining) / POWERSHOT_COOLDOWN
            key_name = KEY_NAMES[self.player_keybinds['6']]
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GREEN, RED, key_name, "Powershot")
        else:
            cooldown_remaining = max(0, POWERSHOT_COOLDOWN - (current_time - self.opponent_last_powershot))
            cooldown_percent = (POWERSHOT_COOLDOWN - cooldown_remaining) / POWERSHOT_COOLDOWN
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GREEN, RED, key_name, "Powershot")

    def draw_stealth_meter(self, current_time, is_player, x_pos, key_name=None):
        if is_player:
            cooldown_remaining = max(0, STEALTH_COOLDOWN - (current_time - self.player_last_stealth))
            cooldown_percent = (STEALTH_COOLDOWN - cooldown_remaining) / STEALTH_COOLDOWN
            key_name = KEY_NAMES[self.player_keybinds['7']]
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GRAY, RED, key_name, "Stealth")
        else:
            cooldown_remaining = max(0, STEALTH_COOLDOWN - (current_time - self.opponent_last_stealth))
            cooldown_percent = (STEALTH_COOLDOWN - cooldown_remaining) / STEALTH_COOLDOWN
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GRAY, RED, key_name, "Stealth")

    def draw_pinpoint_meter(self, current_time, is_player, x_pos, key_name=None):
        if is_player:
            cooldown_remaining = max(0, PINPOINT_COOLDOWN - (current_time - self.player_last_pinpoint))
            cooldown_percent = (PINPOINT_COOLDOWN - cooldown_remaining) / PINPOINT_COOLDOWN
            key_name = KEY_NAMES[self.player_keybinds['8']]
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GREEN, RED, key_name, "Pinpoint")
        else:
            cooldown_remaining = max(0, PINPOINT_COOLDOWN - (current_time - self.opponent_last_pinpoint))
            cooldown_percent = (PINPOINT_COOLDOWN - cooldown_remaining) / PINPOINT_COOLDOWN
            draw_ability_ring(screen, x_pos, 0, cooldown_percent,
                            GREEN, RED, key_name, "Pinpoint")

    def shrink_paddle(self, is_player):
        if not self.paddle_shrink_enabled:
            return
            
        if is_player:
            self.player_height = max(MIN_PADDLE_HEIGHT, 
                                   self.player_height - PADDLE_SHRINK_RATE)
            if not self.player_powerup_active:
                self.player.height = self.player_height
        else:
            self.opponent_height = max(MIN_PADDLE_HEIGHT, 
                                     self.opponent_height - PADDLE_SHRINK_RATE)
            if not self.opponent_powerup_active:
                self.opponent.height = self.opponent_height

    def reset_ball(self):
        self.ball.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        # Reset ball speed to initial value
        self.current_ball_speed = self.initial_ball_speed
        self.ball_speed_y = self.current_ball_speed * random.choice((1, -1))
        self.ball_speed_x = self.current_ball_speed * random.choice((1, -1))
        # Reset ball color
        self.ball_color = WHITE
        # Change paddle colors
        self.player_color = get_random_color()
        self.opponent_color = get_random_color()

    def increase_ball_speed(self):
        # Increase the current ball speed
        self.current_ball_speed *= BALL_SPEED_INCREASE
        
        # Maintain the direction but update the speed
        self.ball_speed_x = abs(self.ball_speed_x) * (1 if self.ball_speed_x > 0 else -1)
        self.ball_speed_y = abs(self.ball_speed_y) * (1 if self.ball_speed_y > 0 else -1)
        
        # Apply the new speed while maintaining direction
        self.ball_speed_x = self.current_ball_speed * (1 if self.ball_speed_x > 0 else -1)
        self.ball_speed_y = self.current_ball_speed * (1 if self.ball_speed_y > 0 else -1)

    def move_paddle(self, paddle, up=True):
        speed = PADDLE_SPEED
        if (paddle == self.player and self.player_speed_powerup_active) or \
           (paddle == self.opponent and self.opponent_speed_powerup_active):
            speed *= SPEED_MULTIPLIER
        if (paddle == self.player and self.player_slow_active) or \
           (paddle == self.opponent and self.opponent_slow_active):
            speed *= SLOW_MULTIPLIER
        if (paddle == self.player and self.player_chaos_active) or \
           (paddle == self.opponent and self.opponent_chaos_active):
            speed *= CHAOS_SPEED_MULTIPLIER
            
        if up and paddle.top > 0:
            paddle.y -= speed
        if not up and paddle.bottom < WINDOW_HEIGHT:
            paddle.y += speed

    def update_explosions(self):
        # Update explosions and remove completed ones
        self.active_explosions = [exp for exp in self.active_explosions if not exp.update()]
    
    def draw_explosions(self, surface):
        # Draw all active explosions
        for explosion in self.active_explosions:
            try:
                explosion.draw(surface)
            except (pygame.error, TypeError, ValueError):
                continue  # Skip drawing if there's an error

    def ball_movement(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # Ball collision with top and bottom
        if self.ball.top <= 0 or self.ball.bottom >= WINDOW_HEIGHT:
            self.ball_speed_y *= -1

        # Ball collision with paddles
        if self.ball.colliderect(self.player):
            self.ball_speed_x *= -1
            if self.player_powershot_active:
                self.ball_speed_x *= POWERSHOT_MULTIPLIER
                self.ball_speed_y *= POWERSHOT_MULTIPLIER
                self.player_powershot_active = False
                try:
                    # Create explosion effect at collision point
                    explosion_x = self.player.right
                    explosion_y = self.ball.centery
                    self.active_explosions.append(Explosion(explosion_x, explosion_y))
                except (pygame.error, TypeError, ValueError):
                    pass  # Skip explosion creation if there's an error
            else:
                self.increase_ball_speed()

        if self.ball.colliderect(self.opponent):
            self.ball_speed_x *= -1
            if self.opponent_powershot_active:
                self.ball_speed_x *= POWERSHOT_MULTIPLIER
                self.ball_speed_y *= POWERSHOT_MULTIPLIER
                self.opponent_powershot_active = False
                try:
                    # Create explosion effect at collision point
                    explosion_x = self.opponent.left
                    explosion_y = self.ball.centery
                    self.active_explosions.append(Explosion(explosion_x, explosion_y))
                except (pygame.error, TypeError, ValueError):
                    pass  # Skip explosion creation if there's an error
            else:
                self.increase_ball_speed()

        # Score points and shrink paddles
        if self.ball.left <= 0:
            if self.opponent_score < self.winning_score:  # Only increment if not at winning score
                self.opponent_score += 1
                self.shrink_paddle(False)
            self.reset_ball()
            
        if self.ball.right >= WINDOW_WIDTH:
            if self.player_score < self.winning_score:  # Only increment if not at winning score
                self.player_score += 1
                self.shrink_paddle(True)
            self.reset_ball()

    def check_ai_ability_usage(self):
        current_time = time.time()
        difficulty_settings = BOT_DIFFICULTY[self.bot_difficulty]
        
        # Increase minimum time between ability checks (in seconds)
        min_check_delay = {
            'EASY': 3.0,
            'MEDIUM': 2.5,
            'HARD': 1.5,    # Reduced delay for faster reactions
            'ULTRA': 0.75   # Even faster reactions for Ultra
        }
        
        if current_time - self.last_ai_ability_check < min_check_delay[self.bot_difficulty]:
            return
        
        self.last_ai_ability_check = current_time
        
        # Adjust chance to use abilities based on difficulty
        chance_to_use = {
            'EASY': 0.15,    # ~1 ability every 20 seconds
            'MEDIUM': 0.25,  # ~1 ability every 10 seconds
            'HARD': 0.40,    # Increased from 0.35
            'ULTRA': 0.55    # Increased from 0.45
        }
        
        if random.random() < chance_to_use[self.bot_difficulty]:
            # Randomly select an available ability that's off cooldown
            available_abilities = []
            
            for ability in self.opponent_abilities:
                if ability == '1' and current_time - self.opponent_last_powerup >= POWERUP_COOLDOWN:
                    available_abilities.append(('1', self.activate_powerup))
                elif ability == '2' and current_time - self.opponent_last_speed_powerup >= SPEED_POWERUP_COOLDOWN:
                    available_abilities.append(('2', self.activate_speed_powerup))
                elif ability == '3' and current_time - self.opponent_last_reverse >= REVERSE_POWERUP_COOLDOWN:
                    available_abilities.append(('3', self.activate_reverse_powerup))
                elif ability == '4' and current_time - self.opponent_last_slow >= SLOW_POWERUP_COOLDOWN:
                    available_abilities.append(('4', self.activate_slow_powerup))
                elif ability == '5' and current_time - self.opponent_last_chaos >= CHAOS_POWERUP_COOLDOWN:
                    available_abilities.append(('5', self.activate_chaos_powerup))
                elif ability == '6' and current_time - self.opponent_last_powershot >= POWERSHOT_COOLDOWN:
                    available_abilities.append(('6', self.activate_powershot))
                elif ability == '7' and current_time - self.opponent_last_stealth >= STEALTH_COOLDOWN:
                    available_abilities.append(('7', self.activate_stealth))
                elif ability == '8' and current_time - self.opponent_last_pinpoint >= PINPOINT_COOLDOWN:
                    available_abilities.append(('8', self.activate_pinpoint))
            
            if available_abilities and self.bot_difficulty in ['HARD', 'ULTRA']:
                # Advanced strategic selection for Hard and Ultra difficulties
                best_ability = None
                best_score = -1
                
                for ability_id, activate_func in available_abilities:
                    score = 0
                    
                    # Size-up (1)
                    if ability_id == '1':
                        # Higher priority when:
                        # - Paddle is small
                        # - Ball is approaching at high speed
                        # - Score is close or losing
                        if self.opponent.height <= PADDLE_HEIGHT * 0.8:
                            score += 3
                        if self.ball_speed_x > 0 and abs(self.ball_speed_x) > self.initial_ball_speed * 1.5:
                            score += 2
                        if self.ball.centerx > WINDOW_WIDTH * 0.6:
                            score += 2
                        if self.player_score >= self.opponent_score:
                            score += 1
                    
                    # Speed-up (2)
                    elif ability_id == '2':
                        # Higher priority when:
                        # - Ball is far from paddle
                        # - Ball is moving very fast
                        # - Need to catch up to ball quickly
                        paddle_ball_dist = abs(self.ball.centery - self.opponent.centery)
                        if paddle_ball_dist > PADDLE_HEIGHT * 1.5:
                            score += 3
                        if abs(self.ball_speed_x) > self.initial_ball_speed * 1.8:
                            score += 2
                        if self.ball_speed_x > 0:
                            score += 1
                    
                    # Reverse (3)
                    elif ability_id == '3':
                        # Higher priority when:
                        # - Ball is moving towards player with high speed
                        # - Ball is in opponent's half
                        # - Player is in good position to receive reversed ball
                        if self.ball_speed_x < 0 and self.ball.centerx < WINDOW_WIDTH * 0.4:
                            score += 3
                        if abs(self.ball_speed_x) > self.initial_ball_speed * 1.5:
                            score += 2
                        if abs(self.ball.centery - self.opponent.centery) < PADDLE_HEIGHT * 0.5:
                            score += 2
                    
                    # Slow-down (4)
                    elif ability_id == '4':
                        # Higher priority when:
                        # - Player is on a scoring streak
                        # - Ball is moving very fast
                        # - Close match and ball is in player's half
                        if self.player_score > self.opponent_score:
                            score += 3
                        if abs(self.ball_speed_x) > self.initial_ball_speed * 2:
                            score += 2
                        if abs(self.player_score - self.opponent_score) <= 2 and self.ball.centerx < WINDOW_WIDTH * 0.5:
                            score += 2
                    
                    # Chaos (5)
                    elif ability_id == '5':
                        # Higher priority when:
                        # - Losing the game
                        # - Ball is in player's half
                        # - Player has full-size paddle (to maximize effect)
                        if self.player_score > self.opponent_score + 1:
                            score += 3
                        if self.ball.centerx < WINDOW_WIDTH * 0.3:
                            score += 2
                        if self.player.height >= PADDLE_HEIGHT * 0.9:
                            score += 2
                    
                    # Powershot (6)
                    elif ability_id == '6':
                        # Higher priority when:
                        # - Ball is moving towards opponent and close
                        # - Opponent's paddle is small
                        # - Ball speed is moderate (to ensure hit)
                        if self.ball_speed_x > 0 and WINDOW_WIDTH * 0.6 < self.ball.centerx < WINDOW_WIDTH * 0.8:
                            score += 3
                        if self.player.height <= PADDLE_HEIGHT * 0.8:
                            score += 2
                        if self.initial_ball_speed * 0.8 <= abs(self.ball_speed_x) <= self.initial_ball_speed * 1.5:
                            score += 2
                    
                    # Stealth (7)
                    elif ability_id == '7':
                        # Higher priority when:
                        # - Ball is in middle of field
                        # - Ball speed is moderate to fast
                        # - Close match
                        if WINDOW_WIDTH * 0.4 < self.ball.centerx < WINDOW_WIDTH * 0.6:
                            score += 3
                        if abs(self.ball_speed_x) > self.initial_ball_speed * 1.3:
                            score += 2
                        if abs(self.player_score - self.opponent_score) <= 2:
                            score += 2
                    
                    # Pinpoint (8)
                    elif ability_id == '8':
                        # Higher priority when:
                        # - Ball is far from paddle vertically
                        # - Ball is approaching
                        # - Ball is moving fast
                        if abs(self.ball.centery - self.opponent.centery) > PADDLE_HEIGHT * 1.5:
                            score += 3
                        if self.ball_speed_x > 0:
                            score += 2
                        if abs(self.ball_speed_x) > self.initial_ball_speed * 1.5:
                            score += 2
                    
                    # Ultra difficulty gets bonus points for certain situations
                    if self.bot_difficulty == 'ULTRA':
                        # Bonus for defensive abilities when losing
                        if self.player_score > self.opponent_score and ability_id in ['1', '4', '8']:
                            score += 1
                        # Bonus for offensive abilities when winning
                        if self.opponent_score > self.player_score and ability_id in ['3', '5', '6', '7']:
                            score += 1
                        # Bonus for speed/positioning when ball is moving fast
                        if abs(self.ball_speed_x) > self.initial_ball_speed * 2 and ability_id in ['2', '8']:
                            score += 1
                    
                    # Update best ability if current score is higher
                    if score > best_score:
                        best_score = score
                        best_ability = (ability_id, activate_func)
                
                # Use the ability if it has a good enough score
                min_score_threshold = 3 if self.bot_difficulty == 'HARD' else 2
                if best_ability and best_score >= min_score_threshold:
                    _, activate_func = best_ability
                    activate_func(False)  # False indicates it's the opponent/bot using the ability
            
            elif available_abilities:  # For EASY and MEDIUM difficulties
                # Use existing simple logic
                ability_id, activate_func = random.choice(available_abilities)
                
                # Basic conditions for ability usage
                use_ability = False
                
                if ability_id == '1':  # Size-up
                    use_ability = (self.opponent.height <= PADDLE_HEIGHT * 0.8 or 
                                 (self.ball_speed_x > 0 and self.ball.centerx > WINDOW_WIDTH * 0.6))
                elif ability_id == '2':  # Speed-up
                    use_ability = (abs(self.ball.centery - self.opponent.centery) > PADDLE_HEIGHT or
                                 abs(self.ball_speed_x) > self.initial_ball_speed * 1.5)
                elif ability_id == '3':  # Reverse
                    use_ability = (self.ball_speed_x < 0 and self.ball.centerx < WINDOW_WIDTH * 0.5)
                elif ability_id == '4':  # Slow-down
                    use_ability = (self.player_score >= self.opponent_score or
                                 abs(self.ball_speed_x) > self.initial_ball_speed * 2)
                elif ability_id == '5':  # Chaos
                    use_ability = (self.player_score > self.opponent_score or
                                 self.ball.centerx < WINDOW_WIDTH * 0.3)
                elif ability_id == '6':  # Powershot
                    use_ability = (self.ball_speed_x > 0 and 
                                 abs(self.ball.centerx - self.opponent.centerx) < WINDOW_WIDTH * 0.3)
                elif ability_id == '7':  # Stealth
                    use_ability = (WINDOW_WIDTH * 0.4 < self.ball.centerx < WINDOW_WIDTH * 0.6)
                elif ability_id == '8':  # Pinpoint
                    use_ability = abs(self.ball.centery - self.opponent.centery) > PADDLE_HEIGHT * 1.5
                
                # Strategic bonus based on difficulty
                strategic_bonus = {
                    'EASY': 0.2,
                    'MEDIUM': 0.4,
                    'HARD': 0.6,
                    'ULTRA': 0.8
                }
                
                if use_ability or random.random() < strategic_bonus[self.bot_difficulty]:
                    activate_func(False)

    def opponent_ai(self):
        if not self.two_player_mode:
            current_time = time.time()
            difficulty_settings = BOT_DIFFICULTY[self.bot_difficulty]
            
            # Check and use abilities
            self.check_ai_ability_usage()
            
            # Update AI target with reaction delay
            if (self.target_y is None or 
                current_time - self.last_ai_update >= difficulty_settings['reaction_delay']):
                
                # Predict ball position with some error
                prediction_error = random.randint(-difficulty_settings['prediction_error'], 
                                               difficulty_settings['prediction_error'])
                self.target_y = self.ball.y + prediction_error
                self.last_ai_update = current_time
            
            # Move towards the target
            if self.target_y is not None:
                ai_speed = difficulty_settings['speed']
                
                # Adjust speed based on active effects
                if self.opponent_speed_powerup_active:
                    ai_speed *= SPEED_MULTIPLIER
                if self.opponent_slow_active:
                    ai_speed *= SLOW_MULTIPLIER
                if self.opponent_chaos_active:
                    ai_speed *= CHAOS_SPEED_MULTIPLIER
                
                # Move towards target
                if self.opponent.centery < self.target_y:
                    self.opponent.y += ai_speed
                elif self.opponent.centery > self.target_y:
                    self.opponent.y -= ai_speed
                
                # Keep paddle within screen bounds
                if self.opponent.top < 0:
                    self.opponent.top = 0
                if self.opponent.bottom > WINDOW_HEIGHT:
                    self.opponent.bottom = WINDOW_HEIGHT

    def draw_fire_effect(self):
        # Calculate fire intensity based on ball speed
        current_speed = abs(self.ball_speed_x)  # Use absolute speed
        speed_ratio = min((current_speed - FIRE_MIN_SPEED) / (FIRE_MAX_SPEED - FIRE_MIN_SPEED), 1.0)
        
        if speed_ratio <= 0:
            return  # No fire effect at minimum speed
        
        # Calculate number of particles based on speed
        num_particles = int(FIRE_MIN_PARTICLES + 
                          (FIRE_MAX_PARTICLES - FIRE_MIN_PARTICLES) * speed_ratio)
        
        # Calculate base particle size (slightly larger than ball)
        base_size = BALL_SIZE * (1.0 + 0.5 * speed_ratio)
        
        # Draw fire particles behind the ball
        ball_center = self.ball.center
        movement_direction = math.atan2(self.ball_speed_y, self.ball_speed_x)
        
        for i in range(num_particles):
            # Calculate particle position (opposite to ball movement)
            offset_distance = (i + 1) * (base_size * 0.3 * speed_ratio)
            particle_x = ball_center[0] - math.cos(movement_direction) * offset_distance
            particle_y = ball_center[1] - math.sin(movement_direction) * offset_distance
            
            # Calculate particle size (decreasing as they trail)
            particle_size = base_size * (1.0 - (i / num_particles) * 0.5)
            
            # Draw particle with color based on position in trail
            color_idx = min(i, len(FIRE_COLORS) - 1)
            color = FIRE_COLORS[color_idx]
            
            # Create particle rect
            particle_rect = pygame.Rect(0, 0, particle_size, particle_size)
            particle_rect.center = (particle_x, particle_y)
            
            # Draw the particle
            pygame.draw.ellipse(screen, color, particle_rect)
            
            # Add glow effect by drawing additional transparent circles
            glow_size = particle_size * 1.2
            glow_rect = pygame.Rect(0, 0, glow_size, glow_size)
            glow_rect.center = (particle_x, particle_y)
            
            # Create a surface for the glow with alpha channel
            glow_surface = pygame.Surface((int(glow_size), int(glow_size)), pygame.SRCALPHA)
            alpha = int(128 * (1.0 - i / num_particles) * speed_ratio)
            glow_color = (*color, alpha)
            pygame.draw.ellipse(glow_surface, glow_color, glow_surface.get_rect())
            screen.blit(glow_surface, glow_rect)

    def draw(self):
        screen.fill(BLACK)
        
        # Draw fire effect before the ball
        self.draw_fire_effect()
        
        # Update and draw explosions
        self.update_explosions()
        self.draw_explosions(screen)
        
        # Draw game elements
        pygame.draw.rect(screen, self.player_color, self.player)
        pygame.draw.rect(screen, self.opponent_color, self.opponent)
        pygame.draw.ellipse(screen, self.ball_color, self.ball)
        pygame.draw.aaline(screen, WHITE, (WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2, WINDOW_HEIGHT))

        # Draw score at the top of the screen
        player_text = large_font.render(str(self.player_score), False, WHITE)
        opponent_text = large_font.render(str(self.opponent_score), False, WHITE)
        screen.blit(player_text, (WINDOW_WIDTH//4 - player_text.get_width()//2, 20))
        screen.blit(opponent_text, (3*WINDOW_WIDTH//4 - opponent_text.get_width()//2, 20))

        # Draw powerup meters at the bottom
        self.draw_powerup_meters()

        pygame.display.flip()

    def check_winner(self):
        if self.winning_score != float('inf'):
            if self.player_score >= self.winning_score:
                return "Player 1 Wins!"
            elif self.opponent_score >= self.winning_score:
                return "Player 2 Wins!" if self.two_player_mode else "Computer Wins!"
        return None

def main():
    # Initialize Pygame and create window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    while True:
        # Initialize all menu variables
        two_player_mode = None
        ball_speed = None
        paddle_shrink_enabled = None
        bot_difficulty = None
        winning_score = None
        current_menu = "main"  # Start at main menu

        while True:
            # Display current menu
            if current_menu == "main":
                draw_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            two_player_mode = False
                            current_menu = "speed"
                        elif event.key == pygame.K_2:
                            two_player_mode = True
                            current_menu = "speed"

            elif current_menu == "speed":
                draw_speed_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            ball_speed = INITIAL_BALL_SPEED * 0.4
                            current_menu = "paddle_shrink"
                        elif event.key == pygame.K_2:
                            ball_speed = INITIAL_BALL_SPEED * 0.75
                            current_menu = "paddle_shrink"
                        elif event.key == pygame.K_3:
                            ball_speed = INITIAL_BALL_SPEED
                            current_menu = "paddle_shrink"
                        elif event.key == pygame.K_4:
                            ball_speed = INITIAL_BALL_SPEED * 1.25
                            current_menu = "paddle_shrink"
                        elif event.key == pygame.K_5:
                            ball_speed = INITIAL_BALL_SPEED * 1.75
                            current_menu = "paddle_shrink"
                        elif event.key == pygame.K_MINUS:
                            # Reset state when going back to main menu
                            current_menu = "main"
                            two_player_mode = None
                            ball_speed = None

            elif current_menu == "paddle_shrink":
                draw_paddle_shrink_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            paddle_shrink_enabled = True
                            current_menu = "difficulty" if not two_player_mode else "score"
                        elif event.key == pygame.K_2:
                            paddle_shrink_enabled = False
                            current_menu = "difficulty" if not two_player_mode else "score"
                        elif event.key == pygame.K_MINUS:
                            # Reset state when going back to speed menu
                            current_menu = "speed"
                            paddle_shrink_enabled = None

            elif current_menu == "difficulty":
                draw_difficulty_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            bot_difficulty = 'EASY'
                            current_menu = "score"
                        elif event.key == pygame.K_2:
                            bot_difficulty = 'MEDIUM'
                            current_menu = "score"
                        elif event.key == pygame.K_3:
                            bot_difficulty = 'HARD'
                            current_menu = "score"
                        elif event.key == pygame.K_4:
                            bot_difficulty = 'ULTRA'
                            current_menu = "score"
                        elif event.key == pygame.K_MINUS:
                            # Reset state when going back to paddle shrink menu
                            current_menu = "paddle_shrink"
                            bot_difficulty = None

            elif current_menu == "score":
                draw_score_selection()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                       pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]:
                            key = str(event.key - pygame.K_0)  # Convert to string 1-8
                            winning_score = SCORE_OPTIONS[key]
                            # All settings are complete, create game
                            if two_player_mode:
                                bot_difficulty = 'MEDIUM'
                            game = PongGame(two_player_mode, ball_speed, winning_score,
                                          bot_difficulty, paddle_shrink_enabled)
                            countdown_timer()
                            # Exit menu loop and start game
                            break
                        elif event.key == pygame.K_MINUS:
                            # Reset state when going back
                            if not two_player_mode:
                                current_menu = "difficulty"
                                winning_score = None
                            else:
                                current_menu = "paddle_shrink"
                                winning_score = None
                if winning_score is not None:
                    break  # Exit to game loop

            clock.tick(60)

        if winning_score is None:
            continue  # Start over from main menu if we didn't get all settings

        # Game loop
        running = True
        while running:
            try:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

                # Get pressed keys
                keys = pygame.key.get_pressed()

                # Move paddles
                if keys[pygame.K_w]:
                    game.move_paddle(game.player, up=True)
                if keys[pygame.K_s]:
                    game.move_paddle(game.player, up=False)
                
                if game.two_player_mode:
                    if keys[pygame.K_UP]:
                        game.move_paddle(game.opponent, up=True)
                    if keys[pygame.K_DOWN]:
                        game.move_paddle(game.opponent, up=False)
                else:
                    game.opponent_ai()

                # Check for ability activations
                for ability, key in game.player_keybinds.items():
                    if keys[key]:
                        if ability == '1':
                            game.activate_powerup(True)
                        elif ability == '2':
                            game.activate_speed_powerup(True)
                        elif ability == '3':
                            game.activate_reverse_powerup(True)
                        elif ability == '4':
                            game.activate_slow_powerup(True)
                        elif ability == '5':
                            game.activate_chaos_powerup(True)
                        elif ability == '6':
                            game.activate_powershot(True)
                        elif ability == '7':
                            game.activate_stealth(True)
                        elif ability == '8':
                            game.activate_pinpoint(True)

                if game.two_player_mode:
                    for ability, key in game.opponent_keybinds.items():
                        if keys[key]:
                            if ability == '1':
                                game.activate_powerup(False)
                            elif ability == '2':
                                game.activate_speed_powerup(False)
                            elif ability == '3':
                                game.activate_reverse_powerup(False)
                            elif ability == '4':
                                game.activate_slow_powerup(False)
                            elif ability == '5':
                                game.activate_chaos_powerup(False)
                            elif ability == '6':
                                game.activate_powershot(False)
                            elif ability == '7':
                                game.activate_stealth(False)
                            elif ability == '8':
                                game.activate_pinpoint(False)

                # Update game state
                game.ball_movement()
                game.update_powerups()
                game.update_explosions()  # Update explosion effects

                # Draw everything
                screen.fill(BLACK)
                pygame.draw.rect(screen, game.player_color, game.player)
                pygame.draw.rect(screen, game.opponent_color, game.opponent)
                pygame.draw.ellipse(screen, game.ball_color, game.ball)
                pygame.draw.aaline(screen, WHITE, (WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2, WINDOW_HEIGHT))
                
                # Draw scores
                player_score = large_font.render(str(game.player_score), True, WHITE)
                opponent_score = large_font.render(str(game.opponent_score), True, WHITE)
                screen.blit(player_score, (WINDOW_WIDTH//4, 20))
                screen.blit(opponent_score, (3*WINDOW_WIDTH//4, 20))
                
                # Draw ability rings
                game.draw_powerup_meters()
                
                # Draw explosions
                game.draw_explosions(screen)
                
                # Update display
                pygame.display.flip()
                clock.tick(60)

                # Check for winner
                winner = game.check_winner()
                if winner:
                    draw_winner(winner)
                    waiting_for_input = True
                    while waiting_for_input:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    waiting_for_input = False
                                    running = False
                                elif event.key == pygame.K_ESCAPE:
                                    pygame.quit()
                                    sys.exit()
                        pygame.time.Clock().tick(60)  # Control frame rate in the waiting loop

            except Exception as e:
                print(f"Error in game loop: {e}")
                continue  # Continue the game loop even if there's an error

if __name__ == "__main__":
    main()
