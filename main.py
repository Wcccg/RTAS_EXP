# 该模块使用其他模块定义的函数进行求解
from readFile import *
from model import *
import random


if __name__ == '__main__':
    alpha = 0.5                                                                     # 超参数 alpha，自行设置
    m = Model('M')                                                                  # 新建求解器模型
    taskNum, taskSet, sensorTask, controlTask, E, HP = readDAG("DAG.txt")           # 读文件、计算基础参数
    saveTaskSet(HP, taskSet,"taskSet.txt")                                          # 写文件，主要是看 HP、period、worksNum
    X = setX(m, taskSet)                                                            # 新建求解器布尔型变量组 X[]               
    B = setB(m, E)                                                                  # 新建求解器浮点型变量组 B[] 
    m = addCon(m, X, B, E, taskSet, alpha, HP, sensorTask, controlTask, taskNum)    # 添加约束一、二、三、四
    m.setParam('OutputFlag',0)                                                      # 省略求解过程
    m.optimize()                                                                    # 求解
    m.write('model.lp')                                                             # 将模型输出到 model.lp 中
    saveSolution(m, "solution.txt")                                                 # 将解输出到 solution.txt 中
