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

    def save(self):  # 保存结果
        file = input("请输入想要保存的文件名，不需要添加后缀名:")
        with open(file + ".txt", 'w', encoding='utf-8') as f:
            f.write("能够获得的最大价值为:%d\n" % self.max_val)
            f.write("得出最优解的运行时间为：%fs\n" % self.stime)
            if self.so_res != []:
                f.write("按照第三项的价值重量比降序排序后的向量为：\n")
                for item in self.items:
                    f.write(item.__str__() + '\n')
                f.write('\n')
                f.write("对应上方按照第三项的价值重量比降序排序后向量的解向量为：\n")
                for i in self.so_ve:
                    f.write(i.__str__() + '\n')

    def deal_so(self):  # 处理解向量矩阵
        for (i, j) in self.so_res:
            self.so_ve[i][j] = 1

    def draw(self):  # 画散点图
        nums_pro = self.str_profit[0:len(self.str_profit)]
        nums_wei = self.str_weight[0:len(self.str_weight)]
        nums_pro = [int(i) for i in nums_pro]
        nums_wei = [int(i) for i in nums_wei]
        df = pd.DataFrame({'profit': nums_pro, 'weight': nums_wei})
        df.plot(kind="scatter", x="weight", y="profit")
        plt.show()

    def run(self):  # 控制面板
        print("请选择你的操作")
        print("1 -- 绘制图像")
        print("2 -- 使用算法求解问题得到最优解")
        select = int(input("请选择："))
        if select == 1:
            self.draw()
        else:
            print("请选择使用的算法")
            print("1 -- 动态规划")
            print("2 -- 回溯算法")
            select = int(input("请选择："))
            t = 0
            if select == 1:
                start = time.time()
                self.DP()
                end = time.time()
                t = end - start
            else:
                start = time.time()
                self.Backtracking(-1, 0, self.cubage)
                end = time.time()
                t = end - start
            self.stime = t
            print("能够获得的最大价值为:", self.max_val)
            if self.so_res != []:
                print("使用回溯算法得出最优解经过的项目为:")
                print(self.so_res)
                self.deal_so()
            print("得出最优解的运行时间为：", self.stime, 's')
            self.save()

    def DP(self):  # 动态规划算法
        dp = [[[0 for k in range(self.cubage + 5)] for i in range(4)] for j in range(self.size + 5)]  # 三维dp数组
        for k in range(1, self.size + 1):
            for i in range(1, 4):
                for v in range(self.cubage + 1):
                    for j in range(1, 4):
                        dp[k][i][v] = max(dp[k][i][v], dp[k - 1][j][v])
                        if v >= self.items[k - 1].pack[i - 1].weight:
                            dp[k][i][v] = max(dp[k][i][v],dp[k - 1][j][v - self.items[k - 1].pack[i - 1].weight]+self.items[k - 1].pack[i - 1].profit)
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


if __name__ == '__main__':
    d = int(input('请输入n的大小：'))
    cubage = int(input('请输入c的最大容量：'))
    profit_in = input("请输入价值数据集：")
    weight_in = input("请输入重量数据集：")
    bp = Back_pack(d, cubage, profit_in, weight_in)
    bp.run()
