# Convert .TDM and .TDMS files recorded with LabVIEW to .HDF5
# Requires the cTDMS module which need the National Intruments C library
# and therefore can only run in Windows
#
# NILIBDDC installation notes: 
# If running 64 bit Windows, the 64 bit version of the library needs to be installed.
# Copy nilibddc.lib from ./Dominonilibddc/dev/lib/64-bit/msvc64 and all the contents
# of /Dominonilibddc/dev/bin/64-bit to the cTDMS site-packages directory

# T.Branco @ LMB August 2014

import numpy as np
import os
import matplotlib.pylab as plt

import h5py

from cTDMS.cTDMS import TDM_File


filedir = 'Z:\data\Experiment Data\imaging\\'
savedir = 'Z:\data\Experiment Data\imaging\H5files\\'
#filedir = 'F:\Analysis\Adam\AdamAnalysis\NPYhrGFP\cells\\'
#savedir = 'F:\Analysis\Adam\AdamAnalysis\NPYhrGFP\cells\H5files\\'

h5fileList = os.listdir(savedir)

# Go through all files in filedir
for fname in os.listdir(filedir):
  ext = os.path.splitext(fname)[1]
  if (ext=='.tdms') | (ext=='.tdm'):
    if ('test_pulse' in fname)==False:   # Skip test_pulse files 
      H5fname =  fname.rstrip('.tdms') + '.hdf5'
      #print H5fname, (H5fname in h5fileList)

      # Skipped already converted files
      if (H5fname in h5fileList)==True:
        print 'skipped file', H5fname
        
      else:
        # Open TDM file
        print fname
        tdm  = TDM_File(filedir+fname)
        tdm.open()

        # Open HDF5 file
        H5fname = savedir + fname.rstrip('.tdms') + '.hdf5'
        f = h5py.File(H5fname, 'w')

        # Get TDM groups and data from Channels
        groups, hgroups = [], []
        for groupname in tdm:
          f.create_group(str(groupname))
          for channelname in tdm.Groups[groupname]:
              data = tdm.Groups[groupname][channelname][:]
              f.create_dataset('/'+str(groupname)+'/'+str(channelname), data=data)

        # Add attributes to H5 file
        for attr in tdm.attrs:
          f.attrs[attr] = str(tdm.attrs[attr])
          if '_rate_kHz' in attr: f.attrs['dt'] = 1./tdm.attrs[attr]
        f.attrs['TDMS_conversion'] = True

        # Close open files
        tdm.close()
        f.close()

