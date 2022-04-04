import tkinter
import tkinter as tk
import dataloader as dt
import threading
import datetime
from tkinter import ttk
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


data_list = dt.get_table_list()

# 第1步，实例化object，建立窗口window
window = tkinter.Tk()

# 第2步，给窗口的可视化起名字
window.title('{0-1}KP实例数据集算法实验平台')
# 第3步，设定窗口的大小(长 * 宽)
center_window(window, 700, 400)
window.configure(bg='white')

import sys

sys.setrecursionlimit(1000000)
import time
import matplotlib.pyplot as plt
import pandas as pd


class article:
    def __init__(self, profit, weight):
        self.profit = profit
        self.weight = weight
        self.cmp = self.profit / self.weight

    def __str__(self):
        return "profit:" + str(self.profit) + " weight:" + str(self.weight)


class item:
    def __init__(self, fir, sec, thr):
        self.pack = [fir, sec, thr]

    def __str__(self):
        return "(1)" + self.pack[0].__str__() + " (2)" + self.pack[1].__str__() + " (3)" + self.pack[2].__str__()


class Back_pack:

    def __init__(self, d, cubage, profit_in, weight_in):
        self.d = d
        self.cubage = cubage
        self.str_profit = [i for i in profit_in.split(',')]
        self.str_weight = [i for i in weight_in.split(',')]
        # 处理价值数据集和重量数据集
        j = 1
        self.items = []  # 封存数据集的对象列表
        tmp = []
        for i in range(d):
            tmp.append(article(int(self.str_profit[i]), int(self.str_weight[i])))
            if j == 3:
                self.items.append(item(tmp[0], tmp[1], tmp[2]))
                tmp = []
                j = 1
            else:
                j += 1
        self.items.sort(key=lambda x: x.pack[2].cmp, reverse=True)  # 按照第三项的价值重量比降序排序
        self.max_val = 0
        self.val = 0
        self.size = self.d // 3  # 数据集组数
        self.so_res = []  # 保存最优解解向量结果
        self.so_tmp = []  # 保存解向量中间结果
        self.so_ve = [[0, 0, 0] for i in range(self.size)]  # 解向量矩阵
        self.stime = 0  # 运行时间

    def show_result(self):  # 保存结果
        if self.so_res != []:
            show.insert('end', "按照第三项的价值重量比降序排序后的向量为：\n")
            for item in self.items:
                show.insert('end', str(item.__str__()) + "\n")
            show.insert('end', "对应上方按照第三项的价值重量比降序排序后向量的解向量为：\n")
            for i in self.so_ve:
                show.insert('end', str(i.__str__()) + "\n")

    def save(self):  # 保存结果
        now = datetime.datetime.now()
        time = now.strftime("%m-%d-%H-%M")
        with open(time + ".txt", 'w', encoding='utf-8') as f:
            f.write("运行算法:%s\n" % str(com2_selected))
            f.write("数据集:%s\n" % str(com1_selected))
            f.write("数据集大小:%s\n" % str(self.d))
            f.write("包裹的最大容量：%s\n" % str(self.cubage))
            f.write("价值数据集:%s\n" % str(self.str_profit))
            f.write("重量数据集：%s\n" % str(self.str_weight))
            f.write("能够获得的最大价值:%s\n" % str(self.max_val))
            f.write("得出最优解的运行时间：%s\n" % str(self.stime))
            if self.so_res != []:
                f.write("按照第三项的价值重量比降序排序后的向量：\n")
                for item in self.items:
                    f.write(item.__str__() + '\n')
                f.write('\n')
                f.write("对应上方按照第三项的价值重量比降序排序后向量的解向量：\n")
                for i in self.so_ve:
                    f.write(i.__str__() + '\n')

    def deal_so(self):  # 处理解向量矩阵
        for (i, j) in self.so_res:
            self.so_ve[i][j] = 1

    def run(self, suanfa):
        if (suanfa == "回溯算法"):
            start = time.time()
            self.Backtracking(-1, 0, self.cubage)
            end = time.time()
            t = end - start
        else:
            start = time.time()
            self.DP()
            end = time.time()
            t = end - start
        self.stime = t
        show.insert('end', "执行完毕！" + '\n')
        show.insert('end', "能够获得的最大价值为:" + str(self.max_val) + '\n')
        if self.so_res != []:
            show.insert('end', "使用回溯算法得出最优解经过的项目为:" + str(self.so_res) + '\n')
            self.deal_so()
        show.insert('end', "得出最优解的运行时间为：" + str(self.stime) + 's' + '\n')
        self.show_result()
        self.save()

    def DP(self):  # 动态规划算法
        dp = [[[0 for k in range(self.cubage + 5)] for i in range(4)] for j in range(self.size + 5)]  # 三维dp数组
        for k in range(1, self.size + 1):
            for i in range(1, 4):
                for v in range(self.cubage + 1):
                    for j in range(1, 4):
                        dp[k][i][v] = max(dp[k][i][v], dp[k - 1][j][v])
                        if v >= self.items[k - 1].pack[i - 1].weight:
                            dp[k][i][v] = max(dp[k][i][v], dp[k - 1][j][v - self.items[k - 1].pack[i - 1].weight] +
                                              self.items[k - 1].pack[i - 1].profit)
                        self.max_val = max(self.max_val, dp[k][i][v])

    def bound(self, k, caup):  # 计算上界函数，功能为剪枝
        ans = self.val
        while k < self.size and caup >= self.items[k].pack[2].weight:
            caup -= self.items[k].pack[2].weight
            ans += self.items[k].pack[2].profit
            k += 1
        if k < self.size:
            ans += self.items[k].pack[2].profit / self.items[k].pack[2].weight * caup
        return ans

    def Backtracking(self, k, i, caup):  # 回溯算法
        bound_val = self.bound(k + 2, caup)
        if k == self.size - 1:
            if self.max_val < self.val:
                self.max_val = self.val
                self.so_res = list.copy(self.so_tmp)
            return
        for j in range(3):
            if caup >= self.items[k + 1].pack[j].weight:
                self.val += self.items[k + 1].pack[j].profit
                self.so_tmp.append((k + 1, j))
                self.Backtracking(k + 1, j, caup - self.items[k + 1].pack[j].weight)
                self.so_tmp.pop()
                self.val -= self.items[k + 1].pack[j].profit
            if bound_val > self.max_val:
                self.Backtracking(k + 1, j, caup)


