import numpy as np

with open('aoc_5_data') as f:
    data = f.readlines()

part_2 = False


class Line:

    def __init__(self, raw_line):
        coordinates = raw_line.replace('\n', '').split(' -> ')
        self.points = np.array([[int(x) for x in coordinate.split(',')] for coordinate in coordinates])

    def get_points(self):
        if self.points[0, 0] == self.points[1, 0]:
            return np.array([[self.points[0, 0], int(x)]
                             for x in np.linspace(self.points[0, 1], self.points[1, 1],
                                                  np.abs(self.points[1, 1] - self.points[0, 1]) + 1)])
        elif self.points[0, 1] == self.points[1, 1]:
            return np.array([[int(x), self.points[0, 1]]
                             for x in np.linspace(self.points[0, 0], self.points[1, 0],
                                                  np.abs(self.points[1, 0] - self.points[0, 0]) + 1)])
        else:
            if part_2:
                y_range = np.linspace(self.points[0, 1], self.points[1, 1],
                                      np.abs(self.points[1, 1] - self.points[0, 1]) + 1)
                x_range = np.linspace(self.points[0, 0], self.points[1, 0],
                                      np.abs(self.points[1, 0] - self.points[0, 0]) + 1)
                return np.array([[int(x_range[i]), int(y_range[i])] for i in range(len(x_range))])
            else:
                return np.array([])

    def cover_points(self, field_f):
        points = self.get_points()
        for point in points:
            if len(point) > 0:
                field_f[point[0], point[1]] = field_f[point[0], point[1]] + 1
        return field_f


field = np.zeros((1000, 1000))

for row in data:
    line = Line(row)
    field = line.cover_points(field)

print(np.sum(field >= 2))
