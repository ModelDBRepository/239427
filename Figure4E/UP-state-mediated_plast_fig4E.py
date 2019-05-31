##################################################################################
# UP-state-mediated_plast_fig4E.py -- Uses the simulator from network_simulator.py
# and runs a simulation of a plastic feedforward network following the findings
# of González-Rueda et al. (Neuron, 2018).
#
# On these simulations, synaptic weights are updated following the Up-state-mediated 
# plasticity described in the paper.
#
# Author: Victor Pedrosa
# Imperial College London, London, UK - Dec 2017
##################################################################################


# Clear everything!
def clearall():
	all = [var for var in globals() if var[0] != "_"]
	for var in all:
		del globals()[var]

clearall()

# -------------------------- Import libraries ------------------------------------

import numpy as np
from time import time as time_now
import sys

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

args = sys.argv
trial = int(args[1])

# ------------------------ Import parameters -------------------------------------

from imp import reload
import params; reload(params); import params as p
import SimStep; reload(SimStep); import SimStep as SS

time_in = time_now()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Initialization of time-dependent variables -------------------------------------

# Synaptic weights ---------------------------------------------------------------

WEE = np.zeros((1,p.NE))	# E-E connections

WEE[:] = np.linspace(0.1,1.0,p.NE)

WEE += np.random.normal(0,0.000001,(1,p.NE))
WEE = SS._rect(WEE) - SS._rect(WEE-p.w_max)


# Other variables ----------------------------------------------------------------

xbar_pre = np.zeros(p.NE) 		# Synaptic traces for presynaptic events
xbar_post = np.zeros(1) 		# Synaptic traces for postsynaptic events
Vmemb = np.zeros(p.NE+1)		# [mV] Membrane potential
ref = np.zeros(p.NE+1)			# Variable to identify the neurons within the refractory time
gSynE = np.zeros(p.NE)			# Synaptic conductance for excitatory connections
Iext = np.zeros(p.NE+1)		# [pA] External current for each neuron


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create variables to "save" the results -----------------------------------------

subsampling = 100
WEE_all = np.zeros((int(p.nSteps/subsampling)+1,1,p.NE))
WEE_all[0] = WEE
WEE_var = 1.*WEE

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Run the code -------------------------------------------------------------------

for step in range(p.nSteps):
	WEE_in = WEE
	
	Vmemb,ref,xbar_pre,xbar_post,gSynE,WEE,Iext \
	= SS.SimStep (Vmemb,ref,xbar_pre,xbar_post,gSynE,WEE,Iext,"up")
	
	WEE_diff = WEE - WEE_in
	WEE_var = WEE_var + WEE_diff
	WEE = WEE_in
		
	if (((step+1) % subsampling) == 0):
		WEE_all[int(step/subsampling)+1,:] = WEE_var # save the synaptic weights

	
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Compute the total time spent with the simulation -------------------------------

time_end = time_now()
time_total = time_end - time_in

np.save('Data/Wall_{0:03d}'.format(trial),WEE_all[[0,-1]])

print('')
print('Trial = {1:3d} \n Total time = {0:.3f} segundos'.format(time_total,trial))
print("finished")