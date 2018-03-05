#-------------------------------------------------------------------------------
# Name:        Dyadic Partitioning Module
# Purpose:     Extrapolates data from questions such as "Would you recommend
#              this course?" from a subset of our data to the rest by
#              implementing dyadic partitioning.
#
# Author:      Alex Maiorella
#
# Created:     02/03/2018
#-------------------------------------------------------------------------------

from statistics import mode
import pandas as pd

# COSTS is a variable used for memoization during recursion to avoid unnecessary
# computation.
# LAMBDA represents the cost of declaring a leaf. Initialized to None.
COSTS = {}
LAMBDA = None

class DataPoint:
    '''
    This class represents a single element of the training data. It has x and
    y coordinates and the category that it belongs to.
    '''
    def __init__(self, x, y, category):
        self.x = x
        self.y = y
        self.category = category

    def __repr__(self):
        return "({},{})|{}".format(self.x, self.y, self.category)

class Box:
    '''
    This class models a 'box' of data, a piece of the partition being created.
    Naturally it has dimensions, as well as the data living inside and its
    category, which is assigned by majority rule.
    '''
    def __init__(self, upper_left_x, upper_left_y, height, width, data):
        self.x = upper_left_x
        self.y = upper_left_y
        self.height = height
        self.width = width
        self.data = data
        try:
            self.category = mode([d.category for d in data])
        except:
            self.category = 'bad'


    def __repr__(self):
        return "{}|{}|{}|{}|{}".format(self.x, self.y, self.x + self.width, \
            self.y - self.height, self.category)

    def vert_boxes(self):
        '''
        Slices the box in half and returns resulting box objects.
        '''
        top_data = [d for d in self.data if d.y >= (self.y - self.height / 2)]
        bot_data = [d for d in self.data if d.y < (self.y - self.height / 2)]
        top = Box(self.x, self.y, self.height / 2, self.width, top_data)
        bot = Box(self.x, self.y - self.height / 2, self.height / 2, \
            self.width, bot_data)

        return top, bot

    def horiz_boxes(self):
        '''
        Slices the box in half (the other way) and returns resulting
        box objects.
        '''
        right_data = [d for d in self.data if d.x >= (self.x + self.width / 2)]
        left_data = [d for d in self.data if d.x < (self.x + self.width / 2)]

        right = Box(self.x + self.width / 2, self.y, self.height, self.width \
            / 2, right_data)
        left = Box(self.x, self.y, self.height, self.width / 2, left_data)

        return left, right

    def error(self):
        '''
        Computes the error of a box, defined as the number of points of the
        opposite category it contains.
        '''
        incorrect = 0
        for d in self.data:
            if d.category != self.category:
                incorrect += 1

        return incorrect

    def leaf_cost(self):
        '''
        Returns the cost of declaring a leaf
        '''
        return self.error() + LAMBDA

    def vert_cost(self, level):
        '''
        Computes the cost of splitting vertically, makes recursive calls to
        do so.
        '''
        top, bot = self.vert_boxes()
        return top.cost(level - 1) + bot.cost(level - 1)

    def horiz_cost(self, level):
        '''
        Computes the cost of splitting horizontally, makes recursive calls to
        do so.
        '''
        left, right = self.horiz_boxes()
        return right.cost(level - 1) + left.cost(level - 1)

    def cost(self, level):
        '''
        Computes the absolute cost of a given box, makes recursive calls
        to horiz_cost and vert_cost as needed. Stores that information
        in global variable in order to 'memoize' and speed up the process.
        '''
        global COSTS

        if self.__repr__() in COSTS:
            c = COSTS[repr(self)]
            return c

        if level == 0:
            c = self.leaf_cost()
            COSTS[repr(self)] = c
            return c

        c =  min(self.horiz_cost(level), self.vert_cost(level), \
            self.leaf_cost())

        COSTS[repr(self)] = c
        return c

def find_ideal_partition(level, box, leaves):
    '''
    Given a box of data, find its ideal partition (minimizing cost)
    Inputs:
        level: maximum number of splits allowed
        box: box of DataPoint objects to partition
        leaves: used to store the leaves (boxes that comprise the ideal
          partition) during the recursion
    Returns:
        leaves (ideal partition)
    '''

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
    '''
    Create initial box of data, 100 x 100 dimension for our purposes
    '''
    data = []
    for i in good:
        data.append(DataPoint(i[0], i[1],'good'))
    for i in bad:
        data.append(DataPoint(i[0], i[1], 'bad'))

    return Box(0,100,100,100,data)


def classify(pts_to_classify, leaves):
    '''
    Classify new data based on the ideal partition that has been found.
    '''

    classified = []

    for p in pts_to_classify:
        for leaf in leaves:
            min_x, max_y, max_x, min_y, cat = leaf.__repr__().split('|')
            if p[1] >= float(min_x):
                if p[1] < float(max_x):
                    if p[2] >= float(min_y):
                        if p[2] < float(max_y):
                            classified.append((p[0], cat))
                            break

    return classified


def go(df, level = 10, lambda_ = 3):
    '''
    Takes in our evaluations DataFrame, extracts the training data,
    runs the dyadic partitioning algorithm on the training data,
    classifies the remaining data based on the partition.

    This process happens for both "Would you recommend this course?"
    data and "Was your instructor good overall?" data. Finally, we return
    an updated DataFrame.
    '''

    global LAMBDA
    LAMBDA = lambda_

    good_df = df[df.num_recommend \
        / df.num_dont_recommend >= 6].loc[:,['inst_sentiment','prof_score']]
    good = list(good_df.itertuples(index=False, name = None))
    bad_df = df[df.num_recommend \
        / df.num_dont_recommend < 6].loc[:,['inst_sentiment','prof_score']]
    bad = list(bad_df.itertuples(index=False, name = None))

    good_prof_test_df = \
        df[pd.isnull(df.good_inst)].loc[:,['inst_sentiment','prof_score']]
    good_prof_test = list(good_prof_test_df.itertuples(index=True, name = None))

    box = initialize_box(good, bad)
    leaves = find_ideal_partition(level, box, [])
    good_prof_classified = classify(good_prof_test, leaves)

    # Reset the COSTS before running algorithm on new type of data
    global COSTS
    COSTS = {}

    rec_df = df[df.num_recommend \
        / df.num_dont_recommend >= 5].loc[:,['course_sentiment','prof_score']]
    rec = list(rec_df.itertuples(index=False, name = None))
    no_rec_df = df[df.num_recommend \
        / df.num_dont_recommend < 5].loc[:,['course_sentiment','prof_score']]
    no_rec = list(no_rec_df.itertuples(index=False, name = None))

    rec_test_df = \
        df[pd.isnull(df.num_recommend)].loc[:,['course_sentiment','prof_score']]
    rec_test = list(rec_test_df.itertuples(index=True, name = None))

    box = initialize_box(rec, no_rec)
    leaves = find_ideal_partition(level, box, [])
    recommend_classified = classify(rec_test, leaves)

    new_rec_column = pd.Series(dict(recommend_classified), \
        name = 'would_recommend')
    new_inst_quality = pd.Series(dict(good_prof_classified), \
        name = 'would_like_inst')

    return pd.concat([df, new_inst_quality, new_rec_column], axis = 1)


