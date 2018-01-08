import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

f_esti = open('input/2018_01_06_22_56.txt', 'r')
esti_lines = f_esti.readlines()
f_esti.close()


track_id = 0
count_first = 0
count_second = 0
count_third = 0
track_count = 0
threshold = 400
x_diff_total_first = 0
x_diff_total_second = 0
x_diff_total_third = 0

cur_pos_esti = []
cur_pos_truth = []
cur_speed_esti = []
cur_speed_truth = []
i = 0

while i < len(esti_lines):
    spl = esti_lines[i].split(' ')
    cur_id = spl[0]

    while cur_id == track_id:
        if i == len(esti_lines):
            break
        spl = esti_lines[i].split(' ')
        pos_truth = float(spl[1])
        speed_truth = float(spl[2])
        pos_esti = float(spl[3])
        speed_esti = float(spl[4])
        if pos_truth < 20:
            count_first += 1
            x_diff_total_first += abs(speed_esti - speed_truth)
        elif pos_truth < 45:
            count_second += 1
            x_diff_total_second += abs(speed_esti - speed_truth)
        else:
            count_third += 1
            x_diff_total_third += abs(speed_esti - speed_truth)

        cur_pos_esti.append(pos_esti)
        cur_pos_truth.append(pos_truth)
        cur_speed_esti.append(speed_esti)
        cur_speed_truth.append(speed_truth)

        i += 1
        if i < len(esti_lines):
            cur_id = esti_lines[i].split(' ')[0]


    if len(cur_pos_truth) > threshold:
        print (len(cur_speed_truth))
        # draw
        fig = plt.figure(figsize=(16, 9))
        plt.subplot(2, 1, 1)
        # ax = fig.add_subplot(1, 2, 1)
        major_ticks = np.arange(0, len(cur_pos_truth), 10)
        # plt.set_xticks(major_ticks)
        plt.plot(cur_pos_truth, '-r')
        plt.plot(cur_pos_esti, '-b')
        green_patch = mpatches.Patch(color='red', label='Truth depth')
        red_patch = mpatches.Patch(color='blue', label='Esti depth')
        plt.legend(handles=[red_patch, green_patch])
        plt.grid()

        # ax2 = fig.add_subplot(2, 2, 1)
        plt.subplot(2, 1, 2)
        major_ticks = np.arange(0, len(cur_pos_truth), 10)
        # plt.set_xticks(major_ticks)
        plt.plot(cur_speed_truth, '-r')
        plt.plot(cur_speed_esti, '-b')
        green_patch = mpatches.Patch(color='red', label='Truth speed')
        red_patch = mpatches.Patch(color='blue', label='Esti speed')
        # plt.ylim(-10, 10)
        plt.legend(handles=[red_patch, green_patch])
        plt.grid()

        # plt.show()
        plt.savefig("output/{}.jpg".format(cur_id), dpi=150)

    track_id = cur_id
    cur_pos_esti = []
    cur_pos_truth = []
    cur_speed_esti = []
    cur_speed_truth = []
    i += 1

print "0 - 20m :"
print (x_diff_total_first / count_first)
print "20 - 45m :"
print (x_diff_total_second / count_second)
print "> 45m :"
print (x_diff_total_third / count_third)
