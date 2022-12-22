import board
import displayio
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_clue import clue
import terminalio
from adafruit_display_text.label import Label
import time
import random

display = board.DISPLAY

change_distance = 5
character_size = 10
screen_width = 240
display_right_side = screen_width - change_distance - character_size
advance_speed = 5
initial_block_delay = 1000
collision = False


class Character:
    def __init__(self, x_pos, y_pos, height, width):
        self.x = x_pos
        self.y = y_pos
        self.height = height
        self.width = width

class Block:
    def __init__(self, x_pos, y_pos, height, width):
        self.x = x_pos
        self.y = y_pos
        self.height = height
        self.width = width

def main():
    character_x = 120
    character_y = 200
    blocks = []
    character = Character(character_x, character_y, character_size, character_size)
    initial_delay = 50
    delay = initial_delay
    block_delay = initial_block_delay
    blocks = add_blocks(blocks)
    global collision
    score = 0

    while collision == False:
        if delay == 0:
            screen = displayio.Group()
            if block_delay == 0:
                blocks = add_blocks(blocks)
                block_delay = initial_block_delay
            handle_button_press(character)
            draw_object(character, screen)
            advance_blocks(blocks)
            blocks = remove_blocks(blocks)

            for block in blocks:
                collision = check_for_collision(character, block) #<--this doesn't work as expected
                #if check_for_collision(character, block):        #<-- these two statements do work
                #    collision = True                             #<-- so why does collision scope out differently here?

            for block in blocks:
                draw_object(block, screen)

            draw_score(score, screen)
            display.show(screen)
            delay = initial_delay

        delay = delay - 1
        block_delay = block_delay - 1


    process_game_over(score, screen)

def handle_button_press(character):
    if clue.button_a:
        if character.x > 0:
            character.x = character.x - change_distance
    if clue.button_b:
        if character.x < display_right_side:
            character.x = character.x + change_distance
    return

def draw_object(obj, screen):
    screen.append(Rect(obj.x, obj.y, obj.width, obj.height, fill=0x999999))
    return

def draw_score(score, screen):
    score = "Score: " + str(score)
    screen.append(Label(terminalio.FONT, text=score))
    return

def add_blocks(blocks):
    side = random.randrange(0,1)
    length = random.randrange(30, 200)
    block = Block(0, 30, 5, length)
    blocks.append(block)
    return blocks

def remove_blocks(blocks):
    new_blocks = []
    for block in blocks:
        if block.y <= 240:
            new_blocks.append(block)
    return new_blocks

def advance_blocks(blocks):
    for block in blocks:
        block.y = block.y + advance_speed
    return

def check_for_collision(character, block):
    if character.y == block.y:
        for i in range(character.x, character.x + character.width):
            if i in range(block.x, block.x + block.width):
                print(f"{character.x} {character.x + character.width} {block.x} {block.x + block.width}")

                return True
    else:
        return False

def process_game_over(score, screen):
    game_over_screen = displayio.Group()
    score = "Score: " + str(score)
    screen.append(Label(terminalio.FONT, text=score))
    display.show(screen)

    for i in range(5):
        clue.play_tone(440, .25)
        clue.play_tone(587, .25)



    while True:
        pass
    return

if __name__ == "__main__":
    main()
