# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 21:51:28 2019

@author: engsv
"""

"""
Alt udartethed skrives bare som yderligere modes. Antages harmonisk approksimation,
stiv rotor, og kT << dE_elektron. Antager høj-energi ved rotation og translation.
Antager at den elektroniske udartethed er 1
"""

import numpy as np
import math

#Standard enheder med mindre andet er givet
R = 8.3144621 
k = 1.3806488*10**-23
c = 2.99792458*10**8
h = 6.62606957*10**-34
h_bar = 1.054571726*10**-34
amu = 1.660538921*10**-27
g_E = 1 #Elektronisk udartethed

def linear_tilstandssum(dictionary):
    Lambda = h/(math.sqrt(2*math.pi*dictionary['M']*k*dictionary['T']))
    qT = dictionary['Volume']/(Lambda**3)
    if dictionary['N'] == 2:
        qR = k*dictionary['T']/(dictionary['Sigma']*h*c*dictionary['Rot1'])
    else:
        qR = (k*dictionary['T']/(dictionary['Sigma']*h*c*dictionary['Rot1']))*k*dictionary['T']/(dictionary['Sigma']*h*c*dictionary['Rot2']) #Hvilke molekyler har to rotationelle konstanter?
    qV = 1 #Opsætning til mit for loop
    for i in range(3*dictionary['N']-5):
        qV *= 1/(1-math.exp(-h*c*dictionary[i]/(k*dictionary['T'])))
    q = qT*qR*qV
    return q

def nonlinear_tilstandssum(dictionary):
    Lambda = h/(math.sqrt(2*math.pi*dictionary['M']*k*dictionary['T']))
    qT = dictionary['Volume']/(Lambda**3)
    qR = 1/dictionary['Sigma']*(k*dictionary['T']/(h*c))**(3/2)*math.sqrt(math.pi/(dictionary['Rot1']*dictionary['Rot2']*dictionary['Rot3']))
    qV = 1 #Opsætning til mit for loop
    for i in range(3*dictionary['N']-6):
        qV *= 1/(1-math.exp(-h*c*dictionary[i]/(k*dictionary['T'])))
    q = qT*qR*qV
    return q

#Definering af vores molekyle:
def tilstandssum():  
    if input("Standard betingelser? ja/nej: ") == 'ja':
        T = 298.15
        P = 10**5
    else:
        T = float(input("Temperatur i Kelvin: "))
        P = float(input("Tryk i Pascal: "))
    N = int(input("Antal atomer: "))
    M = amu*float(input("Masse, i amu: "))
    Sigma = int(input("Sigma: "))
    if  input("Får vi givet volumen? ja/nej: ") == 'ja':
        Volume = float(input("Volumen/molarvolumen i m^3: "))
    else:
        Volume = R*T/P
    linearity = input("Er molekylet lineært? ja/nej: ")
    
    if linearity == 'ja':
        Vib = 3*N-5
        linear = {'N': N, 'M': M, 'Sigma': Sigma, 'Volume': Volume, 'T': T, 'P': P}
        linear['Rot1'] = 100*float(input("Rotationelle bølgetal i cm^-1: "))
        for i in range(Vib):
            linear[i] = 100*float(input(str(i+1)+". vibrationelle bølgetal i cm^-1: "))
        print("Tilstandssummen er: " + str(linear_tilstandssum(linear)))
    
    if linearity == 'nej':
        Vib = 3*N-6
        nonlinear = {'N': N, 'M': M, 'Sigma': Sigma, 'Volume': Volume, 'T': T, 'P': P}
        nonlinear['Rot1'] = 100*float(input("1. rotationelle bølgetal i cm^-1: "))
        nonlinear['Rot2'] = 100*float(input("2. rotationelle bølgetal i cm^-1: "))
        nonlinear['Rot3'] = 100*float(input("3. rotationelle bølgetal i cm^-1: "))
        for i in range(Vib):
            nonlinear[i] = 100*float(input(str(i+1)+". vibrationelle bølgetal i cm^-1: "))
        print("Tilstandssummen er: " + str(nonlinear_tilstandssum(nonlinear)))
