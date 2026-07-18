#!/usr/bin/env python3
"""
Dino Jump Game - Pygame Version
A complete dinosaur jumping game with audio, settings, and theme changes.
"""

import pygame
import random
import json
import os
import sys
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')
SCORES_FILE = os.path.join(DATA_DIR, 'scores.json')
LOG_FILE = os.path.join(LOGS_DIR, 'game.log')

# Create directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Logging setup
def log_message(message):
    """Log message to file and console"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + '\n')

# Settings
DEFAULT_SETTINGS = {
    'volume': 0.7,
    'difficulty': 'normal',
    'fullscreen': False,
    'show_fps': False
}

def load_settings():
    """Load settings from JSON file"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        log_message(f"Error loading settings: {e}")
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        log_message("Settings saved successfully")
        return True
    except Exception as e:
        log_message(f"Error saving settings: {e}")
        return False

# Score management
def load_scores():
    """Load scores from JSON file"""
    try:
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        log_message(f"Error loading scores: {e}")
    return []

def save_score(player_name, score):
    """Save score to JSON file"""
    try:
        scores = load_scores()
        scores.append({
            'player_name': player_name,
            'score': score,
            'date': datetime.now().isoformat()
        })
        scores.sort(key=lambda x: x['score'], reverse=True)
        scores = scores[:10]  # Keep top 10
        
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
        log_message(f"Score saved: {player_name} - {score}")
        return True
    except Exception as e:
        log_message(f"Error saving score: {e}")
        return False

# Themes
THEMES = {
    'day': {
        'sky': (135, 206, 235),
        'ground': (139, 69, 19),
        'ground_detail': (101, 67, 33),
        'cloud': (255, 255, 255),
        'text': (0, 0, 0)
    },
    'night': {
        'sky': (25, 25, 112),
        'ground': (85, 85, 85),
        'ground_detail': (64, 64, 64),
        'cloud': (200, 200, 200),
        'text': (255, 255, 255)
    },
    'sunset': {
        'sky': (255, 127, 80),
        'ground': (160, 82, 45),
        'ground_detail': (139, 69, 19),
        'cloud': (255, 200, 150),
        'text': (0, 0, 0)
    }
}

