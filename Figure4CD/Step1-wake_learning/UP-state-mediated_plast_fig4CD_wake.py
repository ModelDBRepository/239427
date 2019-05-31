##################################################################################
# UP-state-mediated_plast_fig4CD_sleep.py -- Uses the simulator from network_simulator.py
# and runs a simulation of a plastic feedforward network following the findings
# of González-Rueda et al. (Neuron, 2018).
#
# On these simulations, synaptic weights are updated following the conventional STDP 
# (as described in the paper).
#
# Author: Victor Pedrosa
# Imperial College London, London, UK - Dec 2017
##################################################################################


# -------------------------- Import libraries ------------------------------------

import numpy as np
from time import time as time_now
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


# ------------------------ Import parameters -------------------------------------

from imp import reload
import params; reload(params); import params as p
import SimStep; reload(SimStep); import SimStep as SS

time_in = time_now()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Initialization of time-dependent variables -------------------------------------

# Synaptic weights ---------------------------------------------------------------

WEE = np.zeros((1,p.NE))	# E-E connections

WEE[:] = 0.2
WEE += 0.02*np.random.random((1,p.NE)) - 0.02*np.random.random((1,p.NE))
WEE = SS._rect(WEE) - SS._rect(WEE-p.w_max)


# Other variables ----------------------------------------------------------------

xbar_pre = np.zeros(p.NE) 		# Synaptic traces for presynaptic events
xbar_post = np.zeros(1) 		# Synaptic traces for postsynaptic events
Vmemb = np.zeros(p.NE+1)		# [mV] Membrane potential
ref = np.zeros(p.NE+1)			# Variable to identify the neurons going over refractory time
gSynE = np.zeros(p.NE)			# Synaptic conductance for excitatory connections
Iext = np.zeros(p.NE+1)		    # [pA] External current for each neuron

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create variables to "save" the results -----------------------------------------

subsampling = 1000 # To save weights only after specific intervals 
WEE_all = np.zeros((int(p.nSteps/subsampling)+1,1,p.NE))
WEE_all[0] = WEE

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Run the code -------------------------------------------------------------------

for step in range(p.nSteps):
	Vmemb,ref,xbar_pre,xbar_post,gSynE,WEE,Iext \
	= SS.SimStep (Vmemb,ref,xbar_pre,xbar_post,gSynE,WEE,Iext,"wake")
	
	if (((step+1) % subsampling) == 0):
		WEE_all[int(step/subsampling)+1,:] = WEE # save the synaptic weights

	
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Compute the total time spent with the simulation -------------------------------

time_end = time_now()
time_total = time_end - time_in

print('')
print('Wake plasticity >> Total time = {0:.3f} segundos'.format(time_total))
print("")


# Post-processing ----------------------------------------------------------------

np.save('./Data/Syn_weights_wake_plast',WEE_all)

