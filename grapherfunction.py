#-------------------------------------------------------------------------------
# Name:        Dyadic Partitioning grapher function
# Purpose:     Visually represents a partition of data using matplotlib.
#
# Author:      Sam Hoffman & Alex Maiorella
#
# Created:     03/04/2018
#-------------------------------------------------------------------------------

from matplotlib import pyplot as plt

def plot_w_box(leaves):
    '''
    Shows graph of partition.
    Inputs:
        a list of 'box' objects as defined in dyadic partitioning module
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    for l in leaves:
        a = repr(l).split('|')
        l_x,u_y,u_x,l_y,color = float(a[0]),float(a[1]),float(a[2]),float(a[3]), a[4]
        lower_left_y = l_y
        lower_left_x = l_x
        width = u_x - l_x
        height = u_y - l_y
        if color == 'bad':
            rect = patches.Rectangle((lower_left_x,lower_left_y), width, height, alpha = .2, fc='r', edgecolor = 'g', lw = 2)
        if color == 'good':
            rect = patches.Rectangle((lower_left_x,lower_left_y), width, height, alpha = .2, fc='b', edgecolor = 'g', lw = 2)
        ax.add_patch(rect)
    plt.show()