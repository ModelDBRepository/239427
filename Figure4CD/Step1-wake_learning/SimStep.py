##################################################################################
# SimStep.py -- Performs all the calculations to be executed in one integration 
# step. 
#
#
# Author: Victor Pedrosa
# Imperial College London, London, UK - Dec 2017
##################################################################################


import numpy as np

# ------------------------ Import parameters -------------------------------------

from imp import reload
import params; reload(params); import params as p


# ================================================================================
# Main code ----------------------------------------------------------------------
def _rect (x): return x*(x>0.)

def _Iext (Ipre):
	taufilt = 20 # [ms] filtering time constant
	Iext = Ipre - (Ipre-_rect((np.random.normal(0,2,p.NE+1))**3.))*p.dt/taufilt
	Iext[-1] = Ipre[-1] - (Ipre[-1]-(9+_rect((np.random.normal(0,2,1)))))*p.dt/taufilt
	return Iext

def SimStep (u,ref,xbar_pre,xbar_post,gSynE,WEE,Iext,s):
	# ----------------------------------------------------------------------------
	# Takes as the input:
	#   u: [NE] Membrane potential at time t
	#   xbar_pre: [NE] synaptic traces for presynaptic events
	#   xbar_post: [NE] synaptic traces for postsynaptic events
	#   gSyn_E: [NE] synaptic conductances fo excitatory connections
	#   WEE: [NExNE] Excitatory synaptic weights
	#   Iext: [NE+1] External current for each neuron
	#   s: [str] "up" or "wake" - state of the network
	# ----------------------------------------------------------------------------
	# Returns as output: (all variables for time t+dt)
	#   u_out: 
	#   xbar_pre_out: 
	#   xbar_post_out 
	#   gSynE_out 
	#   gSynI_out 
	#   WEE_out
	# ----------------------------------------------------------------------------
	
	spikes = (u>p.Vth) # Verify all the neurons that fired an action potential
	spikesE = spikes[:p.NE] # Excitatory neurons
	ref += spikes*p.Tref  # update the refractory variable
	
	# Update the synaptic conductances
	gSynE_out = gSynE + p.gBarEx * spikesE
	gSynE_out = gSynE_out - gSynE_out*p.step_tauSynEx
	
	# Update the membrane potential
	IsynE = -(u[-1] - p.EsynE)*np.dot(WEE,gSynE)
	Isyn = IsynE 
	Iext = _Iext(Iext)
	preferred = np.ones(p.NE+1)
	preferred[[17,28,61,64,83]] = 1.5
	
	u = u + (p.Vres-u)*spikes # reset the voltage for those who spiked
	u_out = u + (-u + p.R*preferred*Iext)*p.step_tau_m
	u_out[-1] = u_out[-1] + (Isyn)*p.step_tau_m
	u_out[(ref>0.001)] = p.Vres
	u_out = u_out + (p.Vspike-u_out+p.Vth)*(u_out>p.Vth) # add a constant to "see" the spikes
	
	ref = _rect(ref - p.dt)
	ref_out = ref
	
	# Update the synaptic traces
	xbar_pre_out = xbar_pre + spikesE
	xbar_pre_out = xbar_pre_out - xbar_pre_out*p.step_tp_plast
	xbar_post_out = xbar_post + spikes[-1]
	xbar_post_out = xbar_post_out - xbar_post_out*p.step_tm_plast
	
	# Update the synaptic weights
	auxMat = np.ones((1,p.NE))
	WEE_out = WEE + p.a_pre[s]*(auxMat*spikesE) + p.a_post[s]*(auxMat*spikes[-1]) \
		+ p.a_plus[s]*(auxMat*spikes[-1]) * xbar_pre  \
		+ p.a_minus[s]*(auxMat*xbar_post) * spikesE 
	
	WEE_out = _rect(WEE_out) - _rect(WEE_out-p.w_max) # apply bounds
	
	# normalize ***
	
	return u_out,ref_out,xbar_pre_out,xbar_post_out,gSynE_out,WEE_out,Iext