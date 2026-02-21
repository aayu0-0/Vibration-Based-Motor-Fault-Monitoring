import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.stats import kurtosis, skew


data = pd.read_csv("SP1_data.csv")
x, y, z = data.iloc[:, 1], data.iloc[:, 2], data.iloc[:, 3]

fs = 250
start = int(4.26 * fs)

def highpass(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)

def lowpass(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)


x_filtered = lowpass(highpass(x, 5, fs), 80, fs)
y_filtered = lowpass(highpass(y, 5, fs), 80, fs)
z_filtered = lowpass(highpass(z, 5, fs), 80, fs)


x_f = x_filtered[start:]
y_f = y_filtered[start:]
z_f = z_filtered[start:]


t = np.arange(len(x_f)) / fs


plt.figure(figsize=(12,8))
for i, sig in enumerate([x_f, y_f, z_f], 1):
    plt.subplot(3,1,i)
    plt.plot(t, sig)
    plt.title(f"{['X','Y','Z'][i-1]} Axis")
plt.xlabel("Time (s)")
plt.tight_layout()
plt.show()

a_mag = np.sqrt(x_f**2 + y_f**2 + z_f**2)

plt.figure(figsize=(12,4))
plt.plot(t, a_mag)
plt.title("Acceleration Magnitude")
plt.xlabel("Time (s)")
plt.grid(True)
plt.show()


window = int(0.5 * fs)
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


features_df = pd.DataFrame(
    features,
    columns=["RMS","Peak","Crest_Factor","Variance","Kurtosis","Skewness"]
)

print(features_df)
