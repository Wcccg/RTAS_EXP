# 该模块使用其他模块定义的函数进行求解
from readFile import *
from model import *
import random


if __name__ == '__main__':
    m = Model('M')
    taskNum, taskSet, sensorTask, controlTask, E, HP = readDAG("DAG.txt")
    saveTaskSet(HP, taskSet,"taskSet.txt")
    X = setX(m, taskSet)
    B = setB(m, E)
    m = setObj(m, X, HP, taskSet)
    m = addCon1(m, X)
    m = addCon2(m, X, B, E, taskSet, 0.5, HP)
    for i in sensorTask:
        for j in controlTask:
            S = Floyd_S(taskNum, E, i, j)
            L = Floyd_L(taskNum, E, i, j)
            m = addCon3(m, L, B, HP)
            m = addCon4(m, S, B, HP)
    m.optimize()
    m.write('model.lp')
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))
    # 透過屬性objVal顯示最佳解
    print('Obj: %g' % m.objVal)
