#:q
###Hell###iiao#a;lsk;lkajd make the imports
#Hello world
###test
#Hello
#Hello world
#lkj;lkj
#test1
import matplotlib.pyplot as plt
import numpy as np
from scipy import io, signal # we will also import the signal module, from s
def plot_spectrogram(spg, t, f, freq_lims=[0,100], plot_db=False):
    plt.figure(figsize=(15,4))
    if plot_db:
        plt.imshow(10*np.log10(spg), aspect='auto', extent=[t[0], t[-1], f[-1], f[0]])
    else:
        plt.imshow(spg, aspect='auto', extent=[t[0], t[-1], f[-1], f[0]])
        plt.xlabel('Time'); plt.ylabel('Frequency(Hz)');
        plt.ylim(freq_lims)
        plt.colorbar()
        plt.tight_layout()

T, fs = 20, 1000
t = np.arange(0,T,1/float(fs))
# simulate a signal
# refer to the function documentation for f0, t1, f1
sig = signal.chirp(t, f0=10, t1=20,f1=30)

# plot it
plt.figure(figsize=(15,3))
plt.plot(t,sig)
plt.savefig('static/plot0.png')plt.xlim([0,5])
plt.xlabel('Time (s)'); plt.ylabel('Voltage (V)');
