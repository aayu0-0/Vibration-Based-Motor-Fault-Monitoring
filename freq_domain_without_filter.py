import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= LOAD DATA =================
data = pd.read_csv("22-02-26 corr mo.csv")
x, y, z = data.iloc[:, 0], data.iloc[:, 1], data.iloc[:, 2]

fs = 250
start = int(0.37 * fs)   # optional trimming

# Use raw signals (no filtering)
x_raw = x[start:]
y_raw = y[start:]
z_raw = z[start:]

# ================= FFT FUNCTION =================
def compute_fft(signal, fs):
    N = len(signal)
    fft_vals = np.fft.rfft(signal)
    fft_mag = np.abs(fft_vals) / N
    freqs = np.fft.rfftfreq(N, 1/fs)
    return freqs, fft_mag

# ================= FFTs =================
fx, X_fft = compute_fft(x_raw, fs)
fy, Y_fft = compute_fft(y_raw, fs)
fz, Z_fft = compute_fft(z_raw, fs)

# ================= AXIS SPECTRA =================
plt.figure(figsize=(12,8))

plt.subplot(3,1,1)
plt.plot(fx, X_fft)
plt.title("Raw X Spectrum")
plt.xlim(0, 120)

plt.subplot(3,1,2)
plt.plot(fy, Y_fft)
plt.title("Raw Y Spectrum")
plt.xlim(0, 120)

plt.subplot(3,1,3)
plt.plot(fz, Z_fft)
plt.title("Raw Z Spectrum")
plt.xlim(0, 120)
plt.xlabel("Frequency (Hz)")

plt.tight_layout()
plt.show()

# ================= MAGNITUDE SPECTRUM =================
a_mag = np.sqrt(x_raw**2 + y_raw**2 + z_raw**2)
fm, M_fft = compute_fft(a_mag, fs)

plt.figure(figsize=(12,5))
plt.plot(fm, M_fft)
plt.title("Raw Magnitude Spectrum (No Filtering)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.xlim(0, 120)
plt.grid(True)
plt.show()