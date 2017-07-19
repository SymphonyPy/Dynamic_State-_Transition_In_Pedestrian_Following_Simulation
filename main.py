import time
import pygame
from DataParser import open_file

file_path = "data_7_people.xlsx"
background_image_filename="background.png"
windowSize = [720, 540]
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
cyan = 0, 180, 105
pygame.init()
pedestrians = open_file(file_path)
current_index = 0
for i in pedestrians:
    i.smoothy()
bp = max([i.get_end_pos() for i in pedestrians])
sp = min([i.get_start_pos() for i in pedestrians])
larger = 620 / bp - sp
subtract = sp * larger - 50
temp = int((540 - len(pedestrians) * 10) / 2)
y = [i * 10 + temp for i in range(len(pedestrians))]
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
            pygame.draw.circle(screen, red, (int(i.get_position(current_index) * larger - subtract), 270), 5)
    pygame.display.update()
    current_index = round(current_index + 0.01, 2) % 15
    time.sleep(0.001)
