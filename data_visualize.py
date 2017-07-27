import matplotlib.pyplot as plt
from DataParser import open_file


def draw_line(pedestrian):
    x = list(pedestrian.info.keys())
    y = list(pedestrian.info.values())
    x.sort()
    y.sort()
    plt.plot(x, y)


def draw_tamplate_line_for_Leader(Leader):
    x = list(Leader.info.keys())
    y = list(Leader.info.values())
    x.sort()
    y.sort()
    template_line(x, y, 0.4, 0.60)
    template_line(x, y, 0.4, 1.05)
    template_line(x, y, 0.4, 1.50)
    template_line(x, y, 0.7, 0.60)
    template_line(x, y, 0.7, 1.05)
    template_line(x, y, 0.7, 1.50)
    template_line(x, y, 1.0, 0.6)
    template_line(x, y, 1.0, 1.05)
    template_line(x, y, 1.0, 1.50)


def template_line(x, y, time_lag, dis_lag):
    xx = [i + time_lag for i in x]
    yy = [i - dis_lag for i in y]
    plt.plot(xx, yy, ":")


if __name__ == "__main__":
    file_path = "data_7_people.xlsx"
    compared_Leader_No = 5
    compared_Follower_No = 6

    pedestrians = open_file(file_path)
    for pedestrian in pedestrians:
        pedestrian.smoothy()
        draw_line(pedestrian)
    plt.show()

    Leader = pedestrians[compared_Leader_No]
    draw_line(Leader)
    draw_tamplate_line_for_Leader(Leader)

    Follower = pedestrians[compared_Follower_No]
    draw_line(Follower)
    plt.show()
