# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 16:00:19 2020
"""

'''
This code is mainly for seat allocation. 
Reference: 姜启源《数学建模》
'''

from typing import List
import heapq

import numpy as np

class SeatAllocation:
    def __init__(self, p: List[int], n:int):
        '''
        p 为人数向量
        n 为待分配的席位总数
        '''
        self.person = p
        self.num = n
    
    def Q_Value_Method(self) -> List[int]:
        '''
        Q值法分配席位
        '''
        m = len(self.person)
        if self.num < m:
            print("席位过少，该方法不适用")
            return 
        n = [1] * m # n为分配方式的向量
        
        def calculate_Q(i):
            return self.person[i] ** 2 / (n[i] * (n[i] + 1) )
        
        tmp = []
        for index in range(m):
            heapq.heappush(tmp,(-calculate_Q(index),index))
        for i in range(self.num - m):
            Q, index = heapq.heappop(tmp)
            n[index] += 1
            heapq.heappush(tmp,(-calculate_Q(index),index))
        return n
    
    def Greatest_Remainders(self) -> List[int]:
        '''
        最大剩余法分配席位
        会导致席位悖论和人口悖论
        '''
        s = sum(self.person)
        p = np.array(self.person)
        n = np.floor(p * self.num / s) #按比例分配的席位
        if self.num - np.sum(n) == 0.:
            return list(n)
        
        import heapq
        m = int(self.num - np.sum(n)) #剩下的席位
        r = list(p * self.num / s - n) # 小数点后的结果
        l = []
        n = list(n.astype(int))
        for index,value in enumerate(r):
            heapq.heappush(l,(-value,index))
        for i in range(m):
            v, index = heapq.heappop(l)
            n[index] += 1
        return n
    
    def Largest_Fractions(self) -> List[int]:
        '''
        最大分数法，方法同最大剩余法
        '''
        return self.Greatest_Remainders()
    
    def Hungtington(self, method = 'EP') -> List[int]:
        '''
        Huntington除数法
        GD:最大除数法
        MF:主要分数法
        EP:相等比例法
        HM:调和平均法
        SD:最小除数法
        '''
        if method not in {'GD','MF','EP','HM','SD'}:
            print('The Method Doesn\'t Exist')
            return 
        if method == 'EP':
            return self.Q_Value_Method()
        import heapq
        m = len(self.person)
        if self.num < m:
            print("席位过少，该方法不适用")
            return 
        n = [1] * m 
        
        def calculate_priority(i,method = method):
            if method == 'GD':
                return self.person[i] / (n[i] + 1)
            elif method == 'MF':
                return self.person[i] / (n[i] + 0.5)
            elif method == 'HM':
                return self.person[i] / (2 * n[i] * (n[i] + 1) / (2 * n[i] + 1))
            elif method == 'SD':
                return self.person[i] / n[i]
        tmp = []
        for index in range(m):
            heapq.heappush(tmp,(-calculate_priority(index),index))
        for i in range(self.num - m):
            Q, index = heapq.heappop(tmp)
            n[index] += 1
            heapq.heappush(tmp,(-calculate_priority(index),index))
        return n
    

if __name__ == '__main__':
    example = SeatAllocation([9061,7179,5259,3319,1182],26)
    example_2 = SeatAllocation([91490, 1660, 1460, 1450, 1440, 1400, 1100], 100)
    # print(example.Q_Value_Method())
    l = ['GD', 'MF', 'EP', 'HM', 'SD']
    for item in l:
        print(example.Hungtington(method = item))
    for item in l:
        print(example_2.Hungtington(method = item))
    print(example_2.Greatest_Remainders())
    example_3 = SeatAllocation([100,60,40], 21)
    print(example_3.Q_Value_Method())
