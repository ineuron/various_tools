# Convert .TDM and .TDMS files recorded with LabVIEW to .HDF5
# Requires the cTDMS module which need the National Intruments C library
# and therefore can only run in Windows
#
# T.Branco @ LMB August 2014

import numpy as np
import os
import matplotlib.pylab as plt

import h5py

from cTDMS.cTDMS import TDM_File


# Open TDM file
#fileStr = './python/control_cell_1.TDM'
fileStr = './python/140124_10Ttx__2__test_pulse__2.tdms'

tdm  = TDM_File(fileStr)
tdm.open()

# Open HDF5 file
#fileStrH = './python/control_cell1.hdf5'
fileStrH = './python/test.hdf5'
f = h5py.File(fileStrH, 'w')


# Get TDM groups
groups, hgroups = [], []

for groupname in tdm:
    #groups.append(tdm.Groups[groupname])
    f.create_group(str(groupname))
    for channelname in tdm.Groups[groupname]:
        data = tdm.Groups[groupname][channelname][:]
        f.create_dataset('/'+str(groupname)+'/'+str(channelname), data=data)

for name in f:
    print name

# Add attributes to H5 file
for attr in tdm.attrs:
    f.attrs[attr] = tdm.attrs[attr]
f.attrs['TDMS_conversion'] = True

f.close()

# when looping skip *test_pulse*