# Game Class
class DinoGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.settings = load_settings()
        
        # Audio system (using simple beep sounds)
        self.sounds = {}
        self.init_audio()
        
        # Screen setup
        if self.settings['fullscreen']:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = pygame.display.get_surface().get_size()
        else:
            self.width, self.height = 800, 600
            self.screen = pygame.display.set_mode((self.width, self.height))
        
        pygame.display.set_caption("Dino Jump")
        
        # Game state
        self.state = 'menu'  # menu, playing, paused, gameover, settings, highscores
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game variables
        self.score = 0
        self.base_speed = 2.0  # Very slow start
        self.current_speed = self.base_speed
        self.theme = 'day'
        self.theme_change_score = 500
        self.speed_increase_score = 150
        
        # Dinosaur
        self.dino = {
            'x': 100,
            'y': self.height - 150,
            'width': 50,
            'height': 60,
            'velocity_y': 0,
            'jumping': False,
            'gravity': 0.5,
            'jump_force': -12
        }
        self.ground_y = self.height - 100
        
        # Obstacles
        self.obstacles = []
        self.obstacle_timer = 0
        self.obstacle_interval = 120
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Input
        self.player_name = ""
        
        log_message("Game initialized")
    
    def init_audio(self):
        """Initialize audio system with generated sounds"""
        try:
            # Generate simple beep sounds using pygame's Sound
            # Jump sound (high pitch)
            self.jump_sound = self.generate_beep(440, 0.1)
            # Score sound (medium pitch)
            self.score_sound = self.generate_beep(523, 0.05)
            # Game over sound (low pitch)
            self.gameover_sound = self.generate_beep(220, 0.3)
            log_message("Audio system initialized")
        except Exception as e:
            log_message(f"Audio initialization failed: {e}")
            self.jump_sound = None
            self.score_sound = None
            self.gameover_sound = None
    
    def generate_beep(self, frequency, duration):
        """Generate a simple beep sound"""
        try:
            import array
            sample_rate = 44100
            n_samples = int(sample_rate * duration)
            buffer = array.array('h')
            
            for i in range(n_samples):
                value = int(32767 * 0.5 * (1 + 0.5 * self.settings['volume']) * 
                           (i % (sample_rate // frequency)) / (sample_rate // frequency))
                buffer.append(value)
            
            return pygame.mixer.Sound(buffer)
        except:
            return None
    
    def play_sound(self, sound):
        """Play a sound if available"""
        if sound and self.settings['volume'] > 0:
            sound.set_volume(self.settings['volume'])
            sound.play()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == 'playing':
                        self.state = 'paused'
                    elif self.state == 'paused' or self.state == 'settings' or self.state == 'highscores':
                        self.state = 'menu'
                    elif self.state == 'menu':
                        self.running = False
                
                if self.state == 'menu':
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_s:
                        self.state = 'settings'
                    elif event.key == pygame.K_h:
                        self.state = 'highscores'
                
                elif self.state == 'playing':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.jump()
                    elif event.key == pygame.K_p:
                        self.state = 'paused'
                
                elif self.state == 'paused':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_c:
                        self.state = 'playing'
                
                elif self.state == 'gameover':
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_RETURN:
                        if self.player_name:
                            save_score(self.player_name, self.score)
                            self.state = 'menu'
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if len(self.player_name) < 20 and event.unicode.isprintable():
                            self.player_name += event.unicode
                
                elif self.state == 'settings':
                    if event.key == pygame.K_v:
                        self.settings['volume'] = (self.settings['volume'] + 0.1) % 1.1
                        if self.settings['volume'] > 1.0:
                            self.settings['volume'] = 0.0
                        save_settings(self.settings)
                    elif event.key == pygame.K_d:
                        difficulties = ['easy', 'normal', 'hard']
                        idx = difficulties.index(self.settings['difficulty'])
                        self.settings['difficulty'] = difficulties[(idx + 1) % 3]
                        save_settings(self.settings)
                    elif event.key == pygame.K_f:
                        self.settings['fullscreen'] = not self.settings['fullscreen']
                        save_settings(self.settings)
                        pygame.display.quit()
                        pygame.init()
                        if self.settings['fullscreen']:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            self.width, self.height = pygame.display.get_surface().get_size()
                        else:
                            self.width, self.height = 800, 600
                            self.screen = pygame.display.set_mode((self.width, self.height))
                        self.ground_y = self.height - 100
                        self.dino['y'] = self.ground_y - self.dino['height']
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
                
                elif self.state == 'highscores':
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 'menu':
                    self.start_game()
    
    def jump(self):
        if not self.dino['jumping']:
            self.dino['velocity_y'] = self.dino['jump_force']
            self.dino['jumping'] = True
            self.play_sound(self.jump_sound)
            log_message("Dino jumped")
    
    def start_game(self):
        self.state = 'playing'
        self.score = 0
        self.current_speed = self.base_speed
        self.theme = 'day'
        self.obstacles = []
        self.obstacle_timer = 0
        self.dino['y'] = self.ground_y - self.dino['height']
        self.dino['velocity_y'] = 0
        self.dino['jumping'] = False
        log_message("Game started")
    
    def restart_game(self):
        self.start_game()
    
    def update(self):
        if self.state != 'playing':
            return
        
        # Update dino
        self.dino['velocity_y'] += self.dino['gravity']
        self.dino['y'] += self.dino['velocity_y']
        
        if self.dino['y'] >= self.ground_y - self.dino['height']:
            self.dino['y'] = self.ground_y - self.dino['height']
            self.dino['velocity_y'] = 0
            self.dino['jumping'] = False
        
        # Generate obstacles
        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_interval:
            self.generate_obstacle()
            self.obstacle_timer = 0
            self.obstacle_interval = random.randint(80, 150)
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle['x'] -= self.current_speed
            if obstacle['x'] + obstacle['width'] < 0:
                self.obstacles.remove(obstacle)
                self.score += 10
                self.play_sound(self.score_sound)
        
        # Check collision
        if self.check_collision():
            self.state = 'gameover'
            self.player_name = ""
            self.play_sound(self.gameover_sound)
            log_message(f"Game over! Score: {self.score}")
        
        # Update speed and theme
        self.update_difficulty()
    
    def generate_obstacle(self):
        types = ['cactus', 'cactus', 'bird', 'rock']
        if self.theme != 'day':
            types.append('bird')
            types.append('rock')
        
        obstacle_type = random.choice(types)
        
        if obstacle_type == 'cactus':
            obstacle = {
                'x': self.width,
                'y': self.ground_y - 50,
                'width': 30,
                'height': 50,
                'type': 'cactus'
            }
        elif obstacle_type == 'bird':
            obstacle = {
                'x': self.width,
                'y': self.ground_y - 120,
                'width': 40,
                'height': 30,
                'type': 'bird'
            }
        elif obstacle_type == 'rock':
            obstacle = {
                'x': self.width,
                'y': self.ground_y - 40,
                'width': 35,
                'height': 40,
                'type': 'rock'
            }
        
        self.obstacles.append(obstacle)
    
    def check_collision(self):
        dino_rect = pygame.Rect(
            self.dino['x'],
            self.dino['y'],
            self.dino['width'],
            self.dino['height']
        )
        
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(
                obstacle['x'],
                obstacle['y'],
                obstacle['width'],
                obstacle['height']
            )
            if dino_rect.colliderect(obstacle_rect):
                return True
        return False
    
    def update_difficulty(self):
        # Increase speed by 1% every 150 points
        speed_increases = self.score // self.speed_increase_score
        self.current_speed = self.base_speed * (1.01 ** speed_increases)
        
        # Change theme every 500 points
        theme_changes = self.score // self.theme_change_score
        themes = ['day', 'night', 'sunset']
        self.theme = themes[theme_changes % len(themes)]
    
    def draw(self):
        theme = THEMES[self.theme]
        
        # Draw sky
        self.screen.fill(theme['sky'])
        
        # Draw clouds
        for i in range(3):
            cloud_x = (i * 300 + (self.score * 0.5)) % (self.width + 200) - 100
            pygame.draw.circle(self.screen, theme['cloud'], (cloud_x, 100), 30)
            pygame.draw.circle(self.screen, theme['cloud'], (cloud_x + 40, 100), 40)
            pygame.draw.circle(self.screen, theme['cloud'], (cloud_x + 80, 100), 30)
        
        # Draw ground
        pygame.draw.rect(self.screen, theme['ground'], (0, self.ground_y, self.width, self.height - self.ground_y))
        for i in range(0, self.width, 50):
            pygame.draw.rect(self.screen, theme['ground_detail'], (i, self.ground_y, 30, 5))
        
        # Draw obstacles
        for obstacle in self.obstacles:
            if obstacle['type'] == 'cactus':
                pygame.draw.rect(self.screen, (46, 125, 50), (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))
                pygame.draw.rect(self.screen, (46, 125, 50), (obstacle['x'] - 10, obstacle['y'] + 10, 10, 20))
                pygame.draw.rect(self.screen, (46, 125, 50), (obstacle['x'] + obstacle['width'], obstacle['y'] + 5, 10, 15))
            elif obstacle['type'] == 'bird':
                pygame.draw.rect(self.screen, (230, 81, 0), (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))
                pygame.draw.rect(self.screen, (230, 81, 0), (obstacle['x'] + 5, obstacle['y'] - 10, 20, 10))
                pygame.draw.rect(self.screen, (230, 81, 0), (obstacle['x'] + 5, obstacle['y'] + obstacle['height'], 20, 10))
            elif obstacle['type'] == 'rock':
                pygame.draw.rect(self.screen, (105, 105, 105), (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))
                pygame.draw.rect(self.screen, (128, 128, 128), (obstacle['x'] + 5, obstacle['y'] + 5, 10, 10))
        
        # Draw dino
        pygame.draw.rect(self.screen, (51, 51, 51), (self.dino['x'], self.dino['y'], self.dino['width'], self.dino['height']))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.dino['x'] + 35, self.dino['y'] + 10, 8, 8))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.dino['x'] + 38, self.dino['y'] + 12, 4, 4))
        
        # Draw UI based on state
        self.draw_ui(theme)
        
        pygame.display.flip()
    
    def draw_ui(self, theme):
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, theme['text'])
        self.screen.blit(score_text, (20, 20))
        
        if self.settings['show_fps']:
            fps_text = self.font_small.render(f"FPS: {int(self.clock.get_fps())}", True, theme['text'])
            self.screen.blit(fps_text, (self.width - 100, 20))
        
        if self.state == 'menu':
            title = self.font_large.render("DINO JUMP", True, theme['text'])
            start = self.font_medium.render("Press SPACE to Start", True, theme['text'])
            settings = self.font_small.render("S - Settings | H - High Scores", True, theme['text'])
            
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 150))
            self.screen.blit(start, (self.width//2 - start.get_width()//2, 250))
            self.screen.blit(settings, (self.width//2 - settings.get_width()//2, 320))
        
        elif self.state == 'paused':
            pause = self.font_large.render("PAUSED", True, theme['text'])
            resume = self.font_medium.render("Press C to Continue", True, theme['text'])
            restart = self.font_small.render("Press R to Restart", True, theme['text'])
            
            self.screen.blit(pause, (self.width//2 - pause.get_width()//2, 200))
            self.screen.blit(resume, (self.width//2 - resume.get_width()//2, 280))
            self.screen.blit(restart, (self.width//2 - restart.get_width()//2, 340))
        
        elif self.state == 'gameover':
            gameover = self.font_large.render("GAME OVER", True, theme['text'])
            score = self.font_medium.render(f"Score: {self.score}", True, theme['text'])
            name = self.font_small.render("Enter your name:", True, theme['text'])
            name_text = self.font_medium.render(self.player_name, True, theme['text'])
            submit = self.font_small.render("Press ENTER to Save", True, theme['text'])
            
            self.screen.blit(gameover, (self.width//2 - gameover.get_width()//2, 150))
            self.screen.blit(score, (self.width//2 - score.get_width()//2, 230))
            self.screen.blit(name, (self.width//2 - name.get_width()//2, 300))
            self.screen.blit(name_text, (self.width//2 - name_text.get_width()//2, 340))
            self.screen.blit(submit, (self.width//2 - submit.get_width()//2, 400))
        
        elif self.state == 'settings':
            title = self.font_large.render("SETTINGS", True, theme['text'])
            volume = self.font_medium.render(f"Volume: {int(self.settings['volume'] * 100)}% (V)", True, theme['text'])
            difficulty = self.font_medium.render(f"Difficulty: {self.settings['difficulty'].upper()} (D)", True, theme['text'])
            fullscreen = self.font_medium.render(f"Fullscreen: {self.settings['fullscreen']} (F)", True, theme['text'])
            back = self.font_small.render("Press ESC to go back", True, theme['text'])
            
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 100))
            self.screen.blit(volume, (self.width//2 - volume.get_width()//2, 200))
            self.screen.blit(difficulty, (self.width//2 - difficulty.get_width()//2, 260))
            self.screen.blit(fullscreen, (self.width//2 - fullscreen.get_width()//2, 320))
            self.screen.blit(back, (self.width//2 - back.get_width()//2, 400))
        
        elif self.state == 'highscores':
            title = self.font_large.render("HIGH SCORES", True, theme['text'])
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 80))
            
            scores = load_scores()
            for i, score_data in enumerate(scores[:10]):
                score_text = self.font_small.render(f"{i+1}. {score_data['player_name']} - {score_data['score']}", True, theme['text'])
                self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 160 + i * 35))
            
            back = self.font_small.render("Press ESC to go back", True, theme['text'])
            self.screen.blit(back, (self.width//2 - back.get_width()//2, 520))
    
    def run(self):
        log_message("Game loop started")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        log_message("Game closed")
        sys.exit()

if __name__ == '__main__':
    game = DinoGame()
    game.run()
