import pygame
import random
import os
import cv2
import mediapipe as mp
import time

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images
fruit_images = {
    'apple': pygame.transform.scale(pygame.image.load('apple.png').convert_alpha(), (70, 70)),
    'banana': pygame.transform.scale(pygame.image.load('banana.png').convert_alpha(), (70, 70)),
    'orange': pygame.transform.scale(pygame.image.load('orange.png').convert_alpha(), (70, 70)),
    'watermelon': pygame.transform.scale(pygame.image.load('watermelon.png').convert_alpha(), (70, 70)),
    'strawberry': pygame.transform.scale(pygame.image.load('strawberry.png').convert_alpha(), (70, 70)),
}

bomb_image = pygame.transform.scale(pygame.image.load('bomb.png').convert_alpha(), (60, 60))
explosion_image = pygame.transform.scale(pygame.image.load('explosion.png').convert_alpha(), (100, 100))

# Load sounds
cut_sound = pygame.mixer.Sound('cut1.mp3')
explosion_sound = pygame.mixer.Sound('explosion.mp3')
bg_music = 'background.mp3'

# Background music
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)  # Loop forever

# Hand tracking setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Camera setup
cap = cv2.VideoCapture(0)

# Score
score = 0
combo_score = 0
font = pygame.font.Font(None, 50)

# State control
game_over = False
difficulty_level = "easy"  # Starting level
timer = 120  # 2 minutes timer

# Thresholds for level increase
level_thresholds = [100, 200, 300, 400]
current_level = 1
level_up_message = ""

# Fruit Class
class Fruit:
    def __init__(self, name):
        self.image = fruit_images[name]
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT + random.randint(20, 100)
        self.speed = random.uniform(4, 7)
        self.name = name
        self.is_cut = False
        self.split = False

    def move(self):
        if not self.is_cut:
            self.y -= self.speed
            if self.y < -100:
                self.reset()

    def draw(self):
        if not self.is_cut:
            screen.blit(self.image, (self.x, self.y))

    def reset(self):
        self.y = HEIGHT + random.randint(20, 100)
        self.x = random.randint(50, WIDTH - 50)
        self.is_cut = False
        self.speed = random.uniform(4, 7)

# Bomb Class
class Bomb:
    def __init__(self):
        self.image = bomb_image
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT + random.randint(20, 100)
        self.speed = random.uniform(5, 8)
        self.is_cut = False

    def move(self):
        if not self.is_cut:
            self.y -= self.speed
            if self.y < -100:
                self.reset()

    def draw(self):
        if not self.is_cut:
            screen.blit(self.image, (self.x, self.y))

    def reset(self):
        self.y = HEIGHT + random.randint(20, 100)
        self.x = random.randint(50, WIDTH - 50)
        self.is_cut = False
        self.speed = random.uniform(5, 8)

# Create objects
fruits = [Fruit(name) for name in fruit_images.keys()]
bombs = [Bomb() for _ in range(2)]

# Function to detect collision
def detect_collision(obj, x, y):
    obj_rect = pygame.Rect(obj.x, obj.y, 70, 70)
    return obj_rect.collidepoint(x, y)

# Explosion effect
def show_explosion(x, y):
    screen.blit(explosion_image, (x - 75, y - 75))  # Half of 150 is 75
    pygame.display.flip()
    time.sleep(0.8)

# Reset game
def reset_game():
    global score, game_over, combo_score, timer, current_level
    score = 0
    combo_score = 0
    timer = 120  # Reset timer to 2 minutes
    current_level = 1
    game_over = False
    for fruit in fruits:
        fruit.reset()
    for bomb in bombs:
        bomb.reset()

# Display Game Over
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

    pygame.display.flip()

# Timer display
def display_timer():
    global timer
    timer_text = font.render(f"Time: {timer:.2f}", True, WHITE)
    screen.blit(timer_text, (WIDTH - 150, 10))

# Level display
def display_level():
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    screen.blit(level_text, (10, 110))

# Display Start Screen
def display_start_screen():
    screen.fill(BLACK)
    welcome_text = font.render("Welcome to Fruit Ninja!", True, RED)
    start_text = font.render("Press Enter to Start", True, WHITE)
    screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# Main loop
running = True
clock = pygame.time.Clock()

# Start screen flag
start_screen = True

while running:
    if start_screen:
        display_start_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            start_screen = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        continue

    if game_over:
        game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture frame from camera
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame to avoid mirror effect
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    screen.fill(BLACK)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x = int(hand_landmarks.landmark[8].x * WIDTH)
            y = int(hand_landmarks.landmark[8].y * HEIGHT)

            pygame.draw.circle(screen, WHITE, (x, y), 10)

            # Check for collision with fruits
            for fruit in fruits:
                if detect_collision(fruit, x, y) and not fruit.is_cut:
                    fruit.is_cut = True
                    score += 10
                    combo_score += 1
                    cut_sound.play()
                    fruit.reset()

            # Check for collision with bombs
            for bomb in bombs:
                if detect_collision(bomb, x, y) and not bomb.is_cut:
                    bomb.is_cut = True
                    explosion_sound.play()
                    show_explosion(bomb.x, bomb.y)
                    game_over = True

    # Move and draw fruits
    for fruit in fruits:
        fruit.move()
        fruit.draw()

    # Move and draw bombs
    for bomb in bombs:
        bomb.move()
        bomb.draw()

    # Display score and combo
    score_text = font.render(f"Score: {score}", True, WHITE)
    combo_text = font.render(f"Combo: {combo_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(combo_text, (10, 60))

    # Display timer
    if timer > 0:
        timer -= 1 / 60  # Reduce the timer every frame
        display_timer()

    # Show level increase
    if score >= level_thresholds[current_level - 1]:
        current_level += 1
        level_up_message = font.render(f"Level {current_level} Unlocked!", True, RED)
        screen.blit(level_up_message, (WIDTH // 2 - level_up_message.get_width() // 2, HEIGHT // 2 - 100))
        pygame.display.flip()
        time.sleep(1)

    display_level()

    pygame.display.flip()
    clock.tick(60)

    # Show OpenCV window
    cv2.imshow("Camera Feed", frame)

    # Handle key events for OpenCV window (to close it)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()
