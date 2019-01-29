import sys
import numpy as np
from scipy import fftpack
from matplotlib import pyplot as plt


class RadioSignal():
    def __init__(self, bit_width, fs):
        '''
        :param bit_width: iq valid bit width
        :param fs: Mhz
        '''
        self.bit_width = bit_width
        self.fs = fs

    def make_wave(self,i, q):
        '''
        calculate time domain power with unit DB
        :param i: narray
        :param q: narray
        '''
        self.iq = i + 1j * q
        if np.isreal(self.iq).all():
            full_scale_rms = (2 ** (self.bit_width - 1) - 1) / np.sqrt(2)
        else:
            full_scale_rms = (2 ** (self.bit_width - 1) - 1)

        self.signal_power = np.abs(self.iq)
        self.power_db = 20 * np.log10(np.sqrt(self.signal_power)/full_scale_rms+ sys.float_info.min)

    def make_spectrum(self, i, q, window_type = "blackman", is_remove_dc = False, is_full_scale_spectrum = False):
        '''
        make spectrum from i,q narray
        :param i: narray
        :param q: narray
        :param window_type: "blackman", "hamming", "hanning"
        :param is_remove_dc: remove DC flag, True/False
        :param is_full_scale_spectrum: full/half spectrum flag, True/False
        '''
        self.iq = i + 1j * q
        if np.isreal(self.iq).all():
            full_scale_rms = (2 ** (self.bit_width - 1) - 1) / np.sqrt(2)
        else:
            full_scale_rms = (2 ** (self.bit_width - 1) - 1)

        self.mean_signal_power = np.mean(np.abs(self.iq) ** 2)
        self.power_db = 20 * np.log10(np.sqrt(self.mean_signal_power) / full_scale_rms + sys.float_info.min)

        window_types = ["blackman", "hamming", "hanning"]
        if window_type in window_types:
            win_func = eval("np.{}".format(window_type))
            window = win_func(self.iq.size)
            iq_fft = fftpack.fft(self.iq * window)

        else:
            iq_fft = fftpack.fft(self.iq)

        if is_remove_dc:
            iq_fft[0] = 1

        iq_fft = fftpack.fftshift(iq_fft)

        # And the power (sig_fft is of complex dtype)
        power = np.abs(iq_fft)
        iq_fft_normlize = power / np.sum(power) * self.mean_signal_power
        iq_fft_fullsacle_normlize = iq_fft_normlize / (full_scale_rms ** 2)
        self.iq_fft_db = 10 * np.log10(iq_fft_fullsacle_normlize + sys.float_info.min)

        self.fft_freq = fftpack.fftfreq(iq_fft.size, d=1 / self.fs)
        self.fft_freq = fftpack.fftshift(self.fft_freq)

        if is_full_scale_spectrum != True:
            n = self.iq_fft_db.size
            zero_db = self.iq_fft_db[0]
            self.iq_fft_db = self.iq_fft_db[n // 2: n] + 3.01
            self.iq_fft_db[0] = zero_db
            self.fft_freq = self.fft_freq[n // 2: n]

    def plot_wave(self):
        '''
        plot IQ domain db power figure
        :return:
        '''
        plt.figure(figsize=(6, 5))
        plt.plot(self.power_db)
        plt.xlabel('Time domain(T = 1/{}MHz)'.format(self.fs))
        plt.ylabel('Power(dB)')
        plt.show()


    def plot_spectrum(self):
        '''
        plot spectrum
        :return:
        '''
        plt.figure(figsize=(6, 5))
        plt.plot(self.fft_freq, self.iq_fft_db)
        plt.xlabel('Frequency [MHz]')
        plt.ylabel('Power(dB)')
        plt.show()