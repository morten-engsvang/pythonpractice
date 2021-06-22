# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:08:02 2020

@author: engsv
"""
import pylab
import scipy
import copy

def LoadFileData(Filename):
    """
    Filnavnet skal være en string med filtype indikeret eks. test.txt
    Filen skal have punktum som decimal separator, størrelsesorden kan godt
    betegnes som eks. 1.2e+002 som 120
    Giver os en liste af x-værdier og en liste af y-værdier.
    """
    x = []
    y = []
    File = open(Filename,'r')
    for Line in File:
        LineData = Line.split(";")
        x.append(float(LineData[0]))
        y.append(float(LineData[1].replace("\n","")))
    
    #Hver linje kommer ud som en string som skal splittes, og
    #hver linje slutter åbenbart med \n, som vi så også skal erstatte
    #før vi kan lave det til en float #SkydMig
    File.close()
    return x,y

def FindIndices(x,a,b):
    """
    Vi har vores indices i lister, som skal slices, hvis vi vil integrere over et mindre område.
    a og b skal være de float værdier hvor vi vil starte og slutte. Desuden a < b
    x skal være vores liste af x-værdier
    Returner k og l som er index-værdierne, som kan bruges til at slice.
    Afstanden mellem x-værdier er generelt den samme ned til 0.482XXXX, hvor X varierer.
    Filen starter altid ved x = 7.998317e+002
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

def Baseline(x,y,a,b):
    """
    Finder gennemsnittet af y-værdierne mellem a og b
    """
    Total = 0
    c,d = FindIndices(x,a,b)[0],FindIndices(x,a,b)[1]
    SumY = y[c:d]
    Total = sum(SumY)
    Mean = Total/len(SumY)
    return Mean

def AdjustY(x,y,a,b):
    """
    Justerer y ift. en baseline fra a til b
    """
    Base = Baseline(x,y,a,b)
    AdjY = []
    for i in y:
        AdjY.append(i-Base)
    return AdjY

def Integration(x,y,a,b):
    """
    Integration af y fra a til b
    """
    c,d = FindIndices(x,a,b)[0],FindIndices(x,a,b)[1]
    Integral = scipy.trapz(y[c:d],x[c:d])
    return Integral

"""
pylab.figure("Sammenligning")    
x1 = LoadFileData("HDO_1.txt")[0]
y1 = LoadFileData("HDO_1.txt")[1]
Adjy1 = AdjustY(x1,y1,2100,2200) 
pylab.plot(x1,Adjy1, label = "HDO")
x2 = LoadFileData("D2O_1.txt")[0]
y2 = LoadFileData("D2O_1.txt")[1]
Adjy2 = AdjustY(x2,y2,2100,2200)
pylab.plot(x2,Adjy2,'r', label = "D2O")
x3 = LoadFileData("H2O_2_2.txt")[0]
y3 = LoadFileData("H2O_2_2.txt")[1]
Adjy3 = AdjustY(x3,y3,2100,2200)
pylab.plot(x3,Adjy3,'k', label = "H2O")
pylab.legend()
pylab.ylim(-0.01,0.05)
pylab.xlabel("Bølgetal [cm^-1]")
pylab.ylabel("Absorbans")

pylab.figure("Sammenligning af D2O")    
x1 = LoadFileData("D2O_1.txt")[0]
y1 = LoadFileData("D2O_1.txt")[1]
Adjy1 = AdjustY(x1,y1,2100,2200) 
pylab.plot(x1,Adjy1, label = "D2O_1")
x2 = LoadFileData("D2O_2.txt")[0]
y2 = LoadFileData("D2O_2.txt")[1]
Adjy2 = AdjustY(x2,y2,2100,2200)
pylab.plot(x2,Adjy2,'r', label = "D2O_2")
x3 = LoadFileData("D2O_3.txt")[0]
y3 = LoadFileData("D2O_3.txt")[1]
Adjy3 = AdjustY(x3,y3,2100,2200)
pylab.plot(x3,Adjy3,'k', label = "D2O_3")
x4 = LoadFileData("D2O_4.txt")[0]
y4 = LoadFileData("D2O_4.txt")[1]
Adjy4 = AdjustY(x4,y4,2100,2200)
pylab.plot(x4,Adjy4,'g', label = "D2O_4")
pylab.legend()
pylab.ylim(-0.01,0.05)
pylab.xlabel("Bølgetal [cm^-1]")
pylab.ylabel("Absorbans")

pylab.figure("Sammenligning af H2O")    
x1 = LoadFileData("H2O_2_2.txt")[0]
y1 = LoadFileData("H2O_2_2.txt")[1]
Adjy1 = AdjustY(x1,y1,2100,2200) 
pylab.plot(x1,Adjy1, label = "H2O_1")
x2 = LoadFileData("H2O_2_3.txt")[0]
y2 = LoadFileData("H2O_2_3.txt")[1]
Adjy2 = AdjustY(x2,y2,2100,2200)
pylab.plot(x2,Adjy2,'r', label = "H2O_2")
x3 = LoadFileData("H2O_2_4.txt")[0]
y3 = LoadFileData("H2O_2_4.txt")[1]
Adjy3 = AdjustY(x3,y3,2100,2200)
pylab.plot(x3,Adjy3,'k', label = "H2O_3")
pylab.legend()
pylab.ylim(-0.01,0.05)
pylab.xlabel("Bølgetal [cm^-1]")
pylab.ylabel("Absorbans")


pylab.figure("Sammenligning af HDO")    
x1 = LoadFileData("HDO_1.txt")[0]
y1 = LoadFileData("HDO_1.txt")[1]
Adjy1 = AdjustY(x1,y1,2100,2200) 
pylab.plot(x1,Adjy1, label = "HDO_1")
x2 = LoadFileData("HDO_2.txt")[0]
y2 = LoadFileData("HDO_2.txt")[1]
Adjy2 = AdjustY(x2,y2,2100,2200)
pylab.plot(x2,Adjy2,'r', label = "HDO_2")
x3 = LoadFileData("HDO_3.txt")[0]
y3 = LoadFileData("HDO_3.txt")[1]
Adjy3 = AdjustY(x3,y3,2100,2200)
pylab.plot(x3,Adjy3,'k', label = "HDO_3")
x4 = LoadFileData("HDO_1.txt")[0]
y4 = LoadFileData("HDO_1.txt")[1]
Adjy4 = AdjustY(x4,y4,2100,2200)
pylab.plot(x4,Adjy4,'g', label = "HDO_4")
pylab.legend()
pylab.ylim(-0.01,0.05)
pylab.xlabel("Bølgetal [cm^-1]")
pylab.ylabel("Absorbans")
"""

