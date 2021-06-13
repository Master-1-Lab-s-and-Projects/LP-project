# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 00:46:40 2020

@author: liece
"""
from gurobipy import *
from utils import *

def first_pl(nbCity,cityDist,cityPop,alpha,k,listK):
    """
    Programme linéaire pour la question 1.2 du sujet
    """
    const = ((1+alpha)/k)*sum(cityPop)
    m = Model("EX1.1") 
    vars = m.addVars(nbCity,k,vtype=GRB.BINARY, name='xij')
    for j in range(len(listK)):
        m.addConstr(sum(vars[i,j]*cityPop[i] for i in range(nbCity)) <= const)
    for i in range(nbCity):
        m.addConstr(sum(vars[i,j] for j in range(len(listK))) == 1)
    obj = LinExpr();
    for i in range(nbCity):
        for j in range(len(listK)):
            obj+= (cityPop[i]*vars[i,j]*cityDist[i][listK[j]])/sum(cityPop)
    m.setObjective(obj,GRB.MINIMIZE)
    m.optimize()


def second_pl(nbCity,cityDist,cityPop,alpha,k):
    """
    Programme linéaire pour la question 2.1 du sujet
    """
    const = ((1+alpha)/k)*sum(cityPop)
    m = Model("EX2.1") 
    vars = m.addVars(nbCity,nbCity,vtype=GRB.BINARY, name='xij')
    vars2 = m.addVars(nbCity,vtype=GRB.BINARY,name='yj')
    for j in range(nbCity):
        m.addConstr(sum(vars[i,j]*cityPop[i] for i in range(nbCity)) <= const)
    for i in range(nbCity):
        m.addConstr(sum(vars[i,j] for j in range(nbCity)) == 1)
    for j in range(nbCity):
        m.addConstr(sum(vars[i,j] for i in range(nbCity)) <= vars2[j]*nbCity)
    m.addConstr(sum(vars2[j] for j in range(nbCity)) <= k)
    obj = LinExpr();
    for i in range(nbCity):
        for j in range(nbCity):
            obj+= (cityPop[i]*vars[i,j]*cityDist[i][j])/sum(cityPop)
    m.setObjective(obj,GRB.MINIMIZE)
    m.optimize()
    
    #retourner les indices des villes pour la suite du projet
    solution = m.getAttr('X', vars2)
    solOpt = [0]*k
    i = 0
    for x in range(nbCity):
        if i == k:
            break;
        if solution[x] == 1:
            solOpt[i] = x
            i+=1
    solution2 = m.getAttr('X',vars)
    solOpt2 = [0]
    for i in range(nbCity):
        for j in range(nbCity):
            if(solution2[i,j] == 1):
                solOpt2.append(cityDist[i][j])
    return solOpt,max(solOpt2)

def third_pl(nbCity,cityDist,cityPop,alpha,k,cityName):
    """
    Programme linéaire pour la question 2.2 du sujet
    """
    const = ((1+alpha)/k)*sum(cityPop)
    m = Model("EX2.2") 
    #obj var
    mdvar = m.addVar(lb=0.0, obj=1.0,vtype = GRB.INTEGER, name="maxDistvar")   
    #old variables
    vars = m.addVars(nbCity,nbCity,vtype=GRB.BINARY, name='xij')
    vars2 = m.addVars(nbCity,vtype=GRB.BINARY,name='yj')
    
    m.update()
    #addminmax constraint
    for i in range(nbCity):
            m.addConstr(sum(vars[i,j]*cityDist[i][j] for j in range(nbCity)) <= mdvar)
    #old constraints
    for j in range(nbCity):
        m.addConstr(sum(vars[i,j]*cityPop[i] for i in range(nbCity)) <= const)
    for i in range(nbCity):
        m.addConstr(sum(vars[i,j] for j in range(nbCity)) == 1)
    for j in range(nbCity):
        m.addConstr(sum(vars[i,j] for i in range(nbCity)) <= vars2[j]*nbCity)
    m.addConstr(sum(vars2[j] for j in range(nbCity)) <= k)
    m.addConstr(sum(vars2[j] for j in range(nbCity)) >= k)
    #m.setParam(GRB.Param.PoolSolutions, 50)
    #m.setParam(GRB.Param.PoolSearchMode, 1)
    m.optimize()
    # Print number of solutions stored
    #nSolutions = m.SolCount
    #print('Number of solutions found: ' + str(nSolutions))
    """
    # print fourth best set if available
    for x in range(nSolutions):
        m.setParam(GRB.Param.SolutionNumber, x)

        solDec = []

        for e in range(nbCity):
            if vars2[e].Xn > .9:
                solDec+=[e]
        print(getCityNames(cityName,solDec))"""
    #retourner les indices des villes pour la suite du projet
    solution = m.getAttr('X', vars2)
    solOpt = [0]*k
    i = 0
    for x in range(nbCity):
        if i == k:
            break;
        if solution[x] == 1:
            solOpt[i] = x
            i+=1
    return solOpt