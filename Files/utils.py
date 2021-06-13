# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 01:33:23 2020

@author: liece
"""
import sys
import csv
import random as rd


def getCityNames(cityNames,indexList):
    """
    Retourne le noms des villes pour les indexes données en paramètres
    """
    return [cityNames[x] for x in indexList]

def subTable(indexList,cityDist):
    """
    Permet d'extraire la sous-table des distances pour les indexes données
    en paramètres
    """
    #indexList*indexList liste
    subTable = [[0 for x in range(len(indexList))] for y in range(len(indexList))]
    #extrait la sous table des distances pour la 2.2
    for i,x in enumerate(indexList):
        for j,y in enumerate(indexList):
            subTable[i][j] = cityDist[x][y]
    return subTable

def generate_random_p(pimax, size):
    """
    Génere aléatoirement des p de façon equilibré,
    un pi ne pourra jamais dépasser pimax/size!
    On aurait pu faire d'une autre manière mais c'est suffisant pour faire nos
    tests
    """
    return [rd.randint(0,int(pimax/size)) for _ in (range(size))]

def generate_random_p_biaised(pimax, size):
    """
    Pareil mais qui a beaucoup plus de chance de genrer des composants > 100
    """
    p = [0]*size
    for x in range(size):
        p[x] = rd.randrange(0,int(pimax-sum(p)))
    return p

def calculate_equilibrium_p(p,size):
    """
    Permet de calculé un p à l'équilibre, on se sert du reste dans le cas ou 
    la division sum(p)/size ne renvoie pas un nombre entier, on essaye alors 
    d'équilibrer au mieux.
    """
    #supposed equilibrium
    p_equi = sum(p)//size
    rest = sum(p)%size
    p_equi_arr = [p_equi]*size
    for x in range(rest):
        p_equi_arr[x]+=1
    return p_equi_arr


    
#Permet de lire un fichier csv d'un format équivalent à celui donné
#On peut changer le delimiter pour acceuilir un nouveau format
def read_csv(filename):
    """
    Lit le fichier csv dans le format donnée dans le sujet et nous renvoie
    le noms des villes, le nombre de ville, la population de chaque ville et
    la distance entre chacune d'elle'
    """
    size = 0
    with open(filename) as csv_file:
        i = -1
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if i == -1:
                nbCity = len(row)-2
                cityDist = [[0 for x in range(nbCity)] for y in range(nbCity)]
                cityPop = [0]*nbCity
                cityName = row[2:]
                i = 0
            else:
                cityPop[i] = int(row[0])
                for x in range(0,i+1):
                    cityDist[i][x] = int(row[x+2])
                    cityDist[x][i] = int(row[x+2])
                i+=1
    return nbCity,cityDist,cityPop,cityName