def AverageY():
    #Virker ikke da nogle af vores filer af en eller anden grund har flere y-værdier end de andre.
    y1 = LoadFileData("HDO_1.txt")[1]
    y2 = LoadFileData("HDO_2.txt")[1]
    y3 = LoadFileData("HDO_3.txt")[1]
    y4 = LoadFileData("HDO_4.txt")[1]
    AvgHDO = []
    for i in range(6639):
        Sum = y1[i]+y2[i]+y3[i]+y4[i]
        Mean = Sum/4
        AvgHDO.append(Mean)
        
    y1 = LoadFileData("D2O_1.txt")[1]
    y2 = LoadFileData("D2O_2.txt")[1]
    y3 = LoadFileData("D2O_3.txt")[1]
    y4 = LoadFileData("D2O_4.txt")[1]
    AvgD2O = []
    for i in range(6639):
        Sum = y1[i]+y2[i]+y3[i]+y4[i]
        Mean = Sum/4
        AvgD2O.append(Mean)
    
    y1 = LoadFileData("H20_2_2.txt")[1]
    y2 = LoadFileData("H20_2_3.txt")[1]
    y3 = LoadFileData("H20_2_3.txt")[1]
    AvgH2O = []
    for i in range(6639):
        Sum = y1[i]+y2[i]+y3[i]
        Mean = Sum/3
        AvgH2O.append(Mean)
    
    return AvgH2O,AvgHDO,AvgD2O
  
def AverageIntegralHDO(a,b):
    x1 = LoadFileData("HDO_1.txt")[0]
    y1 = LoadFileData("HDO_1.txt")[1]
    Adjy1 = AdjustY(x1,y1,2100,2200)
    
    x2 = LoadFileData("HDO_2.txt")[0]
    y2 = LoadFileData("HDO_2.txt")[1]
    Adjy2 = AdjustY(x2,y2,2100,2200) 
    
    x3 = LoadFileData("HDO_3.txt")[0]
    y3 = LoadFileData("HDO_3.txt")[1]
    Adjy3 = AdjustY(x3,y3,2100,2200) 
    
    x4 = LoadFileData("HDO_4.txt")[0]
    y4 = LoadFileData("HDO_4.txt")[1]
    Adjy4 = AdjustY(x4,y4,2100,2200)
    Int1 = Integration(x1,Adjy1,a,b)
    Int2 = Integration(x2,Adjy2,a,b)
    Int3 = Integration(x3,Adjy3,a,b)
    Int4 = Integration(x4,Adjy4,a,b)
    Int = [Int1, Int2,Int3,Int4]
    Mean = sum(Int)/len(Int)
    return Mean, Int1, Int2, Int3, Int4

