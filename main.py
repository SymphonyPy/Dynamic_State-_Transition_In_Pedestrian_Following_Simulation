import time
import xlwt
import pygame
import viterbi
from DataParser import open_file

file_path = "data_7_people.xlsx"
running_time = 15
state_keeping_time = 1
background_image_filename = "background.png"
windowSize = [720, 540]
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
cyan = 0, 180, 105
colors = [red, green, blue, cyan]


# Viterbi算法计算状态
def get_states_sequence(pedestrians):
    distance_sequences = [[] for i in range(len(pedestrians))]
    # 获得距离的list，以传入Viterbi
    current_index = 0
    while current_index < running_time:
        for i in range(1, len(pedestrians)):
            if pedestrians[i].start_time <= current_index < pedestrians[i].end_time:
                if pedestrians[i - 1].get_position(current_index) and pedestrians[i].get_position(current_index):
                    distance_sequences[i].append(round(pedestrians[i - 1].get_position(current_index), 3) - round(
                        pedestrians[i].get_position(current_index), 3))
                else:
                    distance_sequences[i].append(100)
        current_index = round(current_index + 0.01, 2)
    distance_sequences[0] = [100 for i in
                             range(int(pedestrians[0].start_time * 100), int(pedestrians[0].end_time * 100))]
    states_sequences = [viterbi.cal_state_sequence(i) for i in distance_sequences]
    return states_sequences


# 为状态停留做计算
def deal_with_state_sequences(states_sequences):
    keeping_num = int(state_keeping_time / 0.01)
    for states_sequence in states_sequences:
        i = 0
        # # 找到起始位置（因为点出现的时间不同，没出现时默认状态为FF）
        # if states_sequences.index(states_sequence) != 0:
        #     for i in range(len(states_sequence)):
        #         if states_sequence[i] != "FF":
        #             break
        #         else:
        #             states_sequence[i] = ""
        while i < len(states_sequence):
            end_index = min(i + keeping_num, len(states_sequence) - 1)
            for j in range(i + 1, end_index):
                states_sequence[j] = states_sequence[i]
            i = i + keeping_num


# 将状态存到output_state_sequence.xlsx
def save_states_sequences(pedestrians, states_sequences):
    # 创建 xls 文件对象
    wb = xlwt.Workbook()
    # 新增一个表单
    sh = wb.add_sheet('Sheet1')
    # 按位置添加数据
    for col in range(len(states_sequences)):
        sh.write(0, col + 1, label="P" + str(col + 1))
    for row in range(running_time * 100 + 1):
        sh.write(row + 1, 0, label=round(row / 100, 2))
    for num in range(len(pedestrians)):
        col = num + 1
        for time in range(int(pedestrians[num].start_time * 100), int(pedestrians[num].end_time * 100 - 2)):
            # print(num)
            # print(int(pedestrians[num].start_time * 100))
            # print(int(pedestrians[num].end_time * 100))
            # print(len(states_sequences[6]))
            sh.write(time + 1, col, states_sequences[num][time - int(pedestrians[num].start_time * 100)])
    # 保存文件
    wb.save('output_state_sequence.xls')


# 各种参数，包括使整个图形填满画面
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

# Viterbi算法计算状态
states_sequences = get_states_sequence(pedestrians)
# 为状态停留做计算
deal_with_state_sequences(states_sequences)
# 将状态存到output_state_sequence.xlsx
save_states_sequences(pedestrians, states_sequences)
# 动画演示
current_index = 0
while current_index <= running_time:
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
            # 显示当前状态
            font = pygame.font.Font(None, 30)
            scoretext = font.render(
                states_sequences[pedestrians.index(i)][(int(current_index - i.start_time) * 100) - 1],
                1, colors[pedestrians.index(i) % 4])
            screen.blit(scoretext, (300, yy))
        # 显示当前位置坐标
        font = pygame.font.Font(None, 30)
        scoretext = font.render(
            "P" + str(pedestrians.index(i) + 1) + ":" + str(round(i.get_position(current_index), 6)), 1,
            colors[pedestrians.index(i) % 4])
        screen.blit(scoretext, (50, yy))
    pygame.display.update()
    current_index = round(current_index + 0.01, 2)
