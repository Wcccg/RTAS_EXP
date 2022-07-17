from ds import *
from model import *
import random


if __name__ == '__main__':
    taskSet = []
    m = Model('M')
    f = open("taskSet.txt","w")
    # for i in range(0, 3):
    #     temp = Task()
    #     temp.period = random.randint(2, 3)
    #     temp.C = random.randint(1, temp.period-1)
    #     taskSet.append(temp)
    temp1 = Task()
    temp1.period = 3
    temp1.C = 2
    taskSet.append(temp1)
    temp2 = Task()
    temp2.period = 2
    temp2.C = 1
    taskSet.append(temp2)
    temp3 = Task()
    temp3.period = 2
    temp3.C = 1
    taskSet.append(temp3)
    HP = int(getHP(taskSet))
    print('HP = ', HP, file = f)
    for i in range(3):
        taskSet[i].worksNum = int(HP/taskSet[i].period)
    i = 0
    for temp in taskSet:
        i += 1
        print('-----------------', file = f)
        print('task', i, ':', file = f)
        print('period = ', temp.period, file = f)
        print('C = ', temp.C, file = f)
        print('worksNum = ', temp.worksNum, file = f)
    f.close()
    X = setX(m, taskSet)
    E = [[1, 2], [1, 3], [2, 3]]
    sensorTask = [1, 2]
    controlTask = [3]
    B = setB(m, E)
    m = setObj(m, X, HP, taskSet)
    m = addCon1(m, X)
    m = addCon2(m, X, B, E, taskSet, 0.5, HP)
    for i in sensorTask:
        for j in controlTask:
            S = Floyd_S(3, E, i, j)
            L = Floyd_L(3, E, i, j)
            m = addCon3(m, L, B, HP)
            m = addCon4(m, S, B, HP)
    m.write('model.lp')
    m.optimize()
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))
    # 透過屬性objVal顯示最佳解
    print('Obj: %g' % m.objVal)
