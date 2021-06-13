#!/usr/bin/python

#Personal import
from linear_programming_1_2 import *
from utils import *
from graph_function import *

#Lecture du csv en variables global, on peut voir celle-ci comme une constante
nbCity,cityDist,cityPop,cityName = read_csv("villes.csv")

#Variables pour la question 1.2
#Ici on à listK car on fixe les k villes, on lui donne donc l'indices 
#des villes correspondantes.
alpha1 = 0.2
k1 = 3
listk1 = [0,1,2]

#Variables pour la question 2.1
alpha2 = 0.2
k2 = 3

#Variables pour la question 2.2
alpha3 = 0.2
k3 = 5
#Constantes pour la question 3.2
pimax = 500

if __name__ == "__main__":
    rd.seed(None)
    #Exécution du PL pour l'exercice 1.2
    print("----------------")
    print("---- Ex 1.2 ----")
    print("----------------")
    first_pl(nbCity, cityDist, cityPop, alpha1, k1, listk1)
    #Exécution du PL pour l'exercice 2.1
    print("----------------")
    print("---- Ex 2.1 ----")
    print("----------------")
    opt, maxDist = second_pl(nbCity, cityDist, cityPop, alpha2, k2)
    print("Pour k = ",k2,"et alpha = ",alpha2,getCityNames(cityName,opt),maxDist)
    #Exécution du PL pour l'exercice 2.2 et récuperations des indices des 
    print("----------------")
    print("---- Ex 2.2 ----")
    print("----------------")
    opt2 = third_pl(nbCity, cityDist, cityPop, alpha3, k3, cityName)
    
    #Nous récuperons le noms des villes grâce à leur indices
    n = getCityNames(cityName,opt2)
    #Partie 3.1
    #Autre solution optimal pour 332 mais qui est pas renvoyé par notre 
    #algorithme ...
    #opt2 = [5,8,10,13,14]
    
    #Nous commencons par extraire la sous-table des distances correspondant 
    #à la liste de nos villes
    subTable = subTable(opt2,cityDist)
    #Nous definissons nos pi, ici choisi aléatoirement, mais il peuvent 
    #également être défini à la main
    
    #p = generate_random_p(pimax, len(opt2))
    p = generate_random_p_biaised(pimax, len(opt2))
    #p = [20,47,25,3,25]
    #On genere les p de sorties, qui sont sensé être equilibré
    p_equi = calculate_equilibrium_p(p,len(opt2))
    

    
    #Ici on crée les villes de sortie, comme ce sont les memes, nous changeons
    #juste rapidement leur noms
    n_2 = [nv+"2" for nv in n]
    
    #On appelle maintenant la fonction qui nous permet de créer le graph G
    #Sur lequel on pourra appelée l'algorithme max flot min cost
    #Ici on passe les paramèters au graphes, qui sont :
    #Les offreurs, les demandeurs, la table de cout, les différents flow
    #d'entrée et de sortie, donc p et 
    #Notre fonction crée des noeuds S et T bien évidemment, qui ne sont pas
    #dans la liste des villes
    G =  create_bigraph("s","t",n,n_2,p,p_equi,len(opt2),subTable)
    
    #On appelle notre fonction qui permet de calculer le cout minimum pour
    #un flot de valeur maximum
    minCost = max_flot_min_cost(G,"s","t")
    
    #Pour p = [120,25,40,50,40], opt2 = [5,8,10,13,14] on obtient 41315
    # après vérifications à la main
    print("----------------")
    print("---- Ex3.1 -----")
    print("----------------")    
    print("Villes obtenues à la 2.2 pour k = 5, alpha = 0.2 : ",getCityNames(cityName,opt2))
    print("Assignations des patients au départ :",p)
    print("Assignations des patients souhaitées :",p_equi)
    print("Cout minimal pour la redistribution :",minCost)