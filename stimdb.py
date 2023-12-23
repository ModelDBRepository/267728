########################################################################
#Jan 2015
#Leo Medina
#
#June 2022
#Modified by Nathan Titus
#
#Dorsal Column Fiber Model: SCS Waveform Determination
#
#
#########################################################################


import numpy as np
from neuron import h

# Define the SCS Waveform Shape for Vector.play() ###########################
def waveform_t(source_param):

    delta_t = h.dt
    amp = source_param['amp']
    delay = 0
    if 'delay' in source_param:
        delay = source_param['delay']
    tstop = source_param['tstop']
    waveform = source_param['waveform']
    PW = source_param['PW']
    GAP = 0
    if 'GAP' in source_param:
        GAP = source_param['GAP']

    stimvec = h.Vector(0)
    tvec = h.Vector(0)
    if waveform == 'monophasic_pulse':
        stimvec.resize(6)
        stimvec.fill(0)
        stimvec.x[2] = amp
        stimvec.x[3] = amp
        tvec.resize(6)
        tvec.fill(0)
        tvec.x[1] = delay
        tvec.x[2] = delay
        tvec.x[3] = delay + PW
        tvec.x[4] = delay + PW
        tvec.x[5] = delay + PW + delta_t
        
    elif waveform == 'biphasic_pulse':
        stimvec.resize(10)
        stimvec.fill(0)
        stimvec.x[2] = amp
        stimvec.x[3] = amp
        stimvec.x[6] = -amp
        stimvec.x[7] = -amp
        tvec.resize(10)
        tvec.fill(0)
        tvec.x[1] = delay
        tvec.x[2] = delay 
        tvec.x[3] = delay + PW 
        tvec.x[4] = delay + PW 
        tvec.x[5] = delay + PW + GAP
        tvec.x[6] = delay + PW + GAP
        tvec.x[7] = delay + 2 * PW + GAP
        tvec.x[8] = delay + 2 * PW + GAP
        tvec.x[9] = delay + 2 * PW + GAP + delta_t

    elif waveform == 'monophasic_pulse_train':
        stimvec.append(0)
        tvec.append(0)
        period = 1.0 / source_param['ftrain']
        ti = delay
        while ti < (tstop - PW):
            stimvec.append(0)
            tvec.append(ti)

            stimvec.append(amp)
            tvec.append(ti)

            stimvec.append(amp)
            tvec.append(ti + PW)

            stimvec.append(0)
            tvec.append(ti + PW)

            ti += period
        stimvec.append(0)
        tvec.append(ti + PW + delta_t)

    elif waveform == 'biphasic_pulse_train':
        stimvec.append(0)
        tvec.append(0)
        period = 1.0 / source_param['ftrain']
        ti = delay
        while ti < (tstop-2*PW-GAP):
            stimvec.append(0)
            tvec.append(ti)
        
            stimvec.append(amp)
            tvec.append(ti)
        
            stimvec.append(amp)
            tvec.append(ti + PW)
        
            stimvec.append(0)
            tvec.append(ti + PW)
        
            stimvec.append(0)
            tvec.append(ti + PW + GAP)
        
            stimvec.append(-amp)
            tvec.append(ti + PW + GAP)
        
            stimvec.append(-amp)
            tvec.append(ti + 2 * PW + GAP)
        
            stimvec.append(0)
            tvec.append(ti + 2 * PW + GAP)
        
            ti += period
    
    
        while ti < 0:
            stimvec.append(0)
            tvec.append(ti)
            stimvec.append(amp)
            tvec.append(ti + delta_t)
            stimvec.append(amp)
            tvec.append(ti + PW - delta_t)
            stimvec.append(-amp)
            tvec.append(ti + PW + delta_t)
            stimvec.append(-amp)
            tvec.append(ti + 2 * PW - delta_t)
            stimvec.append(0)
            tvec.append(ti + 2 * PW)
            ti += period

        stimvec.append(0)
        tvec.append(ti + 2 * PW + GAP + delta_t)


    return stimvec, tvec

# Connect the SCS waveform to the fiber ###############################
def attach_stim(fiber, stimvec, tvec):
    # since is_xtra is GLOBAL, we only need to specify Vector.play()
    # for one instance of xtra, i.e. at just one internal node
    # of only one section that contains xtra

    stimvec.play(h._ref_is_xtra, tvec, 0)  # "interpolated" play
    # print "Stimulus vector attached!"

# Point the extracellular variables to xtra ##############################
def set_rx(fiber, fiberD, electrodes, sigma, rx_file):
    x = 0.5  # assuming 1 segment per section
    ii = 0
    for s in fiber.sl:
        s(x).x_xtra = fiber.xcoord[ii]
        s(x).y_xtra = fiber.ycoord[ii]
        s(x).z_xtra = fiber.zcoord[ii]
        h.setpointer(s(x)._ref_i_membrane, 'im', s(x).xtra)
        h.setpointer(s(x)._ref_e_extracellular, 'ex', s(x).xtra)
        ii += 1
    reset_rx(fiber, fiberD, electrodes, sigma, rx_file)

# Determine the extracellular voltage at each compartment #######################
def reset_rx(fiber, fiberD, electrodes, sigma, rx_file):
    x = 0.5  # assuming 1 segment per section
    if rx_file is None: # Use point source electrodes #
        for s in fiber.sl:
            xf = s(x).x_xtra
            yf = s(x).y_xtra
            zf = s(x).z_xtra
            rx = 0
            for elec in electrodes:
                if "is_intra" in elec and elec["is_intra"]:
                    continue
                pol = elec["polarity"]
                xe = elec["x"]
                ye = elec["y"]
                ze = elec["z"]
                if len(sigma) > 1:
                    sigma_x = sigma[0]
                    sigma_y = sigma[1]
                    rx += pol / (4 * np.pi *
                                 np.sqrt(sigma_y ** 2 * (xf - xe) ** 2 +
                                         sigma_y * sigma_x * ((zf - ze) ** 2 +
                                                              (yf - ye) ** 2)))
                else:
                    rx += pol / (4 * np.pi * sigma[0] * np.sqrt(
                                 (xf - xe) ** 2 +
                                 (yf - ye) ** 2 +
                                 (zf - ze) ** 2))
            s(x).rx_xtra = rx
    else: # Load voltages from external file #
        v_ext = np.loadtxt(rx_file)
        if len(v_ext) != fiber.total_sections():
            print("Warning! File length different from number of sections...")
        i = 0  
        for s in fiber.sl:
            s(x).rx_xtra = v_ext[i]
            i += 1