com1_selected = tk.StringVar()
com1_selected = data_list[0]
comdata1 = data_list
comvalue1 = tk.StringVar()
comvalue2 = tk.StringVar()
comdata2 = ["动态规划算法", "回溯算法"]
com2_selected = tk.StringVar()
com2_selected = comdata2[0]

title_area = tk.Frame()
function_area = tk.Frame()
show_area = tk.Frame()

photo = tk.PhotoImage(file='logo.png')

img = tk.Label(title_area, image=photo, font=('Arial', 12)).pack(side='left', expand='no', fill='x')
title = tk.Label(title_area, text='{0-1}KP实例数据集算法实验平台', bg='white', font=('Arial', 18)).pack(side='right', expand='no', fill='y')


def combox1_get(*args):
    global com1_selected
    com1_selected = combox1.get()


label1 = tk.Label(function_area, text='数据集选择:', font=('Arial', 12)).pack(side='left', expand='no')
combox1 = ttk.Combobox(function_area, textvariable=comvalue1)
combox1.pack(side='left', expand='no')
# 设置下拉数据
combox1["value"] = comdata1
combox1.bind("<<ComboboxSelected>>", combox1_get)

# 设置默认值
combox1.current(0)


def combox2_get(*args):
    global com2_selected
    com2_selected = combox2.get()


label2 = tk.Label(function_area, text='算法选择:', font=('Arial', 12)).pack(side='left', expand='no')
combox2 = ttk.Combobox(function_area, textvariable=comvalue2)
combox2.pack(side='left', expand='no')
# 设置下拉数据
combox2["value"] = comdata2
# 设置默认值
combox2.current(0)
combox2.bind("<<ComboboxSelected>>", combox2_get)


def start():
    global com1_selected, com2_selected
    sets = dt.get_data(com1_selected)
    for i in sets:
        show.insert('end', "当前正在运算：" + str(i['id']) + '\n')
        d = i['size']
        cubage = i['capacity']
        profit_in = i['profit']
        weight_in = i['weight']
        bp = Back_pack(d, cubage, profit_in, weight_in)
        bp.run(com2_selected)


def start_excute():
    global com1_selected, com2_selected
    show.delete(1.0, tk.END)
    show.insert('end', "选择的数据集为：" + com1_selected + '\n')
    show.insert('end', "选择的算法为：" + com2_selected + '\n')
    show.insert('end', "开始执行......\n")
    T = threading.Thread(target=start)
    T.start()


button_start = tk.Button(function_area, text='开始执行', command=start_excute).pack(side='left', expand='no')
show = tk.Text(show_area, font=('Arial', 12), relief='solid')
show.pack(side='left', expand='yes', fill='both')
scrollbar = tk.Scrollbar(show_area)
scrollbar.pack(side='left', fill='y')  # 必须填充
show['yscrollcommand'] = scrollbar.set
scrollbar['command'] = show.yview
show.insert('end', "欢迎使用！请选择数据集和算法后，点击开始执行按钮！")
# Filepath = filedialog.askopenfilename()
title_area.pack(side='top', expand='no', fill='both')
function_area.pack(side='top', expand='no', fill='both')
show_area.pack(side='top', expand='yes', fill='both')
# 第4步，在图形界面上设定标签
# l = tk.Label(window, text='你好！this is Tkinter', bg='green', font=('Arial', 12), width=30, height=2)
# 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高

# 第5步，放置标签
# l.pack()  # Label内容content区域放置位置，自动调节尺寸
# 放置lable的方法有：1）l.pack(); 2)l.place();


if __name__ == "__main__":
    window.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
# 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。
