# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 22:13:11 2021

@author: Subhadip_CSRE
"""

import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
#%%
product = 'Subset_S1A_IW_SLC__1SDV_20160824T001533_20160824T001600_012735_0140AB_4BC9_Orb_Cal_Deb_ML_Spk_TC'
date = '24-Aug'

theta_xP = 'F:/MDPI_2021/Canada/Sentinel-1/Final_Sentinel_1_products/' + product + '/C2/theta_xp.bin'
print(theta_xP)
H_xP = 'F:/MDPI_2021/Canada/Sentinel-1/Final_Sentinel_1_products/' + product + '/C2/H_dp.bin'

shp_filename = r'F:\MDPI_2021\Canada\shapefile\Crop_extent\crop_extent.shp'

src_ds1=gdal.Open(theta_xP) 
gt=src_ds1.GetGeoTransform()
rb1=src_ds1.GetRasterBand(1)
theta_data = rb1.ReadAsArray()
    
src_ds2=gdal.Open(H_xP) 
rb2=src_ds2.GetRasterBand(1)
ent_data = rb2.ReadAsArray()
    
#%%
import shapefile as shp

sf = shp.Reader(shp_filename) 
#plt.figure()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
#    plt.plot(x,y)
#plt.show()

mx = np.array(x)
mx = mx.reshape([len(mx),1])
px = np.floor((mx - gt[0]) / gt[1])

my = np.array(y)
my = my.reshape([len(my),1])
py = np.floor((my - gt[3]) / gt[5])

#plt.imshow(theta_data)
#plt.scatter(px[0],py[0], c = 'r', s = 40)
#plt.scatter(px[1],py[1], c = 'r', s = 40)
#plt.scatter(px[2],py[2], c = 'r', s = 40)
#plt.scatter(px[3],py[3], c = 'r', s = 40)

x_pix_low = int(px[0])
x_pix_high = int(px[2])
y_pix_low = int(py[1])
y_pix_high = int(py[0]) 

theta_crop = theta_data[x_pix_low:x_pix_high, y_pix_low:y_pix_high]
ent_crop = ent_data[x_pix_low:x_pix_high, y_pix_low:y_pix_high]
#%%
import matplotlib.colors as colors
import matplotlib as mpl

[row, col] = np.shape(theta_crop)

clustered_im = np.zeros([row, col])

for ii in range(row):
    for jj in range(col):
        if (theta_crop[ii,jj] >30 and theta_crop[ii,jj] <= 45):
            if (ent_crop[ii,jj] >= 0 and ent_crop[ii,jj] < 0.3):
                clustered_im[ii,jj] = 1
            if (ent_crop[ii,jj] >= 0.3 and ent_crop[ii,jj] < 0.5):
                clustered_im[ii,jj] = 4
            if (ent_crop[ii,jj] >= 0.5 and ent_crop[ii,jj] < 0.7):
                clustered_im[ii,jj] = 7
            if (ent_crop[ii,jj] >= 0.7 and ent_crop[ii,jj] <= 1.0):
                clustered_im[ii,jj] = 10
        
        if (theta_crop[ii,jj] >15 and theta_crop[ii,jj] <= 30):
            if (ent_crop[ii,jj] >= 0 and ent_crop[ii,jj] < 0.3):
                clustered_im[ii,jj] = 2
            if (ent_crop[ii,jj] >= 0.3 and ent_crop[ii,jj] < 0.5):
                clustered_im[ii,jj] = 5
            if (ent_crop[ii,jj] >= 0.5 and ent_crop[ii,jj] < 0.7):
                clustered_im[ii,jj] = 8
            if (ent_crop[ii,jj] >= 0.7 and ent_crop[ii,jj] <= 1.0):
                clustered_im[ii,jj] = 11
            
        if (theta_crop[ii,jj] >=0 and theta_crop[ii,jj] <= 15):
            if (ent_crop[ii,jj] >= 0 and ent_crop[ii,jj] < 0.3):
                clustered_im[ii,jj] = 3
            if (ent_crop[ii,jj] >= 0.3 and ent_crop[ii,jj] < 0.5):
                clustered_im[ii,jj] = 6
            if (ent_crop[ii,jj] >= 0.5 and ent_crop[ii,jj] < 0.7):
                clustered_im[ii,jj] = 9
            if (ent_crop[ii,jj] >= 0.7 and ent_crop[ii,jj] <= 1.0):
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

im_ratio = theta_crop.shape[1]/theta_crop.shape[0]
cbar = plt.colorbar(fraction=0.047*im_ratio)
cbar.set_ticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5])
cbar.ax.set_yticklabels(['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'Z10', 'Z11', 'Z12'])
saveFileName = 'smapvex16_cluster_xP__' + date + '.png'
file_savePath = 'F:/MDPI_2021/Canada/Sentinel-1/Images/' + saveFileName
print("Saved at: ",file_savePath)
fig.savefig(file_savePath, bbox_inches = 'tight', dpi = 1200, pad_inches = 0.0, 
            frameon = None)
#%%

plt.rcParams['font.size'] = 24
plt.rcParams['font.family'] = 'serif'

fig = plt.figure(figsize=(8, 8))
plt.imshow(theta_crop, vmin = 0, vmax= 45, cmap = 'jet')
#im_ratio = theta_crop.shape[1]/theta_crop.shape[0]
#cbar = plt.colorbar(fraction=0.047*im_ratio)
#cbar.set_ticks([ 0, 15, 30, 45])
plt.axis('off')


saveFileName = 'smapvex16_theta_xP__' + date + '.png'
file_savePath = 'F:/MDPI_2021/Canada/Sentinel-1/Images/' + saveFileName
print("Saved at: ",file_savePath)
fig.savefig(file_savePath, bbox_inches = 'tight', dpi = 1200, pad_inches = 0.0, 
            frameon = None)

#%%
fig = plt.figure(figsize=(8, 8))
plt.imshow(ent_crop, vmin = 0, vmax= 1, cmap = 'jet')
#im_ratio = ent_crop.shape[1]/ent_crop.shape[0]
#cbar = plt.colorbar(fraction=0.047*im_ratio)
#cbar.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
plt.axis('off')


saveFileName = 'smapvex16_ent_xP__' + date + '.png'
file_savePath = 'F:/MDPI_2021/Canada/Sentinel-1/Images/' + saveFileName
print("Saved at: ",file_savePath)
fig.savefig(file_savePath, bbox_inches = 'tight', dpi = 1200, pad_inches = 0.0, 
            frameon = None)  