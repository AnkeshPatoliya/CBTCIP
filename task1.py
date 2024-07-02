import pygame as p
import random
import sys

p.init()

width, height = 1000, 600  
win = p.display.set_mode((width, height))
p.display.set_caption("Guess My Number")

font = p.font.Font(None, 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def get_number_length_from_user():
    input_box = p.Rect(100, 100, 140, 32)
    color_inactive = p.Color('lightskyblue3')
    color_active = p.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == p.KEYDOWN:
                if active:
                    if event.key == p.K_RETURN:
                        try:
                            return int(text)
                        except ValueError:
                            print("Please enter a valid number.")
                    elif event.key == p.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        win.fill(WHITE)
        p.draw.rect(win, color, input_box, 2)
        draw_text('Enter number length:', font, BLACK, win, 100, 70)
        draw_text(text, font, BLACK, win, input_box.x + 5, input_box.y + 5)
        p.display.flip()

number_len = get_number_length_from_user()
print(f"Number length chosen: {number_len}")

num = [str(i) for i in range(10)]
random.shuffle(num)
number_list = num[:number_len]
#print(number_list)

user_input = ""
guesses = []
hints = []

green_count = 0
yellow_count = 0
max_attempts=10
attempts = 0  

box_width = 50
box_height = 30
box_margin = 10
count_box_x = number_len * 60 + 40
green_box_y = 60
yellow_box_y = green_box_y + box_height + box_margin

play_again_button_width = 200
play_again_button_height = 50
play_again_button_x = width // 2 - play_again_button_width // 2
play_again_button_y = height - 100

numpad_x = width - 300
numpad_y = height - 450
numpad_button_size = 70
numpad_button_margin = 10

def draw_grid():
    for i in range(10):
        for j in range(number_len):
            p.draw.rect(win, GRAY, (j * 60 + 20, i * 40 + 60, 50, 30), 2)

def draw_hints():
    for i in range(len(hints)):
        hint = hints[i]
        for j in range(2):
            color = GREEN if j < hint[0] else YELLOW
            p.draw.rect(win, color, (number_len * 60 + 40 + j * 30, i * 40 + 60, 20, 20))

def draw_count_boxes():
    p.draw.rect(win, WHITE, (count_box_x, green_box_y, box_width, box_height))
    p.draw.rect(win, WHITE, (count_box_x, yellow_box_y, box_width, box_height))
    
    draw_text(f"Correct Positions: {green_count}", font, BLACK, win, count_box_x + 5, green_box_y + 5)
    draw_text(f"Correct Numbers: {yellow_count + green_count}", font, BLACK, win, count_box_x + 5, yellow_box_y + 5)

def draw_guesses():
    for i in range(len(guesses)):
        guess = guesses[i]
        for j in range(len(guess)):
            draw_text(guess[j], font, BLACK, win, j * 60 + 30, i * 40 + 60)



def draw_numpad():
    buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'X','0', 'OK', 'Reset']
    x_positions = [numpad_x + (numpad_button_size + numpad_button_margin) * (i % 3) for i in range(len(buttons))]
    y_positions = [numpad_y + (numpad_button_size + numpad_button_margin) * (i // 3) for i in range(len(buttons))]

    for i, button in enumerate(buttons):
        x = x_positions[i]
        y = y_positions[i]
        if button == 'OK':
            p.draw.rect(win, WHITE, (x, y, numpad_button_size * 2 + numpad_button_margin, numpad_button_size))
        else:
            p.draw.rect(win, WHITE, (x, y, numpad_button_size, numpad_button_size))
        draw_text(button, font, BLACK, win, x + 10, y + 10)

def draw_play_again_button():
    p.draw.rect(win, GREEN, (play_again_button_x, play_again_button_y, play_again_button_width, play_again_button_height))
    draw_text("Play Again", font, BLACK, win, play_again_button_x + 25, play_again_button_y + 10)

def check_play_again_button(pos):
    if play_again_button_x <= pos[0] <= play_again_button_x + play_again_button_width and \
       play_again_button_y <= pos[1] <= play_again_button_y + play_again_button_height:
        return True
    return False
str_num_list=''.join(map(str,number_list))
def game():
    global user_input, green_count, yellow_count, guesses, hints, number_list, attempts
    run = True
    is_winner = False
    is_loser =False
    clock = p.time.Clock()

    while run:
        win.fill(WHITE) 
        draw_grid()
        draw_guesses()
        draw_hints()
        draw_count_boxes()
        draw_numpad()

        if is_winner or is_loser:
            draw_play_again_button()

        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            if event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()

                if is_winner and check_play_again_button(pos):
                    user_input = ""
                    guesses.clear()
                    hints.clear()
                    green_count = 0
                    yellow_count = 0
                    random.shuffle(num)
                    number_list = num[:number_len]
                    is_winner = False
                else:
                    buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'X','0', 'OK', 'Reset']
                    x_positions = [numpad_x + (numpad_button_size + numpad_button_margin) * (i % 3) for i in range(len(buttons))]
                    y_positions = [numpad_y + (numpad_button_size + numpad_button_margin) * (i // 3) for i in range(len(buttons))]

                    for i, button in enumerate(buttons):
                        x = x_positions[i]
                        y = y_positions[i]
                        rect = p.Rect(x, y, numpad_button_size, numpad_button_size)
                        if button == 'OK':
                            rect.width = numpad_button_size * 2 + numpad_button_margin
                        if rect.collidepoint(pos):
                            if button == 'OK':
                                if len(user_input) == number_len and len(set(user_input)) == number_len:
                                    correctpos = sum(1 for i in range(number_len) if user_input[i] == number_list[i])
                                    eqnum = sum(1 for digit in user_input if digit in number_list)
                                    guesses.append(user_input)
                                    hints.append((correctpos, eqnum - correctpos))
                                    green_count = correctpos
                                    yellow_count = eqnum - correctpos
                                    user_input = ""
                                    attempts +=1
                                    if correctpos == number_len:
                                        is_winner = True
                                    elif attempts >= max_attempts:
                                        is_loser = True
                            elif button == 'X':
                                if len(user_input) > 0:
                                    user_input = user_input[:-1]
                            elif button == 'Reset':
                                user_input = ""
                                guesses.clear()
                                hints.clear()
                                green_count = 0
                                yellow_count = 0
                                attempts = 0
                                random.shuffle(num)
                                number_list = num[:number_len]
                                is_winner = False
                                print(number_list)
                            else:
                                if len(user_input) < number_len and button.isdigit():
                                    if button not in user_input:
                                        user_input += button

        for i in range(len(user_input)):
            draw_text(user_input[i], font, BLACK, win, i * 60 + 30, len(guesses) * 40 + 60)

        if is_winner:
            draw_text("Congratulations, You Win!", font, GREEN, win, width // 2 - 150, height - 200)
        elif is_loser:
            draw_text("You've used all attempts! Game Over", font, RED, win, width // 2 - 250, height - 200)
            draw_text(f"Correct Number is {str_num_list}", font, RED, win, width // 2 - 210, height - 170)
        p.display.flip()
        clock.tick(30)
game()
p.quit()
sys.exit()