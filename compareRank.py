#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Compare rank (exact SHAP-score and SHAP-score of shap-tool)
#   Author: Xuanxiang Huang
#
################################################################################
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
################################################################################


def plot_wrong_pairs(data, len_X, fig_title, filename):
    plt.rcdefaults()
    y_pos = np.arange(len_X)
    plt.bar(y_pos, data, align='center')
    plt.xticks(np.arange(0, len_X, step=2))
    plt.ylabel('#Instances')
    plt.xlabel('#Wrong pairs')
    plt.title(fig_title)
    plt.savefig(filename)
    plt.clf()
    plt.cla()
    plt.close()


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) >= 1 and args[0] == '-bench':
        bench_name = args[1]
        with open(bench_name, 'r') as fp:
            name_list = fp.readlines()
        for item in name_list:
            name = item.strip()
            print(f"################## {name} ##################")
            b_data = pd.read_csv(f"scores/all_points/barcelo/{name}.csv")
            l_data = pd.read_csv(f"scores/all_points/lundberg/{name}.csv")

            b_score = b_data.to_numpy()
            l_score = l_data.to_numpy()

            # distance based on pair comparison
            n, m = b_score.shape
            l_wrong_pairs = [0] * int((m * (m - 1)) / 2 + 1)
            for k in range(n):
                l_wrong = 0
                for i in range(m):
                    for j in range(i + 1, m):
                        if b_score[k, i] < b_score[k, j]:
                            if l_score[k, i] >= l_score[k, j]:
                                l_wrong += 1
                        elif b_score[k, i] == b_score[k, j]:
                            if l_score[k, i] != l_score[k, j]:
                                l_wrong += 1
                        else:
                            # b_score[k, i] > b_score[k, j]
                            if l_score[k, i] <= l_score[k, j]:
                                l_wrong += 1
                l_wrong_pairs[l_wrong] += 1

            output = pd.DataFrame(data=np.array([[i for i in range(int((m * (m - 1)) / 2 + 1))], l_wrong_pairs]).transpose(),
                                  columns=['#wrong pairs', '#instances'])
            output.to_csv(f"scores/all_points/wrong_pairs/b_lundberg/{name}.csv", index=False)
            plot_wrong_pairs(np.asarray(l_wrong_pairs), int((m * (m - 1)) / 2 + 1), name,
                             f"scores/all_points/wrong_pairs/b_lundberg/{name}.png")
