# ![](https://latex.codecogs.com/gif.latex?\Theta_{\text{xP}}) and ![](https://latex.codecogs.com/gif.latex?H_{\text{xP}}) clustering for dual polarimetric SAR data (HH-HV or, VV-VH)

This repository helps to make cluster using the target characterozation parameter, ![](https://latex.codecogs.com/gif.latex?\Theta_{\text{xP}}) and the scattering entropy, ![](https://latex.codecogs.com/gif.latex?H_{\text{xP}}) information. The clustering plane and its feasible region are shown in the Figure 1.

<p align="center">
<img src="theta_entropy_theoretical_general_.png" width="500" height="400" alt = "Clustering plane. Shaded region is non feasible">
  
<em align="center">Figure 1. Clustering plane using ![](https://latex.codecogs.com/gif.latex?\Theta_{\text{xP}}) and ![](https://latex.codecogs.com/gif.latex?H_{\text{xP}}). Shaded region in black colour is non feasible. The two bounding curves are denoted as "curve I" and "curve II".</em>
</p>

The names and colours of zones are given in Figure 2.

<p align="center">
<img src="theta_entropy_theoretical_zones_.png" width="600" height="400" alt = "Clustering plane. Shaded region is non feasible">
  
<em align="center">Figure 2. Clustering zones and their names. It should be noted that for most of the natural targets ![](https://latex.codecogs.com/gif.latex?\Theta_{\text{xP}}) varies from ![](https://latex.codecogs.com/gif.latex?0^{\circ}) to ![](https://latex.codecogs.com/gif.latex?45^{\circ}). Hence, the clustering zones are shown within this range.</em>
</p>

# Up and Run

Requirements:

1. Python 3
2. Gdal, numpy, matplotlib
3. Dual pol SAR data (HH--HV or, VV--VH) in C2 format

a. Run the `theta_xP.py` file to generate ![](https://latex.codecogs.com/gif.latex?\Theta_{\text{xP}}) image.
b. Use `PolSARpro` software to compute the entropy image
c. Rename the entropy image to `H_xP.bin'
d. 
