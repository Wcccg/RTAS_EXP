from random import random
class Task:                     # 一个Task()实体表示一个任务
    def __init__(self):
        self.exeTime = 0
        self.worksNum = 0
        self.period = 0
        self.pre = []
        self.nxt = []
        self.M = 0
        self.C = 0
