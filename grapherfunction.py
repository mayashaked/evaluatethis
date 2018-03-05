# Dyadic Partitioning grapher thingy:

 def plot_w_box(leaves):
     fig = plt.figure()
     ax = fig.add_subplot(111)
     ax.set_xlim(0,1)
     ax.set_ylim(0,1)
     for l in leaves:
         a = l.__repr__().split('|')
         print(a)
         l_x,u_y,u_x,l_y,color = float(a[0]),float(a[1]),float(a[2]),float(a[3]), a[4]
         lower_left_y = l_y
         lower_left_x = l_x
         width = u_x - l_x
         height = u_y - l_y
         print((lower_left_x,lower_left_y,width,height))
         if color == 'bad':
             rect = patches.Rectangle((lower_left_x,lower_left_y), width, height, alpha = .2, fc='r', edgecolor = 'g', lw = 3)
         if color == 'good':
             rect = patches.Rectangle((lower_left_x,lower_left_y), width, height, alpha = .2, fc='b', edgecolor = 'g', lw = 3)
         ax.add_patch(rect)