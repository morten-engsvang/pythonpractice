# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 20:42:23 2020

@author: engsv
"""
"""
#TO-DO

"""

"""
Jeg antager altid høj-temperatur for rotation og translation.
Antager at det er i den elektroniske grundtilstand.
Jeg udregner de molære værdier, og altid #SIenheder
Nulpunktsenergiberegningen antager at beholderen er stor nok til at E_T(0) -> 0
Desuden at vi definerer E_0(0) = 0. Så det er den vibrationelle nulpunktsenergi.
"""

import math
#Standard enheder med mindre andet er givet
R = 8.3144621; k = 1.3806488*10**-23; c = 2.99792458*10**8
h = 6.62606957*10**-34; h_bar = 1.054571726*10**-34; amu = 1.660538921*10**-27
N_A = 6.02214129*10**23

def test_data():
    #Test funktion
    SO2_attributes = {'T': 298.15, 'P': 10**5, 'M': 64.07*amu, 'V': 0.0227, 'Linear': False, 'Electronic': 1, 'Sigma': 2}
    SO2_vib = {0: [1152*100, 1.0], 1: [518*100, 1.0], 2: [1360*100, 1.0]}
    SO2_rot = {0: [2.03*100, 1.0], 1: [0.344*100, 1.0], 2: [0.294*100, 1.0]}
    SO2 = Molecule(SO2_attributes,SO2_vib,SO2_rot)
    print("Først SO2:")
    SO2.get_partition()
    print("Forventet output: qM = 7.2*10^34")
    SO2.get_heat_capacity()
    print("Forventet: C_Pm = 39.9")
    SO2.get_entropy()
    print("Forventet: S_m = 247.4")
    SO2.get_internal_energy()
    print("Forventet: U_m = 8067")
    SO2.get_gibbs_energy()
    print("")
    HCl_attributes = {'T': 298.15, 'P': 10**5, 'M': 36.45*amu, 'V': 0.02478956875115, 'Linear': True, 'Electronic': 1, 'Sigma': 1}
    HCl_vib = {0: [2991*100, 1.0]}
    HCl_rot = {0: [10.59*100, 1.0]}
    HCl = Molecule(HCl_attributes,HCl_vib,HCl_rot)
    print("Så HCl")
    HCl.get_partition()
    print("Forventet: qM = 1.033*10^32")
    HCl.get_entropy()
    print("Forventet: S_m = 187")

def evaluate_high_temp(T,x):
    #Bestemmer om der er høj temperatur eller ej, hvor T er temperaturen og x er den karakteristiske temp.
    if T >= 4*x:
        return True
    else:
        False

def create_molecule():
    #Skaber og returner en liste med alle de værdier som min molekyle class skal have
    attributes = {}
    if input("Standard betingelser? ja/nej: ") == 'ja':
        attributes['T'] = 298.15
        attributes['P'] = 10**5
    else:
        attributes['T'] = float(input("Temperatur i Kelvin: "))
        attributes['P'] = float(input("Tryk i Pascal: "))
    attributes['M'] = amu*float(input("Masse, i amu: "))
    attributes['Sigma'] = float(input("Sigma: "))
    if  input("Får vi givet volumen? ja/nej: ") == 'ja':
        attributes['V'] = float(input("Volumen/molarvolumen i m^3: "))
    else:
        attributes['V'] = R*attributes['T'] /attributes['P']
    if str(input("Er molekylet lineært? ja/nej: ")) == 'ja':
        attributes['Linear'] = True
    else:
        attributes['Linear'] = False
    attributes['Electronic'] = float(input("Hvad er den elektroniske udartethed i grundtilstanden: "))

    #For hvert bølgetal vil der være en liste med bølgetallet og udartetheden, hvor keys går fra 0 og op.
    vib = {}
    iterator = int(input("Hvor mange vibrationelle bølgetal er der? "))
    for i in range(iterator):
        temp_list = []
        temp_list.append(100*float(input("Hvad er det " + str(i+1) + ". vibrationelle bølgetal i cm^-1? ")))
        temp_list.append(float(input("Hvad er udartetheden: ")))
        vib[i] = temp_list

    rot = {}
    iterator = int(input("Hvor mange rotationelle bølgetal er der? "))
    for i in range(iterator):
        temp_list = []
        temp_list.append(100*float(input("Hvad er det " + str(i+1) + ". rotationelle bølgetal i cm^-1? ")))
        temp_list.append(float(input("Hvad er udartetheden: ")))
        rot[i] = temp_list

    molecule = [attributes, vib, rot]
    return molecule


class Molecule(object):
    def __init__(self, attributes, vib, rot):
         self.attributes = attributes #Har elementerne 'M', 'T', 'P', 'V' ,'Linear', 'Electronic', 'Sigma'
         self.vib = vib #Har en dictionary med vib. bølgetal med start 0 og op af
         self.rot = rot #Samme som vib bare med rot. bølgetal

    def characteristic(self):
        #Udregner de karakteristiske temperaturer
        #Output er en tuple med vib, rot.
        vib_char = []
        rot_char = []
        for i in self.vib:
            vib_char.append(h*c*self.vib[i][0]/k)
        for i in self.rot:
            rot_char.append(h*c*self.rot[i][0]/k)
        return(vib_char, rot_char)

    def linear_partition(self):
        #Finder tilstandssummerne for et lineært molekyle returner en tuple
        Lambda = h/(math.sqrt(2*math.pi*self.attributes['M']*k*self.attributes['T']))
        qT = self.attributes['V']/(Lambda**3)
        qR = k*self.attributes['T']/(h*c*self.rot[0][0]*self.attributes['Sigma'])
        qV = 1
        char = self.characteristic()
        for i in self.vib:
            if evaluate_high_temp(self.attributes['T'],char[0][i]):
                qV *= (k*self.attributes['T']/(h*c*self.vib[i][0]))**self.vib[i][1]
            else:
                qV *= (1/(1-math.exp(-h*c*self.vib[i][0]/(k*self.attributes['T']))))**self.vib[i][1]
        qE = self.attributes['Electronic']
        qM = qT*qR*qV*qE
        return(qT,qR,qV,qE,qM)

    def non_linear_partition(self):
        #Finder tilstandssummerne for et ikke-lineært molekyle returner en tuple
        Lambda = h/(math.sqrt(2*math.pi*self.attributes['M']*k*self.attributes['T']))
        qT = self.attributes['V']/(Lambda**3)
        qR = 1/self.attributes['Sigma']*(k*self.attributes['T']/(h*c))**(3/2)*math.sqrt(math.pi/(self.rot[0][0]*self.rot[1][0]*self.rot[2][0]))
        qV = 1
        char = self.characteristic()
        for i in self.vib:
            if evaluate_high_temp(self.attributes['T'],char[0][i]):
                qV *= (k*self.attributes['T']/(h*c*self.vib[i][0]))**self.vib[i][1]
            else:
                qV *= (1/(1-math.exp(-h*c*self.vib[i][0]/(k*self.attributes['T']))))**self.vib[i][1]
        qE = self.attributes['Electronic']
        qM = qT*qR*qV*qE
        return(qT,qR,qV,qE,qM)

    def heat_capacity(self):
        #Beregner varmekapacitet og returner en tuple
        C_T = (3/2)*R
        if self.attributes['Linear']:
            C_R = R
        else:
            C_R = (3/2)*R
        C_V = 0
        char = self.characteristic()
        for i in self.vib:
            if evaluate_high_temp(self.attributes['T'],char[0][i]):
                C_V += self.vib[i][1]*2*R
            else:
                C_V += self.vib[i][1]*R*((char[0][i]/self.attributes['T'])**2)*(math.exp(-char[0][i]/(2*self.attributes['T']))/(1-math.exp(-char[0][i]/self.attributes['T'])))**2
        C_Vm = C_T + C_R + C_V
        C_Pm = C_Vm + R
        return(C_T,C_R,C_R,C_Vm,C_Pm)
        
    def entropy(self):
        #Returnerer entropien som en tuple, det er uden residual entropi
        Lambda = h/(math.sqrt(2*math.pi*self.attributes['M']*k*self.attributes['T']))
        S_T = R*math.log(self.attributes['V']*math.exp(5/2)/(N_A*Lambda**3))
        if self.attributes['Linear']:
            part = self.linear_partition()
        else:
            part = self.non_linear_partition()
        
        if self.attributes['Linear']:
            S_R = R+R*math.log(part[1])
        else:
            S_R = (3/2)*R+R*math.log(part[1])
        
        char = self.characteristic()
        S_V = 0
        for i in self.vib:
            S_V += self.vib[i][1]*R*((char[0][i]/self.attributes['T'])/(math.exp(char[0][i]/self.attributes['T'])-1)-math.log(1-math.exp(-char[0][i]/self.attributes['T'])))
        S_m = S_T + S_R + S_V
        return(S_T,S_R,S_V,S_m)
    
    def internal_energy(self):
        #Returnerer molær U(T)-U(0) som en tuple
        #Da vi er i elektronisk grundtilstand er den elektroniske forskel 0
        if self.attributes['Linear']:
            U_R = k*self.attributes['T']
        else:
            U_R = (3/2)*k*self.attributes['T']
        U_T = (3/2)*k*self.attributes['T']
        U_E = 0
        U_V = 0
        char = self.characteristic()
        for i in self.vib:
            if evaluate_high_temp(self.attributes['T'], char[0][i]):
                U_V += self.vib[i][1]*k*self.attributes['T']
            else:
                U_V += self.vib[i][1]*h*c*self.vib[i][0]/(math.exp(h*c*self.vib[i][0]/(k*self.attributes['T']))-1)
        U_m = (U_R + U_T + U_E + U_V)*N_A
        return(U_R,U_T,U_E,U_V,U_m)
    
    def gibbs_energy(self):
        #Returnerer molær Gibbs energi: G(T)-G(0)
        if self.attributes['Linear']:
            part = self.linear_partition()[4]
        else:
            part = self.non_linear_partition()[4]
        
        G_m = -R*self.attributes['T']*math.log(part/N_A)
        return G_m
    
    def zero_point_energy(self):
        #Finder den molære nulpunktsenergi
        #Vi antager at beholderen er stor nok til at den translationelle energi er næsten kontinuær.
        E_V = 0
        for i in self.vib:
            E_V += N_A*self.vib[i][1]*0.5*h*c*self.vib[i][0]
        return E_V

    def get_characteristic(self):
        char = self.characteristic()
        print("Karakteristiske temperaturer:","Vibrationelle:", char[0], "Rotationelle:", char[1])

    def get_partition(self):
        if self.attributes['Linear']:
            part = self.linear_partition()
            print("Tilstandsummer:","qT:", part[0], "qR:", part[1], "qV:", part[2], "qE:", part[3], "qM:", part[4])
        else:
            part = self.non_linear_partition()
            print("Tilstandssummer:","qT:", part[0], "qR:", part[1], "qV:", part[2], "qE:", part[3], "qM:", part[4])
    
    def get_heat_capacity(self):
        heat = self.heat_capacity()
        print("Varmekapacitet","C_T:", heat[0], "C_R:", heat[1], "C_V:", heat[2], "C_Vm:", heat[3], "C_Pm:", heat[4])
        
    def get_entropy(self):    
        entropy = self.entropy()
        print("Entropien:", "S_T:", entropy[0], "S_R:", entropy[1], "S_V:", entropy[2], "S_m:", entropy[3])
    
    def get_internal_energy(self):
        inter = self.internal_energy()
        print("Indre energi, kun samlet er molært:", "U_R:", inter[0], "U_T:", inter[1], "U_E:", inter[2], "U_V:", inter[3], "U_m:", inter[4])
        
    def get_gibbs_energy(self):
        gibbs = self.gibbs_energy()
        print("Gibbs energi:", "G_m", gibbs)
    
    def get_zero_point(self):
        zero = self.zero_point_energy()
        print("Nulpunktsenergien:", "E_0", zero)
    
data = create_molecule()
molekyle = Molecule(data[0],data[1],data[2])