import pandas as pd
from radioDSP import RadioSignal

i_raw = pd.read_csv('data/i.txt', sep=" ", header=None)
q_raw = pd.read_csv('data/q.txt', sep=" ", header=None)

i = i_raw.iloc[:, 0]
q = q_raw.iloc[:, 0]

signal = RadioSignal(bit_width = 16, fs = 491.2, i = i, q = q)
signal.make_wave()
signal.plot_spectrogram()