# 该模块用于求解器初始化
from gurobipy import *
from getParameter import *

# 变量生成，X[]是二维列表，X_i_j 的值表示示第 i 个任务的第 j 种策略被选中
def setX(m, taskSet):
    X = []
    ind = 0
    for task in taskSet:
        temp = []
        ind += 1
        for i in range(2**task.worksNum-1):
            name = 'X_'+str(ind)+'_'+str(i+1)
            temp.append(m.addVar(vtype=GRB.BINARY, name = name))
        X.append(temp)
    m.update()
    return X

# 变量生成，B 是哈希表（字典）
def setB(m, E):
    B = {}
    for i, j in E:
        i = int(i)
        j = int(j)
        name = str(i)+'_'+str(j)
        temp = m.addVar(vtype=GRB.CONTINUOUS, name = 'B_'+name)
        B[name] = temp
    m.update()
    return B
        

# 设置目标函数
def setObj(m, X, HP, taskSet):
    obj = 0
    ind = 0
    for x_i in X:
        for j in range(len(x_i)):
            obj += getM(j+1)*taskSet[ind].C*x_i[j]
    obj /= HP
    ind += 1
    m.setObjective(obj, GRB.MAXIMIZE)
    m.update()
    return m    

# 添加约束一，每个任务有且只有一种剔除策略被选中
def addCon1(m, X):
    ind = 0
    for x_i in X:
        con = 0
        ind += 1
        for x_i_j in x_i:
            con += x_i_j
        name = 'C_1_'+str(ind)
        m.addConstr(con == 1, name)
    m.update()
    return m

# 添加约束二
def addCon2(m, X, B, E, taskSet, alpha, HP):
    I = 10000000
    for i, j in E:
        i = int(i)
        j = int(j)
        n_i = taskSet[i-1].worksNum     # n_i、n_j 代表任务 i 和任务 j 在超周期内释放作业数
        n_j = taskSet[j-1].worksNum
        for a in range(1, 2**n_i):    # a、b 代表任务 i、j 当前使用策略 X_i_a、X_j_b
            for b in range(1, 2**n_j):
                works_i = getWorks(a, n_i)
                works_j = getWorks(b, n_j)
                r_j = getR(works_j, taskSet[j-1].period)
                r_i = getR(works_i, taskSet[i-1].period)
                d_i = getAD(r_i, taskSet[i-1].C, alpha, HP)
                d_i.append(d_i[0]+HP)
                ind = 0
                Len = len(r_j)
                while r_j[ind] < d_i[0] and ind < Len:
                    r_j.append(r_j[ind]+HP)
                    ind += 1
                for x in range(len(d_i)-1):           # x, y 从 i、j 未被排除的作业中依次选取
                    for y in range(len(r_j)):       # 故满足 Y_i_x = Y_j_y = 1
                        if (d_i[x] <= r_j[y]) and (d_i[x+1] > r_j[y]):
                            # 满足上面这些条件就可以添加约束二了
                            B_i_j = B[str(i)+'_'+str(j)]
                            con = r_j[y]-r_i[x]+I*(X[i-1][a-1]-1)+I*(X[j-1][b-1]-1)
                            name = 'C_2_('+str(i)+'-'+str(a)+'-'+str(works_i[x%len(works_i)])+')_('+str(j)+'-'+str(b)+'-'+str(works_j[y%len(works_j)])+')'
                            m.addConstr(con <= B_i_j, name)     # 编号规则：(任务号-调度方案号-释放作业号)
    m.update()
    return m

# 添加约束三，最长路约束
def addCon3(m, P, B, HP):
    con = 0
    for k in range(len(P)-1):
        i = int(P[k])
        j = int(P[k+1])
        B_i_j = B[str(i)+'_'+str(j)]
        con += B_i_j
    B_s_c = HP*(len(P)-1)
    name = 'C_3_('+str(P[0])+','+str(P[-1])+')'
    m.addConstr(con <= B_s_c, name)
    return m

# 添加约束四，最短路约束
def addCon4(m, P, B, HP):
    con = 0
    for k in range(len(P)-1):
        i = int(P[k])
        j = int(P[k+1])
        B_i_j = B[str(i)+'_'+str(j)]
        con += B_i_j
    B_s_c = HP*(len(P)-1)
    name = 'C_4_('+str(P[0])+','+str(P[-1])+')'
    m.addConstr(con <= B_s_c, name)
    return m