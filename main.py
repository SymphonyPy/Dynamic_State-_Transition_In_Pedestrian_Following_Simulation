import time
import pygame
import viterbi
from DataParser import open_file

file_path = "data_7_people.xlsx"
background_image_filename = "background.png"
windowSize = [720, 540]
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
cyan = 0, 180, 105
colors = [red, green, blue, cyan]

pygame.init()
pedestrians = open_file(file_path)
current_index = 0
for i in pedestrians:
    i.smoothy()
bp = max([i.get_end_pos() for i in pedestrians])
sp = min([i.get_start_pos() for i in pedestrians])
larger = 620 / bp - sp
subtract = sp * larger - 50
temp = int((500 - len(pedestrians) * 20))
y = [i * 20 + temp for i in range(len(pedestrians))]

distance_sequences = [[] for i in range(len(pedestrians))]
while current_index < 15:
    for i in range(1, len(pedestrians)):
        if pedestrians[i - 1].get_position(current_index) and pedestrians[i].get_position(current_index):
            distance_sequences[i].append(
                round(pedestrians[i - 1].get_position(current_index), 3) - round(
                    pedestrians[i].get_position(current_index),
                    3))
        else:
            distance_sequences[i].append(100)
    current_index = round(current_index + 0.01, 2)
distance_sequences[0] = [100 for i in range(len(distance_sequences[1]))]
states_sequences = [viterbi.cal_state_sequence(i) for i in distance_sequences]
while True:
    screen = pygame.display.set_mode(windowSize)
    background = pygame.image.load(background_image_filename).convert()
    screen.fill(white)
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    scoretext = font.render("Curret time:" + str(current_index), 1, black)
    screen.blit(scoretext, (30, 90))
    for i, yy in zip(pedestrians, y):
        if i.get_position(current_index):
            pygame.draw.circle(screen, colors[pedestrians.index(i) % 4],
                               (int(i.get_position(current_index) * larger - subtract), 270), 5)
            font = pygame.font.Font(None, 30)
            scoretext = font.render(states_sequences[pedestrians.index(i)][int(current_index * 100)], 1,
                                    colors[pedestrians.index(i) % 4])
            screen.blit(scoretext, (300, yy))
        # 显示当前位置
        font = pygame.font.Font(None, 30)
        scoretext = font.render(
            "P" + str(pedestrians.index(i) + 1) + ":" + str(round(i.get_position(current_index), 6)), 1,
            colors[pedestrians.index(i) % 4])
        screen.blit(scoretext, (50, yy))
    pygame.display.update()
    current_index = round(current_index + 0.01, 2) % 15
    # time.sleep(0.0001)
