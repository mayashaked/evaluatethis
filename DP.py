#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     02/03/2018
# Copyright:   (c) alex 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from statistics import mode
COSTS = {}
LAMBDA = None


class DataPoint:

    def __init__(self, x, y, category):
        self.x = x
        self.y = y
        self.category = category

    def __repr__(self):
        return "({},{})|{}".format(self.x, self.y, self.category)

class Box:

    def __init__(self, upper_left_x, upper_left_y, height, width, data):
        self.x = upper_left_x
        self.y = upper_left_y
        self.height = height
        self.width = width
        self.data = data
        self.category = 'good'
        if self.data:
            try:
                self.category = mode([d.category for d in data])
            except:
                self.category = 'bad'


    def __repr__(self):
        return "{}|{}|{}|{}|{}".format(self.x, self.y, self.x + self.width, self.y - self.height, self.category)

    def vert_boxes(self):

        top_data = [d for d in self.data if d.y >= (self.y - self.height / 2)]
        bot_data = [d for d in self.data if d.y < (self.y - self.height / 2)]
        top = Box(self.x, self.y, self.height / 2, self.width, top_data)
        bot = Box(self.x, self.y - self.height / 2, self.height / 2, self.width, bot_data)

        return top, bot

    def horiz_boxes(self):

        right_data = [d for d in self.data if d.x >= (self.x + self.width / 2)]
        left_data = [d for d in self.data if d.x < (self.x + self.width / 2)]

        right = Box(self.x + self.width / 2, self.y, self.height, self.width / 2, right_data)
        left = Box(self.x, self.y, self.height, self.width / 2, left_data)

        return left, right

    def error(self):
        incorrect = 0
        for d in self.data:
            if d.category != self.category:
                incorrect += 1
        return incorrect


    def leaf_cost(self):

        return self.error() + LAMBDA

    def vert_cost(self, level):

        top, bot = self.vert_boxes()

        return top.cost(level - 1) + bot.cost(level - 1)

    def horiz_cost(self, level):

        left, right = self.horiz_boxes()

        return right.cost(level - 1) + left.cost(level - 1)

    def cost(self, level):

        global COSTS

        if self.__repr__() in COSTS:
            c = COSTS[self.__repr__()]
            return c

        if level == 0:
            c = self.leaf_cost()
            COSTS[self.__repr__()] = c
            return c

        c =  min(self.horiz_cost(level), self.vert_cost(level), self.leaf_cost())
        COSTS[self.__repr__()] = c
        return c

def find_ideal_partition(level, box, leaves):

    if level == 0:
        leaves.append(box)

    else:

        leaf_c = box.leaf_cost()
        horiz_c = box.horiz_cost(level)
        vert_c = box.vert_cost(level)
        if leaf_c <= horiz_c and leaf_c <= vert_c:
            leaves.append(box)

        elif horiz_c < leaf_c and horiz_c <= vert_c:
            left, right = box.horiz_boxes()
            find_ideal_partition(level - 1, left, leaves)
            find_ideal_partition(level - 1, right, leaves)

        elif vert_c < horiz_c and vert_c < leaf_c:
            top, bot = box.vert_boxes()
            find_ideal_partition(level - 1, top, leaves)
            find_ideal_partition(level - 1, bot, leaves)

    return leaves

def initialize_box(good, bad):
    data = []
    for i in good:
        data.append(DataPoint(i[0], i[1],'good'))
    for i in bad:
        data.append(DataPoint(i[0], i[1], 'bad'))

    return Box(0,1,1,1,data)


def go(good, bad, pts_to_classify, level, lambda_):

    global LAMBDA
    LAMBDA = lambda_

    box = initialize_box(good, bad)
    leaves = find_ideal_partition(level, box, [])
    classified = classify(pts_to_classify, leaves)

    return classified


def classify(pts_to_classify, leaves):

    classified = []

    for p in pts_to_classify:
        for leaf in leaves:
            min_x, max_y, max_x, min_y, cat = leaf.__repr__().split('|')
            if p[1] >= float(min_x):
                if p[1] < float(max_x):
                    if p[2] >= float(min_y):
                        if p[2] < float(max_y):
                            classified.append((p[0], p[1], p[2], cat))
                            break

    return classified


