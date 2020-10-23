# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:42:44 2020

MDP problem
@author: fishy
"""
import matplotlib.pyplot as plt
import numpy as np

class MDP(object):
    def __init__(self,Xmax,Vmax):
        self.Xmax = Xmax
        self.Vmax = Vmax

        
    def startState(self):
        return [self.X0,self.V0]
    
    def isEdge(self,state):
        return (((state[0]+state[1])>self.Xmax )or((state[0]+state[1])<-self.Xmax))
    
    def isEnd(self,state):
        return state == [0,0]
    
    def actions(self,state):
        # return list of valid actions
        results = []
        if (self.isEdge(state) or self.isEnd(state)):
            results.append('none')
        else:
            results.append('Do_nothing')
            if state[1]+1 <= self.Vmax:
                results.append('accelerating')
            if state[1]-1 >= -self.Vmax:
                results.append('decelerating')
            
        return results
    
    def TransProbAndReward(self,state,action):
        results = []
        next_state = []
        if action == 'Do_nothing':
            next_state = [state[0]+state[1],state[1]]
        elif action == 'accelerating':
            next_state = [state[0]+state[1],state[1]+1]
        elif action == 'decelerating':
            next_state = [state[0]+state[1],state[1]-1]
        results.append((next_state, 1,int(self.isEnd(next_state))))
        return results
    
    
    def discount(self):
        return 0.9
    def states(self):
        results = []
        for i in range(-self.Xmax, self.Xmax+1):
            for j in range(-self.Vmax, self.Vmax+1):
                results.append([i,j])
        return results


def  valueIteration(mdp):
    V = {}
    for state in mdp.states():
        V[tuple(state)] = 0.
        
    def Q(state,action):
        return sum(prob* (reward + mdp.discount()*V[tuple(newstate)]) \
                   for newstate, prob, reward in mdp.TransProbAndReward(state,action))
    while True:
        newV = {}
        for state in mdp.states():
            if (mdp.isEnd(state) or mdp.isEdge(state)):
                newV[tuple(state)] = 0.
            else:
                newV[tuple(state)] = max(Q(state,action) for action in mdp.actions(state))
        if max(abs(V[tuple(state)]-newV[tuple(state)])\
               for state in mdp.states() ) < 1e-8:
            break
        V = newV
    
        pi = {}
        for state in mdp.states():
            if (mdp.isEnd(state) or mdp.isEdge(state)):
                pi[tuple(state)] = 'none'
            else:
                pi[tuple(state)] = max((Q(state,action),action) for action in mdp.actions(state)) [1]
    
        print('{:20} {:20}| {:15} '.format('s','V(s)','pi(s)'))
        for state in mdp.states():
            print('{} {:>20} {:>20} '.format(state,V[tuple(state)],pi[tuple(state)]))
        
        
    optimalValue = []
    optimalPolicy = []
    rows = []
    columns = []
    for state in mdp.states():
            optimalValue.append(str(V[tuple(state)]))
            optimalPolicy.append(str(pi[tuple(state)]))
    cell_text_value = np.array(optimalValue).reshape((2*mdp.Vmax+1,2*mdp.Xmax+1))
    cell_text_policy = np.array(optimalPolicy).reshape((2*mdp.Vmax+1,2*mdp.Xmax+1))
    print (cell_text_value)
    print (cell_text_policy)
    for i in range(-mdp.Xmax, mdp.Xmax+1):
        columns.append(str(i))
        
    for i in range(-mdp.Vmax, mdp.Vmax+1):
        rows.append(str(i)) 
    print (columns)
    print (rows)
    plt.table(cellText = cell_text_value, rowLabels=(rows), colLabels=(columns))           
mdp = MDP(4,2)
valueIteration(mdp)


