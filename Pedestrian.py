class Pedestrian(object):
    def __init__(self):
        self.info = {}
        self.start_time = 0
        self.end_time = 0

    def get_start_pos(self):
        return self.info[list(self.info.keys())[0]]

    def get_end_pos(self):
        return self.info[list(self.info.keys())[-1]]

    def add_info(self, info):
        self.info[info[0]] = info[1]

    def get_position(self, time):
        if time in self.info.keys():
            if self.info[time]:
                return self.info[time]
            else:
                return False
        else:
            return False

    def smoothy(self):
        temp = []
        for i in self.info.keys():
            if not self.info[i]:
                temp.append(i)
        for i in temp:
            del self.info[i]
        self.start_time = list(self.info.keys())[0]
        self.end_time = list(self.info.keys())[-1]
        keys = list(self.info.keys())
        for i in keys[:-1]:
            interval = (self.info[round(i + 0.1, 3)] - self.info[round(i, 3)]) / 10
            for j in range(1, 10):
                time = round(i + j / 100, 2)
                self.add_info((time, self.info[i] + j * interval))
