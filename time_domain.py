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

# ================= BAND-PASS SIGNAL =================
x_bp = lowpass(highpass(x, 5, fs), 80, fs)[start:]
y_bp = lowpass(highpass(y, 5, fs), 80, fs)[start:]
z_bp = lowpass(highpass(z, 5, fs), 80, fs)[start:]

t = np.arange(len(x_bp)) / fs

# ================= AXIS PLOTS =================
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

# ================= WINDOWED FEATURES =================
window = int(0.5 * fs)
y_min, y_max = np.min(a_mag), np.max(a_mag)

features = []

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
        f"RMS: {rms:.2f}  Peak: {peak:.2f}  Crest: {crest:.2f}\n"
        f"Var: {var:.2f}  Kurt: {kurt:.2f}  Skew: {sk:.2f}"
    )

    plt.text(
        0.02, 0.95, text,
        transform=plt.gca().transAxes,
        fontsize=11,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.8)
    )

    plt.title(f"Segment {i//window + 1}")
    plt.grid(True)
    plt.show()

features_df = pd.DataFrame(
    features,
    columns=["RMS","Peak","Crest","Variance","Kurtosis","Skewness"]
)

print(features_df)