# radioDSP

This is an library for radio I/Q signal scientic computing. 
It's based on scientic computing library such as numpy, scipy and matplotlib.

You can use it easily plot spectrum or timedomian.Like this:

import pandas as pd  
from radioDSP import RadioSignal  

i_raw = pd.read_csv('data/i.txt', sep=" ", header=None)
q_raw = pd.read_csv('data/q.txt', sep=" ", header=None)

i = i_raw.iloc[:, 0]  
q = q_raw.iloc[:, 0]  

signal = RadioSignal(bit_width = 16, fs = 491.2)  
signal.make_spectrum(i, q, window_type = "blackman", is_remove_dc = False, is_full_scale_spectrum = True)  
signal.plot_spectrum()  
