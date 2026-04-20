import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.stats import kurtosis, skew


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


# ================= FILTERED SIGNALS =================

# High-pass only
x_hp = highpass(x, 5, fs)[start:]
y_hp = highpass(y, 5, fs)[start:]
z_hp = highpass(z, 5, fs)[start:]

# Low-pass only
x_lp = lowpass(x, 80, fs)[start:]
y_lp = lowpass(y, 80, fs)[start:]
z_lp = lowpass(z, 80, fs)[start:]

# Band-pass (HP → LP)
x_bp = lowpass(highpass(x, 5, fs), 80, fs)[start:]
y_bp = lowpass(highpass(y, 5, fs), 80, fs)[start:]
z_bp = lowpass(highpass(z, 5, fs), 80, fs)[start:]


# ================= TIME VECTOR =================
t = np.arange(len(x_bp)) / fs


# ================= TIME DOMAIN PLOTS =================
plt.figure(figsize=(12,8))
for i, sig in enumerate([x_bp, y_bp, z_bp], 1):
    plt.subplot(3,1,i)
    plt.plot(t, sig)
    plt.title(f"{['X','Y','Z'][i-1]} Axis (Band-pass)")
plt.xlabel("Time (s)")
plt.tight_layout()
plt.show()


# ================= MAGNITUDE =================
a_mag = np.sqrt(x_bp**2 + y_bp**2 + z_bp**2)

plt.figure(figsize=(12,4))
plt.plot(t, a_mag)
plt.title("Acceleration Magnitude")
plt.xlabel("Time (s)")
plt.grid(True)
plt.show()


# ================= FFT FUNCTION =================
def compute_fft(signal, fs):
    N = len(signal)
    fft_vals = np.fft.rfft(signal)
    fft_mag = np.abs(fft_vals) / N
    freqs = np.fft.rfftfreq(N, 1/fs)
    return freqs, fft_mag


# ================= FREQUENCY DOMAIN =================
fx_hp, X_hp = compute_fft(x_hp, fs)
fx_lp, X_lp = compute_fft(x_lp, fs)
fx_bp, X_bp = compute_fft(x_bp, fs)
fm, M_fft = compute_fft(a_mag, fs)


plt.figure(figsize=(12,10))

plt.subplot(4,1,1)
plt.plot(fx_hp, X_hp)
plt.title("High-Pass Spectrum (X)")
plt.xlim(0, 120)

plt.subplot(4,1,2)
plt.plot(fx_lp, X_lp)
plt.title("Low-Pass Spectrum (X)")
plt.xlim(0, 120)

plt.subplot(4,1,3)
plt.plot(fx_bp, X_bp)
plt.title("Band-Pass Spectrum (X)")
plt.xlim(0, 120)

plt.subplot(4,1,4)
plt.plot(fm, M_fft)
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency (Hz)")
plt.xlim(0, 120)

plt.tight_layout()
plt.show()


# ================= WINDOWED FEATURES =================
window = int(0.5 * fs)
features = []

# Fixed scale for all segment plots
y_min = np.min(a_mag)
y_max = np.max(a_mag)

for i in range(0, len(a_mag) - window + 1, window):

    seg = a_mag[i:i+window]

    rms = np.sqrt(np.mean(seg**2))
    peak = np.max(seg)
    crest = peak / rms
    var = np.var(seg)
    kurt = kurtosis(seg)
    sk = skew(seg)

    features.append([rms, peak, crest, var, kurt, sk])

    plt.figure(figsize=(12,4))
    plt.plot(seg)
    plt.ylim(y_min, y_max)

    text = (
        f"RMS: {rms:.2f}   Peak: {peak:.2f}   Crest: {crest:.2f}\n"
        f"Var: {var:.2f}   Kurt: {kurt:.2f}   Skew: {sk:.2f}"
    )

    plt.text(
        0.02, 0.95, text,
        transform=plt.gca().transAxes,
        fontsize=11,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.8)
    )

    plt.title(f"Segment {i//window + 1}")
    plt.xlabel("Sample")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ================= FEATURE TABLE =================
features_df = pd.DataFrame(
    features,
    columns=["RMS","Peak","Crest_Factor","Variance","Kurtosis","Skewness"]
)

print(features_df)


# ================= FFT FUNCTION =================
def compute_fft(signal, fs):
    N = len(signal)
    fft_vals = np.fft.rfft(signal)
    fft_mag = np.abs(fft_vals) / N
    freqs = np.fft.rfftfreq(N, 1/fs)
    return freqs, fft_mag

# FFT without Filtering
fx_No_fft, X_No_fft = compute_fft(x[start:], fs)
fy_No_fft, Y_No_fft = compute_fft(y[start:], fs)
fz_No_fft, Z_No_fft = compute_fft(z[start:], fs)

# ================= FFTs =================
fx, X_fft = compute_fft(x_bp, fs)
fy, Y_fft = compute_fft(y_bp, fs)
fz, Z_fft = compute_fft(z_bp, fs)


a_mag = np.sqrt(x_bp**2 + y_bp**2 + z_bp**2)
fm, M_fft = compute_fft(a_mag, fs)


# Ignore DC component
idx = np.argmax(M_fft[1:]) + 1

dom_freq = fm[idx]
dom_amp = M_fft[idx]

print("Dominant Frequency:", dom_freq, "Hz")
print("Amplitude:", dom_amp)


# Harmonics

print("\nHarmonics:")

for k in range(2, 6):
    target = k * dom_freq
    if target > fs/2:
        break

    i = np.argmin(np.abs(fm - target))
    print(f"{k}x ({target:.2f} Hz): {M_fft[i]:.4f}")


#Energy Distribution Across Bands

low = fm < 20
mid = (fm >= 20) & (fm < 60)
high = fm >= 60

low_E = np.sum(M_fft[low])
mid_E = np.sum(M_fft[mid])
high_E = np.sum(M_fft[high])

print("\nEnergy Distribution")
print("Low (0–20 Hz):", low_E)
print("Mid (20–60 Hz):", mid_E)
print("High (60–125 Hz):", high_E)


# Changes Across Segments

print("\nSegment-wise Dominant Frequencies")

window = int(0.5 * fs)

for i in range(0, len(a_mag) - window + 1, window):

    seg = a_mag[i:i+window]
    f_seg, F_seg = compute_fft(seg, fs)

    idx = np.argmax(F_seg[1:]) + 1
    print(f"Segment {i//window + 1}: {f_seg[idx]:.2f} Hz")


# Directional Differences (X/Y/Z)

plt.figure(figsize=(12,5))

plt.plot(fx, X_fft, label="X")
plt.plot(fy, Y_fft, label="Y")
plt.plot(fz, Z_fft, label="Z")

plt.title("Axis-wise Frequency Comparison")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.xlim(0, 120)
plt.legend()
plt.grid(True)
plt.show()


# ✔ Identify dominant axis

x_peak = np.max(X_fft)
y_peak = np.max(Y_fft)
z_peak = np.max(Z_fft)

axis_max = max(x_peak, y_peak, z_peak)

if axis_max == x_peak:
    print("Dominant direction: X-axis")
elif axis_max == y_peak:
    print("Dominant direction: Y-axis")
else:
    print("Dominant direction: Z-axis")

# Overall Magnitude Spectrum

plt.figure(figsize=(12,5))
plt.plot(fm, M_fft)
plt.title("Overall Magnitude Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.xlim(0, 120)
plt.grid(True)
plt.show()
