# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 14:14:28 2020

@author: jimmy
"""

import heapq
from typing import List,Tuple
def minDistance(n: int, edges: List[Tuple[int]], Distance: List[int], start: int) -> List[int]:
    d = [float('Inf')] * n
    d[start] = 0
    adj = [[] for _ in range(n)] #生成邻接表
    for i,e in enumerate(edges):
        adj[e[0]].append([e[1],Distance[i]])
        adj[e[1]].append([e[0],Distance[i]])
    queue = [(0,start)]
    s = set()
    while queue:
        di, index = heapq.heappop(queue) #用优先队列找出最小值
        if index in s:
            continue
        s.add(index)
        for e, dis in adj[index]:
            if e not in s:
                heapq.heappush(queue,(min(di + dis, d[e]), e))
                d[e] = min(di + dis, d[e])
    return d
edges = [(0,1),(0,2),(0,3),(1,2),(1,4),(2,3),(2,4),(2,5),(2,6),(3,6),(4,5),(4,7),(5,6),(5,7),(6,7)]
dis = [2,8,1,6,1,7,4,2,2,9,3,9,4,6,2]
print(minDistance(8,edges,dis,0))
