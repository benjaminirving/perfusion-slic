
"""

Perfusion Slic demo


Run demo:

>>> python perfusion_slic_demo.py

Using QIN Breast data as an example. This data comes in matlab .mat format.


To load a 4D nifti image instead use:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
file1 = "dce_mri.nii"
img = nib.load(file1)

# Determining ratio of voxel sizes
hdr = img.get_header()
raw1 = hdr.structarr
pixdim = raw1['pixdim']

vox_size = np.abs(np.around([pixdim[1], pixdim[2], pixdim[3]], 2))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Image
img1 = np.array(img.get_data())

Author: Benjamin Irving (20141124)

"""

from __future__ import division, print_function, absolute_import

import numpy as np
import nibabel as nib
from time import time
from perfusionslic import PerfSLIC
import h5py
start1 = time()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Load Nifti data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Folders

# file1 = "dce_mri.nii"
# img = nib.load(file1)
#
# # Determining ratio of voxel sizes
# hdr = img.get_header()
# raw1 = hdr.structarr
# pixdim = raw1['pixdim']
#
# vox_size = np.abs(np.around([pixdim[1], pixdim[2], pixdim[3]], 2))
#
# #Image
# img1 = np.array(img.get_data())

# ~~~~~~~~~~~~~~~~~~ Load .mat data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

f = h5py.File('QIN-Breast-DCE-MRI-BC10-V1.mat', 'r')
img = f.get('da/data')
hdr = f.get('da/hdr')
SliceThickness = hdr["SliceThickness"][0]
PixelSpacing = hdr["PixelSpacing"][0]
vox_size = np.around([PixelSpacing[0], PixelSpacing[1], SliceThickness[0]])
img1 = np.transpose(img, [3, 2, 1, 0])

# Load reconstructed roi
# f2 = h5py.File('QIN-Breast-DCE-MRI-BC10-V1roi.mat', 'r')
# roi = f2.get('roi1')
# roi1 = np.transpose(roi, [2, 1, 0])

# Select a sub-region containing tumour (for speed and memory reasons)

img1 = img1[20:160, 35:180, :, :]
# roi1 = roi1[20:160, 35:180, :]

# ~~~~~~~~~~~~~~~~~~ Running Perfusion SLIC ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("Initialise the perf slic class")

ps1 = PerfSLIC(img1, vox_size)

print("Normalising image...")

ps1.normalise_curves()

print("Extracting features...")

ps1.feature_extraction(n_components=3)

print("Extracting supervoxels...")

segments = ps1.supervoxel_extraction(compactness=0.02, segment_size=1000)

# Plot the PCA modes
ps1.plot_pca_modes()

# Plot a static version of the supervoxels
ps1.plotstatic()

# plot a dynamic version of the image in the background
ps1.plotdynamic(img_slice=54, save_animation=True)

# ~~~~~~~~~~~~~~~~~~~~~ Saving region ~~~~~~~~~~~~~~~~~~~~~~~~~~~
time_complete = time() - start1
#
print("Saving a nifti version of the extracted segments ", end="")

file1 = 'slic_regions.nii'

rb1 = np.array(segments, dtype=np.int)
img = nib.Nifti1Image(rb1, np.eye(4))
img.update_header()
img.to_filename(file1)


print("Done")




