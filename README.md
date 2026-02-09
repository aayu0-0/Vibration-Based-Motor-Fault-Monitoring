Motor Fault Detection via Vibration Monitoring
📌 Overview

This project focuses on detecting faults in electric motors and motor-driven systems using vibration monitoring. Sensor data is acquired from the motor, processed to extract meaningful features, and analyzed to identify different types of mechanical and electrical faults. The system is designed with real-time monitoring, wireless data transmission, and signal processing in mind.

The goal is to build a scalable and practical condition monitoring system that can be extended to industrial applications.

🎯 Objectives

Acquire raw vibration and sensor data from a running motor

Analyze vibration patterns corresponding to different faults

Detect and classify motor faults using signal processing techniques

Transmit sensor data wirelessly over long range (~100 m)

Reduce data size using compression techniques

Visualize signals and fault signatures on a PC

🧠 Faults Considered

Bearing Fault

Rotor Imbalance

Shaft Bending

Mechanical Overload

Electrical Faults

Loose Components

🛠 Sensors Used

Accelerometer (Vibration Analysis)

Temperature Sensor

Strain Sensor

Current / Voltage Sensor

Microphone (Acoustic Analysis)

Hall Effect Sensor

🧩 System Architecture

Data Acquisition
Sensors collect raw signals from the motor in real time.

Embedded Processing
Microcontroller samples, preprocesses, and formats the data.

Wireless Transmission
Sensor data is transmitted wirelessly to a remote system.

Signal Processing & Analysis
Time-domain and frequency-domain techniques are applied to detect faults.

Visualization
Processed data is visualized using Python / MATLAB on a PC.

📊 Signal Processing Techniques

Time-domain analysis (RMS, Peak, Kurtosis)

Frequency-domain analysis (FFT)

Band-pass filtering

Envelope detection (for bearing faults)

Feature extraction for fault identification

🧪 Project Phases

Phase 1:

Sensor setup

Raw signal acquisition

Data visualization

Phase 2:

Signal processing

Fault feature extraction

Phase 3:

Wireless transmission

Data compression

Fault classification

💻 Tech Stack

Programming: C/C++, Python

Embedded Platform: ESP32 / ESP8266

Tools: MATLAB / Python (NumPy, SciPy, Matplotlib)

Communication: Wireless (ESP-based)