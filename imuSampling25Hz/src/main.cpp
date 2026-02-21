

#include <Arduino.h>
#include <Wire.h>
#include "MPU6050.h"

MPU6050 mpu;

/* ===== Sampling Configuration ===== */
const unsigned long SAMPLE_PERIOD_US = 40000;   // 500 Hz
unsigned long lastMicros = 0;

/* ===== Raw Sensor ===== */
int16_t ax_raw, ay_raw, az_raw;
int16_t gx_raw, gy_raw, gz_raw;

/* ===== Physical Values ===== */
float ax, ay, az;
float gx, gy, gz;

/* ===== Orientation ===== */
float roll = 0.0f, pitch = 0.0f;
const float alpha = 0.98f;

/* ===== Linear Acceleration ===== */
float ax_lin, ay_lin, az_lin;

/* ===== Time ===== */
unsigned long sampleIndex = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

  mpu.initialize();

  lastMicros = micros();
}

void loop() {

  unsigned long now = micros();

  if (now - lastMicros < SAMPLE_PERIOD_US)
    return;

  float dt = (now - lastMicros) * 1e-6f;
  lastMicros = now;

  /* ===== Read MPU6050 ===== */
  mpu.getMotion6(&ax_raw, &ay_raw, &az_raw,
                 &gx_raw, &gy_raw, &gz_raw);

  /* ===== Convert Units ===== */
  ax = (ax_raw / 16384.0f) * 9.81f;
  ay = (ay_raw / 16384.0f) * 9.81f;
  az = (az_raw / 16384.0f) * 9.81f;

  gx = (gx_raw / 131.0f) * DEG_TO_RAD;
  gy = (gy_raw / 131.0f) * DEG_TO_RAD;
  gz = (gz_raw / 131.0f) * DEG_TO_RAD;

  /* ===== Accelerometer Angles ===== */
  float roll_acc  = atan2f(ay, az);
  float pitch_acc = atan2f(-ax, sqrtf(ay * ay + az * az));

  /* ===== Complementary Filter ===== */
  roll  = alpha * (roll  + gx * dt) + (1.0f - alpha) * roll_acc;
  pitch = alpha * (pitch + gy * dt) + (1.0f - alpha) * pitch_acc;

  /* ===== Gravity Vector ===== */
  float g_x = -9.81f * sinf(pitch);
  float g_y =  9.81f * sinf(roll) * cosf(pitch);
  float g_z =  9.81f * cosf(roll) * cosf(pitch);

  /* ===== Linear Acceleration ===== */
  ax_lin = ax - g_x;
  ay_lin = ay - g_y;
  az_lin = az - g_z;

  /* ===== Timestamp ===== */
  float timeSec = sampleIndex * (SAMPLE_PERIOD_US / 1000000.0f);
  sampleIndex++;

  /* ===== CSV Serial Output ===== */
  Serial.print(timeSec, 6);
  Serial.print(",");
  Serial.print(ax_lin, 6);
  Serial.print(",");
  Serial.print(ay_lin, 6);
  Serial.print(",");
  Serial.println(az_lin, 6);
  delay(40);   // small delay to allow Serial transmission
}