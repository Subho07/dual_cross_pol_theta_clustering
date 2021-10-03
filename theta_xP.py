###############################################################################
#  Spatial_clustering_xP.py
#
#  Project:
#  Author:   Subhadip Dey, 
#  Email:    sdey2307@gmail.com
#  Created:  August 2021
#
###############################################################################
#  Copyright (c) 2021, Subhadip Dey
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal

#%%
def read_bin(file):
    ds = gdal.Open(file)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
   
    return arr

#%%

def write_bin(file,wdata,refData):
                
    ds = gdal.Open(refData)
    [cols, rows] = wdata.shape
            
    driver = gdal.GetDriverByName("ENVI")
    outdata = driver.Create(file, rows, cols, 1, gdal.GDT_Float32)
    outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
    outdata.SetProjection(ds.GetProjection())##sets same projection as input
                
    outdata.SetDescription(file)
    outdata.GetRasterBand(1).WriteArray(wdata)
    # outdata.GetRasterBand(1).SetNoDataValue(np.NaN)##if you want these values transparent
    outdata.FlushCache() ##saves to disk!! 
    
#%%
def conv2d(a, f):
    filt = np.zeros(a.shape)
    wspad = int(f.shape[0]/2)
    s = f.shape + tuple(np.subtract(a.shape, f.shape) + 1)
    strd = np.lib.stride_tricks.as_strided
    subM = strd(a, shape = s, strides = a.strides * 2)
    filt_data = np.einsum('ij,ijkl->kl', f, subM)
    filt[wspad:wspad+filt_data.shape[0],wspad:wspad+filt_data.shape[1]] = filt_data
    return filt
#%% 
from tkinter import filedialog
from tkinter import *
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

ws = 7 # CHANGE PROCESSING WINDOW SIZE HERE

kernel = np.ones((ws,ws),np.float32)/(ws*ws)
   
C11 = read_bin(folder_selected + '/C11.bin')
C11 = conv2d(np.real(C11),kernel)
C12_im = read_bin(folder_selected + '/C12_imag.bin')
C12_im = conv2d(np.real(C12_im),kernel)
C12_re = read_bin(folder_selected + '/C12_real.bin')
C12_re = conv2d(np.real(C12_re),kernel)
C22 = read_bin(folder_selected + '/C22.bin')
C22 = conv2d(np.real(C22),kernel)

C12 = C12_re+1j*C12_im
C21 = np.conj(C12)


det_C2 = C11*C22-C12*C21
trace_C2 = C11 + C22

m1 = np.real(np.sqrt(1-(4*(det_C2/(trace_C2**2)))))
h = (C11 - C22)
g = C22
span = C11 + C22

val = (m1*span*h)/(C11*g+m1**2*span**2)
thet = np.arctan(np.real(val))
theta_xP = np.real(np.rad2deg(thet))

#%%
infile = folder_selected + '/C11.bin'
ofilegrvi = folder_selected + '/theta_xP.bin'
write_bin(ofilegrvi,theta_xP,infile) 
