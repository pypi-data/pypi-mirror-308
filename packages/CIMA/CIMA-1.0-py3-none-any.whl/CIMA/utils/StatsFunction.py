#===============================================================================
#     This file is part of CIMA.
#
#     CIMA is a software designed to help the user in the manipulation
#     and analyses of genomic super resolution localisation data.
#
#      Copyright  2019-2023
#
#                Authors: Irene Farabella
#
#
#
#===============================================================================

from CIMA.segments.SegmentGaussian import TransformBlurrer
from CIMA.segments.SegmentInfo import Segment
from CIMA.maps import MapFeatures as MF
from CIMA.parsers import ParserCSV as Parser
import os
TB=TransformBlurrer()
from scipy.stats import linregress,ttest_ind,wilcoxon,mannwhitneyu,ks_2samp
from scipy.optimize import curve_fit
from scipy.stats import linregress
import numpy as np
import random

def statConvert(s):
	from decimal import Decimal
	P="{:.2E}".format(Decimal(s))
	if float(s) <=0.0001:
		stat="***"
	elif float(s) <=0.001:
		stat="***"
	elif float(s) <=0.01:
		stat="**"
	elif float(s) <=0.05:
		stat="*"
	else:
		stat=P
	return stat

def power_law(x, a, b):
    return a*np.power(x, b)

def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c
#Y=ax**2+b
def func_sqrt(x, m, c, c0 ):
    return c0 + x** 1.0/m * c
#Y=a*x** 1.0/m

def func2(x, a, b, c):
    return a * np.exp(-b * x) + c

def func_inverse1(x, m, c, c0):
    return c0 + m* (1.0/x**2) * c

def func(x, a, b, c, d):
    return a*np.exp(-c*(x-b))+d

def welch_ttest(x, y):
    #https://pythonfordatascienceorg.wordpress.com/welch-t-test-python-pandas/
    ## Welch-Satterthwaite Degrees of Freedom ##
    dof = (x.var()/x.size + y.var()/y.size)**2 / ((x.var()/x.size)**2 / (x.size-1) + (y.var()/y.size)**2 / (y.size-1))

    t, p = stats.ttest_ind(x, y, equal_var = False)

    #print("""Welch's t-test= %.4f, p-value = %.4f, Degrees of Freedom= %.4f""" %(t,p,dof))
    return t, p,dof


def Create_Random_Hom_Ratio(featuresel_list,rdeed1=1,samplesize=1000):
	#greater vrs smaller

    ration_random=[]
    random.seed(rdeed1)
    for i in range(samplesize):
        random_2=random.sample(featuresel_list,len(featuresel_list))
        for r in range(len(featuresel_list)):
            if len(random_2)>=2:
                Mf,Pf= random.sample(random_2, 2)
                if Mf[0]==Pf[0]:
                    pass
                else:
                    random_2.remove(Mf)
                    random_2.remove(Pf)
                    if Mf[1]>Pf[1]:
                        rat=Mf[1]/Pf[1]
                        ration_random.append(rat)
                    else:
                        rat=Pf[1]/Mf[1]
                        ration_random.append(rat)

    if len(featuresel_list)>len(ration_random):
        print("Change random seed")
        print(len(featuresel_list),len(ration_random))
    else:
        return ration_random

def Create_Random_Hom_Ratio_smalloverlarger(featuresel_list,rdeed1=1,samplesize=1000):


    ration_random=[]
    LEN=len(list(featuresel_list))
    random.seed(rdeed1)
    for i in range(samplesize):
        random_2=random.sample(list(featuresel_list),LEN)
        for r in range(LEN):
            if len(random_2)>=2:
                Mf,Pf= random.sample(random_2, 2)
                if Mf[0]==Pf[0]:
                    pass
                else:
                    random_2.remove(Mf)
                    random_2.remove(Pf)
                    if Mf[1]>Pf[1]:
                        rat=Pf[1]/Mf[1]
                        ration_random.append(rat)
                    else:
                        rat=Mf[1]/Pf[1]
                        ration_random.append(rat)

    if LEN>len(ration_random):
        print("Change random seed")
        print(LEN,len(ration_random))
    else:
        return ration_random

def Create_Random_Hom_Ratio_largeroversmaller(featuresel_list,rdeed1=1,samplesize=1000):


    ration_random=[]
    LEN=len(list(featuresel_list))
    random.seed(rdeed1)
    for i in range(samplesize):
        random_2=random.sample(list(featuresel_list),LEN)
        for r in range(LEN):
            if len(random_2)>=2:
                Mf,Pf= random.sample(random_2, 2)
                if Mf[0]==Pf[0]:
                    pass
                else:
                    random_2.remove(Mf)
                    random_2.remove(Pf)
                    if Mf[1]<Pf[1]:
                        rat=Pf[1]/Mf[1]
                        ration_random.append(rat)
                    else:
                        rat=Mf[1]/Pf[1]
                        ration_random.append(rat)

    if LEN>len(ration_random):
        print("Change random seed")
        print(LEN,len(ration_random))
    else:
        return ration_random


def Create_Random_Hom_Ratio_Paternal_Origin(listhomfeature,rdeed1=16734,rdeed2=3535,samplesize=100,parentalnorm=False):
    ration_random=[]
    LEN=len(list(listhomfeature))
    for i in range(samplesize):
        m,p,n=zip(*listhomfeature)
        Matpool=list(zip(m,n))
        Patpool=list(zip(p,n))
        for r in range(LEN):
            random.seed(rdeed1)
            Mf= random.sample(Matpool, 1)[0]
            random.seed(rdeed2)
            Pf= random.sample(Patpool, 1)[0]    
            if Mf[1]==Pf[1]:
                pass
            else:
                #print (Mf)
                Matpool.remove(Mf)
                Patpool.remove(Pf)
                if parentalnorm:
                    ration_random.append(((Mf[0]/Pf[0])/Mf[0]))
                else:
                    ration_random.append((Mf[0]/Pf[0])) 
    if len(listhomfeature)>len(ration_random):
        print("Change random seed")
        print(len(listhomfeature),len(ration_random))
    else:
        return ration_random