def AverageIntegralH2O(a,b):
    x1 = LoadFileData("H2O_2_2.txt")[0]
    y1 = LoadFileData("H2O_2_2.txt")[1]
    Adjy1 = AdjustY(x1,y1,2100,2200)
    
    x2 = LoadFileData("H2O_2_3.txt")[0]
    y2 = LoadFileData("H2O_2_3.txt")[1]
    Adjy2 = AdjustY(x2,y2,2100,2200) 
    
    x3 = LoadFileData("H2O_2_4.txt")[0]
    y3 = LoadFileData("H2O_2_4.txt")[1]
    Adjy3 = AdjustY(x3,y3,2100,2200) 
    
    Int1 = Integration(x1,Adjy1,a,b)
    Int2 = Integration(x2,Adjy2,a,b)
    Int3 = Integration(x3,Adjy3,a,b)
    Int = [Int1,Int2,Int3]
    Mean = sum(Int)/len(Int)
    return Mean, Int1, Int2, Int3

def AverageIntegralD2O(a,b):
    x1 = LoadFileData("D2O_1.txt")[0]
    y1 = LoadFileData("D2O_1.txt")[1]
    Adjy1 = AdjustY(x1,y1,2100,2200)
    
    x2 = LoadFileData("D2O_2.txt")[0]
    y2 = LoadFileData("D2O_2.txt")[1]
    Adjy2 = AdjustY(x2,y2,2100,2200) 
    
    x3 = LoadFileData("D2O_3.txt")[0]
    y3 = LoadFileData("D2O_3.txt")[1]
    Adjy3 = AdjustY(x3,y3,2100,2200) 
    
    x4 = LoadFileData("D2O_4.txt")[0]
    y4 = LoadFileData("D2O_4.txt")[1]
    Adjy4 = AdjustY(x4,y4,2100,2200)
    
    Int1 = Integration(x1,Adjy1,a,b)
    Int2 = Integration(x2,Adjy2,a,b)
    
    Int3 = Integration(x3,Adjy3,a,b)
    Int4 = Integration(x4,Adjy4,a,b)
    
    Int = [Int1,Int2]
    Mean = sum(Int)/len(Int)
    return Mean, Int1, Int2

def EquilibriumConstant(a,b):
    HDO = AverageIntegralHDO(a,b)[0]
    H2O = AverageIntegralH2O(a,b)[0]
    alpha = 0.9985
    K = ((2*(H2O-HDO))**2)/(HDO*((1/alpha)*H2O-2*(H2O-HDO)))
    return K

def RefEquilibriumConstant(a,b):
    D2O = AverageIntegralD2O(a,b)[0]
    HDO = AverageIntegralHDO(a,b)[0]
    H2O = AverageIntegralH2O(a,b)[0]
    alpha = 0.9985
    K = ((2*(H2O+D2O-HDO))**2)/(HDO*((1/alpha)*H2O-D2O-(H2O+D2O-HDO)))
    return K

"""
HDO = AverageIntegralHDO(1840,2000)
H2O = AverageIntegralH2O(1840,2000)
alpha = 0.9985
K = ((2*(H2O-HDO))**2)/(HDO*((1/alpha)*H2O-2*(H2O-HDO)))
print(K)

HDO = AverageIntegralHDO(1640,1875)
H2O = AverageIntegralH2O(1640,1875)
alpha = 0.9985
K = ((2*(H2O-HDO))**2)/(HDO*((1/alpha)*H2O-2*(H2O-HDO)))
print(K)

HDO = AverageIntegralHDO(1725,1875)
H2O = AverageIntegralH2O(1725,1875)
alpha = 0.9985
K = ((2*(H2O-HDO))**2)/(HDO*((1/alpha)*H2O-2*(H2O-HDO)))
print(K)

HDO = AverageIntegralHDO(1710,1875)
H2O = AverageIntegralH2O(1710,1875)
alpha = 0.9985
K = ((2*(H2O-HDO))**2)/(HDO*((1/alpha)*H2O-2*(H2O-HDO)))
print(K)
"""

"""
x1 = LoadFileData("HDO_2.txt")[0]
y1 = LoadFileData("HDO_2.txt")[1]
Adjy1 = AdjustY(x1,y1,2100,2200)
HDO = Integration(x1,Adjy1,1710,1875)
H2O = AverageIntegralH2O(1710,1875)
alpha = 0.9985
K = ((2*(H2O-HDO))**2)/(HDO*((1/alpha)*H2O-2*(H2O-HDO)))
print(K)
"""

"""
HDO = AverageIntegralHDO(1745,1875)
H2O = AverageIntegralH2O(1745,1875)
alpha = 0.9985
K = ((2*(H2O-HDO))**2)/(HDO*((1/alpha)*H2O-2*(H2O-HDO)))
print(K)
"""

#print(EquilibriumConstant(1640,2000))
print(RefEquilibriumConstant(1640,1875))
#print(AverageIntegralHDO(1640,1875))
#print(AverageIntegralH2O(1640,1875))
#print(AverageIntegralD2O(1640,1875))