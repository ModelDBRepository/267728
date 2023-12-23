########################################################################
#Jan 2015
#Leo Medina
#
#June 2022
#Modified by Nathan Titus
#
#Dorsal Column Fiber Model: Runs, records, and saves DC fiber responses to SCS
#
#This model is based on the MRG fiber model:
#
#McIntyre CC, Richardson AG, and Grill WM. Modeling the excitability of
#mammalian nerve fibers: influence of afterpotentials on the recovery
#cycle. Journal of Neurophysiology 87:995-1006, 2002.
#
#########################################################################

from __future__ import division
from neuron import h
import stimdb as stim
import os
import numpy as np
import sys

# Simulation parameters #######################################################
amp = float(sys.argv[len(sys.argv)-6])/1000 # mA
yval = float(sys.argv[len(sys.argv)-5]) #um
zval = float(sys.argv[len(sys.argv)-4]) #um
fiberD = float(sys.argv[len(sys.argv)-3])/10 # um
nnodes = int(sys.argv[len(sys.argv)-2])
rx_file = sys.argv[len(sys.argv)-1]
outname = "modelDBExample" # folder created for output, can rename

if (not os.path.exists("Output/{}".format(outname))):
    os.mkdir("Output/{}".format(outname))

tstop = 5000                # ms
temperature = 37               # Celsius degrees
dtval = 0.025

v_init = -77.3                   # mV
sampinvl = 0.025				# ms

# SCS Waveform Parameters ####################################
source_param = {"waveform": "biphasic_pulse_train",
                "amp": amp,  # mA
                "delay": 20,    # ms
                "PW": .225,    # ms
                "ftrain": .09,  # kHz
                "tstop": tstop,   # ms
		        "GAP": .1}

# Optional Point Source Electrode Params ###########################
sigma = (1 / 12e3, 1 / 3e3, 1 / 3e3)     # S/mm
electrode1 = {"x": -1,          # mm
              "y": 1,         # mm
              "z": 0,          # mm
              "polarity": -1}  # 1: positive, -1: negative
electrode2 = {"x": 1,          # mm
              "y": 1,         # mm
              "z": 0,          # mm
              "polarity": 1}  # 1: positive, -1: negative
electrodes = (electrode1,electrode2,)

# NEURON parameters ###########################################################
h.load_file('model/DCfiber.hoc')
h.load_file('stdrun.hoc')
h.tstop = tstop
h.celsius = temperature
h.v_init = v_init
h.dt = dtval
stimvec = h.Vector()
tvec = h.Vector()
timevec = h.Vector()
timevec.from_python(np.arange(0, tstop, sampinvl))

# Fiber model #################################################################
midnode = int(nnodes / 2)
channel_type = 231
constant_cm = 1
c_dc = 1
is_xtra = 1

fiber = h.DCFiber(fiberD, nnodes, channel_type, constant_cm, c_dc, is_xtra)

if channel_type == 231:
    h.HSbiasV_axnodena2 = -15

# Calculate Ve ################################################################
stimvec, tvec = stim.waveform_t(source_param)
for s in fiber.sl:
    s.insert("xtra")
stim.set_rx(fiber, fiberD, electrodes, sigma, rx_file)
stim.attach_stim(fiber, stimvec, tvec)

# Record Voltage at Center and Endpoints ###########################
vm = h.Vector()
vm.record(fiber.axon.node[midnode](.5)._ref_v, timevec)
vm0 = h.Vector()
vm0.record(fiber.axon.node[2](.5)._ref_v, timevec)
vm1 = h.Vector()
vm1.record(fiber.axon.node[nnodes-3](.5)._ref_v, timevec)
t = h.Vector()
t.record(h._ref_t, timevec)

# Run Simulation ############################################
h.init()
h.run()

# Save Results ###############################################
fname = h.File()
fname.wopen("Output/{}/{}{}_{}_{}_{}.txt".format(outname,outname,int(yval),int(zval),int(amp*1000),int(fiberD*10)))
vm.vwrite(fname)
fname.close()
fname = h.File()
fname.wopen("Output/{}/{}{}_{}_{}_{}_0.txt".format(outname,outname,int(yval),int(zval),int(amp*1000),int(fiberD*10)))
vm0.vwrite(fname)
fname.close()
fname = h.File()
fname.wopen("Output/{}/{}{}_{}_{}_{}_1.txt".format(outname,outname,int(yval),int(zval),int(amp*1000),int(fiberD*10)))
vm1.vwrite(fname)
fname.close()
