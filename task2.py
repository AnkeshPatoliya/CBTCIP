import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up the display
width, height = 1100, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock Paper Scissors")

# Load images
rock_img = pygame.image.load('rock.png')
paper_img = pygame.image.load('paper.png')
scissors_img = pygame.image.load('scissors.png')
play_again_img = pygame.image.load('play_again.png')  # Assume you have a play again button image

# Scale images
rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))
play_again_img = pygame.transform.scale(play_again_img, (150, 50))

# Positions
player_start_pos = (-150, height // 2 - 75)
computer_start_pos = (width, height // 2 - 75)
player_end_pos = (width // 2, height // 2)
computer_end_pos = (width // 2 - 25, height // 2 - 75)
result_pos = (width // 2, 50)
play_again_pos = (width // 2 - 75, 500)

# Define options
options = ["rock", "paper", "scissors"]
images = {"rock": rock_img, "paper": paper_img, "scissors": scissors_img}

# Font
font = pygame.font.Font(None, 74)

# Function to display text
def display_text(text, position):
    text_surface = font.render(text, True, (255, 255, 255))
    rect = text_surface.get_rect(center=position)
    window.blit(text_surface, rect)

# Function to animate interaction
def animate_interaction(player_choice, computer_choice):
    animation_done = False
    animation_frame = 0
    player_image = images[player_choice]
    computer_image = images[computer_choice]

    player_pos = list(player_start_pos)
    computer_pos = list(computer_start_pos)

    while not animation_done:
        window.fill((0, 0, 0))
        window.blit(player_image, player_pos)
        window.blit(computer_image, computer_pos)
        pygame.display.update()

        player_pos[0] += (player_end_pos[0] - player_pos[0]) / 10
        computer_pos[0] += (computer_end_pos[0] - computer_pos[0]) / 10

        animation_frame += 1
        if animation_frame > 20:
            animation_done = True

        pygame.time.delay(50)

# Function to handle game logic
def game_logic(player_choice):
    computer_choice = random.choice(options)
    result = ""
    if player_choice == computer_choice:
        result = "It's a tie!"
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
        result = "You win!"
    else:
        result = "You lose!"

    return player_choice, computer_choice, result

# Main game loop
running = True
player_choice = None
game_result = None
computer_choice = None

while running:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if player_choice is None:
                if 200 <= mouse_pos[0] <= 350 and 400 <= mouse_pos[1] <= 550:
                    player_choice, computer_choice, game_result = game_logic("rock")
                elif 400 <= mouse_pos[0] <= 550 and 400 <= mouse_pos[1] <= 550:
                    player_choice, computer_choice, game_result = game_logic("paper")
                elif 600 <= mouse_pos[0] <= 750 and 400 <= mouse_pos[1] <= 550:
                    player_choice, computer_choice, game_result = game_logic("scissors")
                if player_choice:
                    animate_interaction(player_choice, computer_choice)
            else:
                if play_again_pos[0] <= mouse_pos[0] <= play_again_pos[0] + 150 and play_again_pos[1] <= mouse_pos[1] <= play_again_pos[1] + 50:
                    player_choice = None
                    game_result = None
                    computer_choice = None

    if player_choice is None:
        # Display choices
        window.blit(rock_img, (200, 400))
        window.blit(paper_img, (400, 400))
        window.blit(scissors_img, (600, 400))
    else:
        # Display result and play again button
        display_text(f"Player: {player_choice}", (width // 4, 200))
        display_text(f"Computer: {computer_choice}", (3 * width // 4, 200))
        display_text(game_result, result_pos)
        window.blit(play_again_img, play_again_pos)

    pygame.display.update()