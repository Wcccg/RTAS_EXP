# 该模块用于计算求解器所需参数
from ds import *
import random

# 计算最大公约数，用于 lcm
def gcd(a, b):
    while a:
        a, b = b%a, a
    return b

# 计算最小公倍数，用于 HP
def lcm(a, b):
    return a*b/gcd(a, b)

# 计算超周期 HP，它等于所有任务周期的最小公倍数
def getHP(taskSet):
    HP = taskSet[0].period
    for task in taskSet:
        HP = lcm(HP, task.period)
    return HP

# 计算每个任务在超周期内释放作业数
def getWorksNum(HP, taskSet):
    for task in taskSet:
        task.worksNum = HP/task.period
    return taskSet

# 给定策略编号 X，计算剩余作业数 M，即统计 X 的二进制序列中中 1 的个数
def getM(X):
    M = 0
    while X:
        X = X & (X-1)
        M += 1
    return M

# 计算使用策略 X 时，剩余作业的编号，即统计 X 的二进制序列中中 1 的位置
def getWorks(X, WorksNum):
    Works = []
    for i in range(WorksNum+1):
        if X == (X | 2**(WorksNum-i)):
            Works.append(i)
    return Works

# 计算剩余作业的释放时间 R，R = (作业编号 - 1) * 释放周期
def getR(Works, p):
    R = []
    for i in Works:
        R.append((i-1)*p)
    return R

# 计算作业相对截止期 RD，RD = C + (相邻任务释放间隔 - C) * alpha
def getRD(R, C, alpha, HP):
    D = []
    L = len(R)-1
    for i in range(L):
        D.append(C+(R[i+1]-R[i]-C)*alpha)
    D.append(C+(HP-R[L]-C)*alpha)
    return D

# 计算作业绝对截止期 AD，AD = R + RD
def getAD(R, C, alpha, HP):
    D = []
    L = len(R)-1
    for i in range(L):
        D.append(R[i]+C+(R[i+1]-R[i]-C)*alpha)
    D.append(R[L]+C+(HP-R[L]-C)*alpha)
    return D

# Floyd 算法求最短路，n 为节点数，E 为边集
def Floyd_S(n, E, start, end):
    Vtx = []
    S_way = []
    for i in range(n):
        temp1 = []
        temp2 = []
        for j in range(n):
            if [i+1, j+1] in E:
                temp1.append(1)
                temp2.append([i, j])
            else:
                temp1.append(99999)
                temp2.append([])
        Vtx.append(temp1)
        S_way.append(temp2)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if Vtx[i][j] > Vtx[i][k]+Vtx[k][j]:
                    Vtx[i][j] = Vtx[i][k]+Vtx[k][j]
                    S_way[i][j] = S_way[i][k] + S_way[k][j][1:]
    S = S_way[start-1][end-1]
    for i in range(len(S)):
        S[i] += 1
    return S

# Floyd 算法求最长路，n 为节点数，E 为边集
def Floyd_L(n, E, start, end):
    Vtx = []
    L_way = []
    for i in range(n):
        temp1 = []
        temp2 = []
        for j in range(n):
            if [i+1, j+1] in E:
                temp1.append(1)
                temp2.append([i, j])
            else:
                temp1.append(-99999)
                temp2.append([])
        Vtx.append(temp1)
        L_way.append(temp2)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if Vtx[i][j] < Vtx[i][k]+Vtx[k][j]:
                    Vtx[i][j] = Vtx[i][k]+Vtx[k][j]
                    L_way[i][j] = L_way[i][k] + L_way[k][j][1:]
    L = L_way[start-1][end-1]
    for i in range(len(L)):
        L[i] += 1
    return L