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

ws = 7
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
thet = np.real(np.arctan(val))
theta_DP = np.rad2deg(thet)

#%%
infile = folder_selected + '/C11.bin'
ofilegrvi = folder_selected + '/theta_xP.bin'
write_bin(ofilegrvi,theta_DP,infile)            
#%%
# import matplotlib.pyplot as plt

# alpha = read_bin('E:/CVPR-2021/RS-2/C2_pp2/alpha.bin')
# alpha1 = 45 - alpha
# #%%
# hfont = {'fontname':'Cambria','size':12,'color':'black'}

# fig = plt.figure(figsize=(8,6))
# plt.imshow(theta_image)
# colorbar = plt.colorbar()
# colorbar.set_ticks(np.linspace(-45, 45, 7))
# plt.clim(-45,45)
# plt.set_cmap('twilight')

# for l in colorbar.ax.yaxis.get_ticklabels():
#     l.set_family("Cambria")
#     l.set_fontsize(20)
#     l.set_color('black')

# plt.axis('off')
# #%%
# fig.savefig(r'E:\CVPR-2021\CVPR_2021\images\txp_pp2_rs2.png',dpi=300,bbox_inches = 'tight',pad_inches = 0)
