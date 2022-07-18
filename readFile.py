# 该模块用于定义数据结构以及读文件并计算初始参数
from getParameter import *


class Task:                     # 一个Task()实体表示一个任务
    def __init__(self):
        self.worksNum = 0       # 剔除前超周期内释放作业数
        self.period = 0         # 释放作业周期
        self.pre = []           # 前驱节点
        self.nxt = []           # 后继节点
        self.C = 0              # 作业执行时间
        self.plotform = 0       # 任务所在平台


def readDAG(filename):
    taskNum = 0
    taskSet = []
    sensorTask = []
    controlTask = []
    E = []
    with open(filename, 'r') as f:
        taskNum = int(f.readline())
        while True:
            line = f.readline()
            if not line:
                break
            line = line.split()
            temp = Task()
            temp.C = int(line[1])
            temp.period = int(line[2])
            pre = line[3][1:-2].split(',')
            for i in pre:
                temp.pre.append(int(i))
            nxt = line[4][1:-2].split(',')
            for i in nxt:
                temp.nxt.append(int(i))
            temp.plotform = int(line[7])
            taskSet.append(temp)
            start = int(line[0])
            end = line[4][1:-2]
            end = end.split(',')
            for i in end:
                i = int(i)
                if i == -1:
                    break
                E.append([start, i])
            if line[5] == '1':
                sensorTask.append(int(line[0]))
            if line[6] == '1':
                controlTask.append(int(line[0]))
    HP = int(getHP(taskSet))
    for task in taskSet:
        task.worksNum = int(HP/task.period)
    return taskNum, taskSet, sensorTask, controlTask, E, HP

# 将 taskSet 参数写入 taskSet.txt
def saveTaskSet(HP, taskSet, filename):
    f = open(filename,"w")
    i = 0
    print('HP = ', HP, file = f)
    for temp in taskSet:
        i += 1
        print('-----------------', file = f)
        print('task', i, ':', file = f)
        print('period = ', temp.period, file = f)
        print('C = ', temp.C, file = f)
        print('worksNum = ', temp.worksNum, file = f)
    f.close()
    return

readDAG("DAG.txt")
