# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 12:12:10 2020

@author: linziqian
reference: 姜启源《数学建模》
"""

import itertools
from typing import List
import numpy as np

class PowerIndex:
    def __init__(self, quota: int, weight: List[float]):
        self.quota = quota
        self.weight = weight
        
    def Shapley(self, normalization = False):
        '''
        Calculate the Shapley power index. Notice the time complexity may be O(n*n!).
        '''
        l = len(self.weight)
        per_list = itertools.permutations(range(l))
        ans = [0] * l
        for per in per_list:
            s = 0
            for num in per:
                s += self.weight[num]
                if s >= self.quota:
                    ans[num] += 1
                    break
        if normalization:
            tmp = np.array(ans, 'float32')
            tmp /= sum(tmp)
            ans = list(tmp)
        return ans
        
    def isWinningCoalition(self, com):
        '''
        Judge whether the combination is a winning coalition.
        '''
        return sum([self.weight[item] for item in com]) >= self.quota
    
    
    def Banzhaf(self, normalization = False):
        '''
        Calculate the Banzhaf power index. Notice the time complexity may be O(n*2^n).
        '''
        l = len(self.weight)
        com_list = []
        for i in range(1,l+1):
            com_list += list(itertools.combinations(range(l),i))
        com_list_new = filter(self.isWinningCoalition, com_list)
        ans = [0] * l
        for com in com_list_new:
            sum_tmp = sum([self.weight[item] for item in com])
            for num in com:
                if sum_tmp - self.weight[num] < self.quota:
                    ans[num] += 1
        if normalization:
            tmp = np.array(ans,'float32')
            tmp /= np.sum(tmp)
            ans = list(tmp)
        return ans
        
        
if __name__ == '__main__':
    weight = [4,3,2,1]
    quota = 6
    pi = PowerIndex(quota,weight)
    print(pi.Shapley())
    print(pi.Banzhaf())
    
    weight_2  = [2,1,1]
    quota_2 = 3
    pi_2 = PowerIndex(quota_2, weight_2)
    print(pi_2.Shapley())
    print(pi_2.Banzhaf())
    
    '''
    weight_3 = list(itertools.repeat(2,5)) + list(itertools.repeat(1,5))
    quota_3 = 8
    pi_3 = PowerIndex(quota_3, weight_3)
    print(pi_3.Shapley(normalization = True))
    print(pi_3.Banzhaf(normalization = True))
    '''
