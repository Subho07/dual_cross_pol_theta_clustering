# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 22:13:11 2021

@author: Subhadip_CSRE
"""

import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt

product = 'GIVE_PRODUCT_DIRECTORY_HERE'
#date = '24-Aug'

theta_xP = product + '/C2/theta_xp.bin'
H_xP = product + '/C2/H_dp.bin'

src_ds1=gdal.Open(theta_xP) 
gt=src_ds1.GetGeoTransform()
rb1=src_ds1.GetRasterBand(1)
theta_data = rb1.ReadAsArray()
    
src_ds2=gdal.Open(H_xP) 
rb2=src_ds2.GetRasterBand(1)
ent_data = rb2.ReadAsArray()

import matplotlib.colors as colors
import matplotlib as mpl

[row, col] = np.shape(theta_xP)

clustered_im = np.zeros([row, col])

for ii in range(row):
    for jj in range(col):
        if (theta_xP[ii,jj] >30 and theta_xP[ii,jj] <= 45):
            if (H_xP[ii,jj] >= 0 and H_xP[ii,jj] < 0.3):
                clustered_im[ii,jj] = 1
            if (H_xP[ii,jj] >= 0.3 and H_xP[ii,jj] < 0.5):
                clustered_im[ii,jj] = 4
            if (H_xP[ii,jj] >= 0.5 and H_xP[ii,jj] < 0.7):
                clustered_im[ii,jj] = 7
            if (H_xP[ii,jj] >= 0.7 and H_xP[ii,jj] <= 1.0):
                clustered_im[ii,jj] = 10
        
        if (theta_xP[ii,jj] >15 and theta_xP[ii,jj] <= 30):
            if (H_xP[ii,jj] >= 0 and H_xP[ii,jj] < 0.3):
                clustered_im[ii,jj] = 2
            if (H_xP[ii,jj] >= 0.3 and H_xP[ii,jj] < 0.5):
                clustered_im[ii,jj] = 5
            if (H_xP[ii,jj] >= 0.5 and H_xP[ii,jj] < 0.7):
                clustered_im[ii,jj] = 8
            if (H_xP[ii,jj] >= 0.7 and H_xP[ii,jj] <= 1.0):
                clustered_im[ii,jj] = 11
            
        if (theta_xP[ii,jj] >=0 and theta_xP[ii,jj] <= 15):
            if (H_xP[ii,jj] >= 0 and H_xP[ii,jj] < 0.3):
                clustered_im[ii,jj] = 3
            if (H_xP[ii,jj] >= 0.3 and H_xP[ii,jj] < 0.5):
                clustered_im[ii,jj] = 6
            if (H_xP[ii,jj] >= 0.5 and H_xP[ii,jj] < 0.7):
                clustered_im[ii,jj] = 9
            if (H_xP[ii,jj] >= 0.7 and H_xP[ii,jj] <= 1.0):
                clustered_im[ii,jj] = 12
#%%
plt.rcParams['font.size'] = 24
plt.rcParams['font.family'] = 'serif'

colorsList = np.array(['#4169E1', '#00FFFF', '#8A2BE2', #blue 
        '#FFBF00', '#FFEA00', '#FFFF00', #yellow
        '#7CFC00', '#AFE1AF', '#008000', #green
        '#880808', '#D2042D', '#FA8072']) #red 
CustomCmap = colors.ListedColormap(colorsList)
bounds = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13])
norm = mpl.colors.BoundaryNorm(bounds, CustomCmap.N)
fig = plt.figure(figsize=(8, 8))
plt.imshow(clustered_im, cmap = CustomCmap, vmin=1, vmax=12, norm = norm)

plt.axis('off')

im_ratio = theta_xP.shape[1]/theta_xP.shape[0]
cbar = plt.colorbar(fraction=0.047*im_ratio)
cbar.set_ticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5])
cbar.ax.set_yticklabels(['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'Z10', 'Z11', 'Z12'])
saveFileName = 'cluster_xP_.png'
file_savePath = product + '/C2/' + saveFileName
print("Saved at: ",file_savePath)
fig.savefig(file_savePath, bbox_inches = 'tight', dpi = 1200, pad_inches = 0.0, 
            frameon = None)
