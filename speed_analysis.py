import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

def speed_plot(ax, truth, esti, fontsize=12, label='x-diff'):
    ax.plot(truth, '-r')
    ax.plot(esti, '-b')

    ax.locator_params(nbins=3)
    ax.set_xlabel('time', fontsize=fontsize)
    ax.set_ylabel(label, fontsize=fontsize)

    # ax.set_title(label, fontsize=fontsize)

f_esti = open('input/esti_speed.txt', 'r')
esti_lines = f_esti.readlines()
f_esti.close()

f_truth = open('input/truth_speed.txt', 'r')
truth_lines = f_truth.readlines()
f_truth.close()

track_id = 0
count_first = 0
count_second = 0
count_third = 0
track_count = 0
cur_count = 0
x_diff_total_first = 0
y_diff_total_first = 0
x_diff_total_second = 0
y_diff_total_second = 0
x_diff_total_third = 0
y_diff_total_third = 0
cur_x_esti = []
cur_x_truth = []
cur_y_esti = []
cur_y_truth = []

for i in range(0, len(esti_lines), 1):
    if esti_lines[i].startswith("###"):
        spl = esti_lines[i].split(' ')
        cur_id = track_id
        track_id = spl[3]
        if cur_id == 2826:
            print len(cur_x_esti)
        if track_count != 0 and cur_count > 350:
            # fig, ax1 = plt.subplots(nrows=1, ncols=1)
            # fig = plt.figure(figsize=(4, 3))
            # speed_plot(ax1, cur_x_truth, cur_x_esti)
            # speed_plot(ax2, cur_y_truth, cur_y_esti, label='y-diff')

            fig = plt.figure(figsize=(10, 3))
            plt.plot(cur_x_truth, '-r')
            plt.plot(cur_x_esti, '-b')
            green_patch = mpatches.Patch(color='red', label='Truth speed')
            red_patch = mpatches.Patch(color='blue', label='Esti speed')
            plt.ylim(-20, 20)
            plt.legend(handles=[red_patch, green_patch])
            plt.savefig("output/{}.jpg".format(cur_id), dpi=150)

            # plt.tight_layout()
            # plt.show()
        cur_count = 0
        track_count += 1
        cur_x_esti = []
        cur_y_esti = []
        cur_x_truth = []
        cur_y_truth = []
    else:
        cur_count += 1
        esti_speed = esti_lines[i].split(',')
        truth_speed = truth_lines[i].split(',')
        position_x = float(esti_speed[2])
        x_esti = float(esti_speed[0])
        x_truth = float(truth_speed[0])
        y_esti = float(esti_speed[1])
        y_truth = float(truth_speed[1])
        x_diff = abs(x_esti + x_truth)
        y_diff = abs(y_esti + y_truth)
        if position_x < 20 :
            count_first += 1
            x_diff_total_first += x_diff
            y_diff_total_first += y_diff
        elif position_x < 45:
            count_second += 1
            x_diff_total_second += x_diff
            y_diff_total_second += y_diff
        else:
            count_third += 1
            x_diff_total_third += x_diff
            y_diff_total_third += y_diff
        cur_x_esti.append(-x_esti)
        cur_y_esti.append(-y_esti)
        cur_x_truth.append(x_truth)
        cur_y_truth.append(y_truth)
        # print(x_diff, y_diff, track_id)

print "0 - 20m :"
print (x_diff_total_first / count_first, y_diff_total_first / count_first)
print "20 - 45m :"
print (x_diff_total_second / count_second, x_diff_total_second / count_second)
print "> 45m :"
print (x_diff_total_third / count_third, x_diff_total_third / count_third)