#!/usr/bin/env python3

import math
import numpy as np
import matplotlib
#matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
import scipy
import math
from scipy.optimize import curve_fit
from scipy.special import factorial
from scipy.optimize import minimize
from scipy.stats import poisson
from scipy.stats import norm
import cv2
import peakutils
import sys
import os


# Image size
width = 2592
height = 1944
z_count = 10# number of Z (Z varies 2mm for the data of September 2019, 1 mm otherwise)
nfiles = 500 #number of files per every Z
fnfiles = np.float64(nfiles)

pbgname = "../Results/ResultsSep/"
bgname = "data_fondo_CDS_1000"
pname= "../"

# el primer for se encarga de calcular las weas para data_beta_CDS y el segundo for se encatga de data_fondo_CDS

MaxFrame=np.load(pbgname+bgname+"_Max.npy")
dirname="data_beta_CDS"
direc="hmw"
dirname2="data_fondo_CDS"

frecuencia_flattened_data_fondo = np.zeros(2*260,dtype=np.uint64)
for z in range(1):
    filenamef="Y_CDS_z" +str(z).zfill(3)+ "_f"
    max_ads=260;
    plt.figure(figsize=(19.2,10.8))
    ############################   parte del CDS FONDO     ###########################################
    filenamef="Y_CDS_z" +str(0).zfill(3)+ "_f"
    for n in range(nfiles):
        tmpname=pname + dirname2 + "/" + filenamef + str(n).zfill(3) + ".npz"
        print(tmpname)
        tmp_data=np.load(tmpname)
        data=np.float64(tmp_data.f.arr_0)
        #ev_matrix=abs(data)>MaxFrame
        data_f=data#*ev_matrix
        flattened_data=data_f.flatten()
        for x in range(-260,260):
            f=np.float64(np.count_nonzero(flattened_data==np.float64(x)))
            frecuencia_flattened_data_fondo[x+260]+=f    

for z in range(z_count):
    filenamef="Y_CDS_z" +str(z).zfill(3)+ "_f"
    max_ads=260;
    plt.figure(figsize=(19.2,10.8))
    ######################  Parte del CDS BETA        ###########################33
    frecuencia_flattened_data = np.zeros(2*260,dtype=np.uint64)
    for n in range(nfiles):
        tmpname=pname + dirname + "/" + filenamef + str(n).zfill(3) + ".npz"
        print(tmpname)
        tmp_data=np.load(tmpname)
        data=np.float64(tmp_data.f.arr_0)
        ev_matrix=abs(data)>MaxFrame
        data_f=data*ev_matrix
        flattened_data=data_f.flatten()
        for x in range(-260,260):
            f=np.float64(np.count_nonzero(flattened_data==np.float64(x)))
            frecuencia_flattened_data[x+260]+=f
    frec=frecuencia_flattened_data
    x=np.array(range(-1*max_ads,max_ads))
    plt.hist(x,bins=2*max_ads,density=True, weights=frec,log=True,histtype = 'step',fill=None)
    ############################   parte del CDS FONDO     ###########################################
    plt.hist(x,bins=2*max_ads,density=True, weights=frecuencia_flattened_data_fondo,log=True,histtype = 'step',fill=None)
    plt.xlim((-1*max_ads*1.10,max_ads*1.10))
    plt.grid(True)
    plt.title("z = "+str(z))
    plt.ylabel('frec')
    plt.xlabel('ADS')
    plt.savefig(direc+str(z)+".png")
