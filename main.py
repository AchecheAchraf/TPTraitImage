#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 12:28:50 2021

@author: chaari
"""
#from mat4py import loadmat
#import h5py
import scipy.io
import numpy as np
from utils import *
import matplotlib.pyplot as plt
from numpy import linalg as LA
from math import log


loaded = scipy.io.loadmat('reference.mat')
ref = loaded['im']
loaded = scipy.io.loadmat('sens.mat')
S = loaded['s']

# Paramètres de simulation
sigma=5 
R_values=[10]
sigma_value = [2,4]

sigma_values = [5, 10, 15]  # Différentes intensités de bruit à tester
R = 2

# Simulation des données avec différentes intensités de bruit
for sigma in sigma_values:
    reduced_FoV = pMRI_simulator(S, ref, sigma, R)
    
    # fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(10, 5))
    # for j in range(min(8, reduced_FoV.shape[2])):  # Pour chaque antenne 
    #     ax = axes[j // 4, j % 4]  # Calcul des indices pour les sous-graphiques
    #     ax.imshow(reduced_FoV[:, :, j],)  # Affichage de l'antenne en niveaux de gris
    #     ax.set_title(f'Antenne {j+1} ')
    #     ax.axis('off')
    
    # plt.suptitle(f"Images simulées avec R={R} et sigma={sigma}", fontsize=16)
    # plt.tight_layout()
    # plt.show()

    # Évaluation de l'impact du bruit sur la qualité des images
    reconstructed = reconstruct(reduced_FoV, S, sigma * np.eye(S.shape[2]), Lambda=1,R=R)
    #reconstructed = reconstruct_tikhonov(reduced_FoV, S, sigma * np.eye(S.shape[2]), Lambda=1,R=2)

    plt.suptitle(f"Images reconstruite avec R={R} et sigma={sigma}", fontsize=16)
    plt.imshow(reconstructed,cmap="gray")
    plt.show()
    snr = SignalToNoiseRatio(ref, reconstructed)
    print(f"SNR for sigma={sigma}: {snr} dB")
