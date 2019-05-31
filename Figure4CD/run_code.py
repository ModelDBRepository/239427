# ====================================================================================================
# run_code.py -- Simulates a feedforward network of excitatory neurons as in
#
# Ref: González-Rueda, A., Pedrosa, V., Feord, R., Clopath, C., Paulsen, O. Activity-dependent 
# downscaling of subthreshold synaptic inputs during slow wave sleep-like activity in vivo. 
# Neuron (2018).
#
# This code executes the following:
#  1. UP-state-mediated_plast_fig1CD_wake.py, which generates Syn_weights_wake_plast.npy
#  2. UP-state-mediated_plast_fig1CD_sleep.py, which generates Syn_weights_sleep_plast.npy
#     and takes Syn_weights_wake_plast.npy as input
#  3. Make_fig1CD.py, which generates one figure file and takes both Syn_weights_wake_plast.npy
#     and Syn_weights_sleep_plast.npy as input
# -----------------------------------------------------------------------
#
# Author: Victor Pedrosa <v.pedrosa15@imperial.ac.uk>
# Imperial College London, London, UK - Dec 2017
# ====================================================================================================


# Import modules -------------------------------------------------------------------------------------
import subprocess
import os
from time import time as time_now

# Create new directories if they don't exist ---------------------------------------------------------
newpath = r'Data/' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
    
newpath = r'Figures/' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

# start to count the time spent with simulations -----------------------------------------------------
time_in = time_now() 


# ====================================================================================================
# Run the simulations
# ====================================================================================================

# Run the main code for wake plasticity --------------------------------------------------------------
subprocess.call('python Step1-wake_learning/UP-state-mediated_plast_fig4CD_wake.py',shell=True)

# Run the main code for sleep plasticity -------------------------------------------------------------
subprocess.call('python Step2-sleep_learning/UP-state-mediated_plast_fig4CD_sleep.py',shell=True)

# Run the code to generate the figures ---------------------------------------------------------------

subprocess.call('python Step3-figures/Make_fig4CD.py',shell=True)


# stop counting the time and show the total time spent -----------------------------------------------
time_end = time_now()
total_time = (time_end-time_in)/60. # [min]

print('\n')
print('Simulation finally finished!')
print('Total time = {0:.2f} minutes'.format(total_time))



