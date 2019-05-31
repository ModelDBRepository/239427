##################################################################################
# Make_fig4CD.py - Load the data generated in steps 1 and 2 and generate figure 4CD
#
# Author: Victor Pedrosa
# Imperial College London, London, UK - Jan 2017
##################################################################################


# Clear everything!
def clearall():
	all = [var for var in globals() if var[0] != "_"]
	for var in all:
		del globals()[var]

clearall()

# -------------------------- Import libraries ------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.pyplot import cm
import matplotlib as mpl

mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['xtick.major.size'] = 5
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['ytick.major.size'] = 5
mpl.rcParams['ytick.minor.size'] = 3
mpl.rcParams['font.weight'] = 900
mpl.rcParams['axes.xmargin'] = 0
mpl.rcParams['xtick.major.pad']= 5
mpl.rcParams['ytick.major.pad']= 5
mpl.rcParams['xtick.direction']='out'
mpl.rcParams['ytick.direction']='out'

plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=19)
plt.rc('text', usetex=True)
mpl.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}\bfseries\boldmath"]
plt.rc('font', weight=400)
plt.ion()

def hide_frame(ax):
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')



# --------------------------------------------------------------------------------
# Import the data

# Choose the directory and load the files

fnames = ['./Data/Syn_weights_wake_plast.npy',\
				'./Data/Syn_weights_sleep_plast.npy']

SynW0 = np.load(fnames[0])[0,0]
SynW1 = np.load(fnames[0])[-1,0]
SynW2 = np.load(fnames[1])[-1,0]

# Compute the signal to noise ratio for all the stages

s_n0 = np.max(SynW0)/np.mean(SynW0)
s_n1 = np.max(SynW1)/np.mean(SynW1)
s_n2 = np.max(SynW2)/np.mean(SynW2)



# --------------------------------------------------------------------------------
# Plot figures

cmap = cm.inferno

color0 = cmap(0)
color1 = cmap(180)
color2 = cmap(70)

#"#{0:02x}{1:02x}{2:02x}".format(r,g,b)


fig = plt.figure(num=1, figsize=(7*0.7, 6*0.7), dpi=100, facecolor='w', edgecolor='k')
gs1 = GridSpec(3, 4)
gs1.update(left=0.15, right=0.95,bottom=0.2,top=0.92, hspace=0.25,wspace=1.3)

matSize = SynW0.shape[0]
xVec = np.arange(1,matSize+1,1)

ax = plt.subplot(gs1[0, 0:3])
hide_frame(ax)

frame1 = plt.gca()
frame1.axes.xaxis.set_ticklabels([])
plt.yticks([0,1])
#plt.ylabel('Syn weight', fontsize=15)
plt.ylim((0,1.05))

plt.plot(xVec,SynW0,color=color0,lw=1.8,label='Before pairing-weights')

ax = plt.subplot(gs1[1, 0:3])
hide_frame(ax)

frame1 = plt.gca()
frame1.axes.xaxis.set_ticklabels([])
plt.yticks([0,1])
#plt.ylabel('Syn weight', fontsize=15)
plt.ylim((0,1.05))

plt.plot(xVec,SynW0,color=color0,alpha=0.5,lw=1.8)
plt.plot(xVec,SynW1,color=color1,lw=1.8,label='After pairing-weights')


ax = plt.subplot(gs1[2, 0:3])
hide_frame(ax)

plt.xlabel('Input neuron',fontsize=20)
#plt.ylabel('Syn weight', fontsize=15)
plt.ylim((0,1.05))
plt.yticks([0,1])

plt.plot(xVec,SynW0,color=color0,alpha=0.5,lw=1.8)
plt.plot(xVec,SynW2,color=color2,lw=1.8,label='After pairing-weights')


fig.text(0.02, 0.5, 'Synaptic weight', fontsize=20, va='center', rotation='vertical')

# --------------------------------------------------------------------------------

plt.rc('ytick', labelsize=15)

ax = plt.subplot(gs1[0, 3])
hide_frame(ax)

plt.title('S/N', fontsize=18)
plt.xlim((0,1.0))
plt.xticks([])
plt.ylim((0.5,50))
plt.bar(0.2,s_n0,0.6,color=color0)
plt.yscale('log', nonposy='clip')

ax = plt.subplot(gs1[1, 3])
hide_frame(ax)

plt.xlim((0,1.0))
plt.xticks([])
plt.ylim((0.5,50))
plt.bar(0.2,s_n1,0.6,color=color1)
plt.yscale('log', nonposy='clip')

ax = plt.subplot(gs1[2, 3])
hide_frame(ax)

plt.xlim((0,1.0))
plt.xticks([])
plt.ylim((0.5,50))
plt.bar(0.2,s_n2,0.6,color=color2)
plt.yscale('log', nonposy='clip')

plt.savefig('./Figures/fig4CD.png',dpi=300)
