#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 10:35:35 2020
@author: morten
"""

#alt med x er kemisk skift og er givet i ppm, beta er lorentz forbredningsfaktor også i ppm
#Implementering af lineshapefunktionerne fra russerartiklen: doi:10.1016/j.ssnmr.2005.10.009
import cmath 
import matplotlib.pyplot as plt
import numpy as np; import scipy as sp
import scipy.optimize as so
import copy
import time

#Jeg skal have ændret den næste, så jeg får lavet arrays.
def LoadFileData(Filename):
    """
    Filnavnet skal være en string med filtype indikeret eks. test.txt
    Filen skal have punktum som decimal separator, størrelsesorden kan godt
    betegnes som eks. 1.2e+002 som 120
    Returner 1D numpy arrays på formen (x,)
    """
    x = []
    y = []
    File = open(Filename)
    for Line in File:
        LineData = Line.split(",")
        x.append(float(LineData[3].replace("\n","")))
        y.append(float(LineData[1]))
    
    #Hver linje kommer ud som en string som skal splittes, og
    #hver linje slutter åbenbart med \n (nok ikke, men sætter det på for en sikkerheds skyld,
    #da linjen slutter med x-værdien)
    File.close()
    x_array = np.array(x);y_array = np.array(y)
    return x_array,y_array

def FindIndices(x,a,b):
    """
    Vi har vores indices i lister/1D numpy arrays, som skal slices, hvis vi vil integrere over et mindre område.
    a og b skal være de float værdier hvor vi vil starte og slutte. Desuden a < b
    x skal være vores liste/1D numpy array af x-værdier, som er arrangeret i stigende rækkefølge 
    Returner k og l som er index-værdierne, som kan bruges til at slice.
    """
    c = x[0]
    Count = 0
    #Først finder jeg a, og så bruger jeg den til at finde b
    while True:
        if abs(c-a) <= abs(x[Count+1]-a):
            break #Tjek om vi er i mål
        else:
            c = x[Count+1]
            Count += 1
    d = c #Laver det samme for d, men nu starter jeg bare ved den fundne c.
    k = copy.deepcopy(Count)
    while True:
        if abs(d-b) <= abs(x[Count+1]-b):
            break #Tjek om vi er i mål
        else:
            d = x[Count+1]
            Count += 1
    l = copy.deepcopy(Count)
    return k,l


i = 1j
def B_evaluation(x,x_i,x_delta,beta):
    """
    B fra Arsenievs lineshape funktion, evalueres seperat af hensyn til læsbarheden.
    """
    B = -x+(x_i-x_delta/3)-i*beta
    return B

def LineshapeFunction(x,r,x_delta,x_i,beta,a):
    """
    Implementering af Arsenievs lineshape funktion i det generelle tilfælde,
    og i tilfældet A = 0
    x er et 1D numpy array på formen (x,)
    r er c/a værdien og er en float.
    x_delta er delta sigma i form af en float.
    x_i er sigma_i i form af en float.
    a er en skaleringskonstant i form af en float.
    """
    
    A = complex((r**2)-1)
    if A == 0: #Det ene af de to "edgecases"
        C = x_delta
        B = B_evaluation(x,x_i,x_delta,beta)
        S = -2*i/(cmath.pi*C)*np.sqrt(C/B)*np.arctan(np.sqrt(C/B))
    else:
        C = x_delta
        B = B_evaluation(x,x_i,x_delta,beta)
        S = a*(2*i/cmath.pi)*(A/(C-A*B))*(1+(2*C/(C-A*B))*(np.sqrt(A)*np.arctan(np.sqrt(A))-np.sqrt(C/B)*np.arctan(np.sqrt(C/B)))/(np.sqrt(A)*np.arctan(np.sqrt(A))+A/(1+A)))
    return S.real

def LineshapeFunctionInfinite(x,x_delta,x_i,beta,a):
    """
    Arsenievs lineshape funktion i tilfældet af r->infinity
    """
    B = B_evaluation(x,x_i,x_delta,beta)
    S = -2*i/(cmath.pi*B)*a
    return S.real

def FitExperimental(x,y,y_uncertainty = None):
    """
    Antager at x og y er 1D numpy arrays som har formen (x,)
    Kan også tage et 1D numpy array, som beskriver usikkerheden i y-værdierne,
    defaulter til at være None, og så får man statistiske usikkerheder, hvis egentlige
    usikkerheder kan findes så skal AbsoluteSigma nok sættes til True, men tjek dokumentationen først.
    Returner en tuple bestående af:
    Et array af parameterne for den fittede model som [r,x_delta,x_i,beta]
    Et array af arrays som giver 2D arrays som bestemmer covariansen for alle parameterne
    (For yderligere info, se dokumentation for scipy_curve_fit)
    """
    #Hvis vi antager at den ikke bliver oblat (r < 1), så kan vi ændre bounds og
    #startparametere til 1 og 1
    
    LowerBounds = np.array([1,-np.inf,-np.inf,-np.inf,0])
    UpperBounds = np.array([np.inf,np.inf,np.inf,np.inf,np.inf])
    Bounds = (LowerBounds,UpperBounds)
    InitialParameters = np.array([1,1,1,1,1]) #Vi kan ikke starte ved r = 0, da sqrt(-1)=i og arctan(i) er ikke defineret.
    return so.curve_fit(LineshapeFunction,x,y,InitialParameters,y_uncertainty,False,True,Bounds)


def EdgecaseFunctions(x,c1,x_delta,x_i,beta,a):
    """
    Tager x som et array
    Giver os en passende linearkombination af numpy arrays af y-værdierne af en simuleret 
    ikke-orienteret vesikel og af en fuldt orienteret vesikel, 
    funktionerne for dette er givet i russerartiklen.
    """
    c2 = 1-c1
    NonOrientedY = (LineshapeFunction(x,1, x_delta, x_i, beta,a))
    FullyOrientedY = (LineshapeFunctionInfinite(x, x_delta, x_i, beta,a))
    return c1*NonOrientedY+c2*FullyOrientedY

def PercentageOrientation(x,y,x_delta,x_i,beta,a):
    """
    Implementering af Pidgeons definition af %-orientering
    x og y er de passende værdier for den model vi har fittet.
    Returner c2, konstanten som bestemmer procentdel orientering
    """
    #Virker sgu kke særlig godt for at være ærlig, er lidt RNG'agtig
    #så lad være med at bruge den, alle henvisninger til den i de andre funktioner
    #er også udkommenteret.
    LowerBounds = np.array([0,x_delta-(1e-10),x_i-(1e-10),beta-(1e-10),a-(1e-10)])
    UpperBounds = np.array([1,x_delta+(1e-10),x_i+(1e-10),beta+(1e-10),a+(1e-10)])
    Bounds = (LowerBounds,UpperBounds)
    InitialParameters = np.array([1,x_delta,x_i,beta,a]) 
    Fit = so.curve_fit(EdgecaseFunctions,x,y,InitialParameters,None,False,True,Bounds)
    return 1-Fit[0][0]

def FitAndPlotExperimental(x,y,LowerLimit,UpperLimit):
    """
    Filename gives som en string, det skal have det fulde filnavn
    Lower og upper limit skal gives som en float
    """
    x = np.flip(x,0)
    y = np.flip(y,0)
    (a,b) = FindIndices(x,LowerLimit,UpperLimit)
    xFit = x[a:b]
    yFit = y[a:b]
    FitExp = FitExperimental(xFit,yFit)
    Parameters = FitExp[0]
    Uncertainty = np.sqrt(np.diag(FitExp[1]))#Usikkerhedsparametere, beregnet ifølge scipy.optimize.curve_fit's dokumentation
    ModelY = LineshapeFunction(x, Parameters[0], Parameters[1], Parameters[2], Parameters[3], Parameters[4])
    #Percent = 100*PercentageOrientation(x, ModelY, Parameters[1], Parameters[2], Parameters[3], Parameters[4])
    plt.plot(x,y,'b',label = "Eksperimental Data")
    plt.plot(x,ModelY,'r--', label = "Fitted Model")
    plt.legend();plt.xlim(50,-50);plt.xlabel("ppm");plt.ylabel("Intensitet")
    print("Parameters:", Parameters)
    print("Uncertainties:", Uncertainty)
    #print("%-orientation:", Percent)    
    return None

def FitSeveral(LowerLimit, UpperLimit, Filenames):
    """
    Files er en liste af filnavne, som skal kombineres og fittes samlet.
    Denne funktion kombinerer og normerer y-værdierne for at gøre fitningen lettere,
    Den caller så FitAndPlotExperimental med de samlede y-værdier, finder desuden også
    run-time fra start til slut.
    Den kan ikke altid finde det rigtige minimum, så man skal nogen gange ændre InitialParameters
    og justere bounds. Default er at alle parametre starter ved 1 og at den generelt er unbounded
    pånær at den antager r>1 (kan sagtens ændres i bounds)
    """
    start = time.time()
    (x,y) = LoadFileData(Filenames[0])
    y = y/np.max(y)
    k = 1
    while k < len(Filenames):
        yTemp = LoadFileData(Filenames[k])[1]
        yTemp = yTemp/np.max(yTemp)
        y = y + yTemp
        k += 1
    y = y/len(Filenames)
    FitAndPlotExperimental(x,y,LowerLimit,UpperLimit)
    end = time.time()
    print("Time to run:", end-start, "seconds")


    