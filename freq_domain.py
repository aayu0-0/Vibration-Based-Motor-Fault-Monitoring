import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# ================= LOAD DATA =================
data = pd.read_csv("22-02-26 corr mo.csv")
x, y, z = data.iloc[:, 0], data.iloc[:, 1], data.iloc[:, 2]

fs = 250
start = int(0.37 * fs)

# ================= FILTER FUNCTIONS =================
def highpass(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, cutoff / nyq, btype='high')
    return filtfilt(b, a, data)

def lowpass(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, cutoff / nyq, btype='low')
    return filtfilt(b, a, data)

# ================= BAND-PASS SIGNAL =================
x_bp = lowpass(highpass(x, 5, fs), 80, fs)[start:]
y_bp = lowpass(highpass(y, 5, fs), 80, fs)[start:]
z_bp = lowpass(highpass(z, 5, fs), 80, fs)[start:]

# ================= FFT FUNCTION =================
def compute_fft(signal, fs):
    N = len(signal)
    fft_vals = np.fft.rfft(signal)
    fft_mag = np.abs(fft_vals) / N
    freqs = np.fft.rfftfreq(N, 1/fs)
    return freqs, fft_mag

# ================= RAW SPECTRA =================
fx_raw, X_raw = compute_fft(x[start:], fs)
fy_raw, Y_raw = compute_fft(y[start:], fs)
fz_raw, Z_raw = compute_fft(z[start:], fs)

plt.figure(figsize=(12,8))
plt.subplot(3,1,1); plt.plot(fx_raw, X_raw); plt.title("Raw X Spectrum"); plt.xlim(0,120)
plt.subplot(3,1,2); plt.plot(fy_raw, Y_raw); plt.title("Raw Y Spectrum"); plt.xlim(0,120)
plt.subplot(3,1,3); plt.plot(fz_raw, Z_raw); plt.title("Raw Z Spectrum"); plt.xlim(0,120)
plt.tight_layout(); plt.show()

# ================= FILTERED SPECTRA =================
fx, X_fft = compute_fft(x_bp, fs)
fy, Y_fft = compute_fft(y_bp, fs)
fz, Z_fft = compute_fft(z_bp, fs)

plt.figure(figsize=(12,5))
plt.plot(fx, X_fft, label="X")
plt.plot(fy, Y_fft, label="Y")
plt.plot(fz, Z_fft, label="Z")
plt.title("Filtered Axis Spectra")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.xlim(0,120)
plt.legend()
plt.grid(True)
plt.show()

# ================= MAGNITUDE SPECTRUM =================
a_mag = np.sqrt(x_bp**2 + y_bp**2 + z_bp**2)
fm, M_fft = compute_fft(a_mag, fs)

plt.figure(figsize=(12,5))
plt.plot(fm, M_fft)
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.xlim(0,120)
plt.grid(True)
plt.show()

# ================= DOMINANT FREQUENCY =================
idx = np.argmax(M_fft[1:]) + 1
dom_freq = fm[idx]

print("Dominant Frequency:", dom_freq, "Hz")

# ================= HARMONICS =================
print("\nHarmonics:")
for k in range(2, 6):
    target = k * dom_freq
    if target > fs/2:
        break
    i = np.argmin(np.abs(fm - target))
    print(f"{k}x ({target:.2f} Hz): {M_fft[i]:.4f}")

# ================= ENERGY DISTRIBUTION =================
low = fm < 20
mid = (fm >= 20) & (fm < 60)
high = fm >= 60

print("\nEnergy Distribution")
print("Low (0–20 Hz):", np.sum(M_fft[low]))
print("Mid (20–60 Hz):", np.sum(M_fft[mid]))
print("High (60–125 Hz):", np.sum(M_fft[high]))

# ================= DOMINANT AXIS =================
x_peak, y_peak, z_peak = np.max(X_fft), np.max(Y_fft), np.max(Z_fft)

if max(x_peak, y_peak, z_peak) == x_peak:
    print("\nDominant direction: X-axis")
elif max(x_peak, y_peak, z_peak) == y_peak:
    print("\nDominant direction: Y-axis")
else:
    print("\nDominant direction: Z-axis")


# FFT without filters
fxx, X_raw = compute_fft(x[start:], fs)
fyy, Y_raw = compute_fft(y[start:], fs)
fzz, Z_raw = compute_fft(z[start:], fs)

plt.figure(figsize=(12,8))
plt.subplot(3,1,1); plt.plot(fxx, X_raw); plt.title
("Raw X Spectrum"); plt.xlim(0,120)
plt.subplot(3,1,2); plt.plot(fyy, Y_raw); plt.title
("Raw Y Spectrum"); plt.xlim(0,120)
plt.subplot(3,1,3); plt.plot(fzz, Z_raw); plt.title
("Raw Z Spectrum"); plt.xlim(0,120)
plt.tight_layout(); plt.show()