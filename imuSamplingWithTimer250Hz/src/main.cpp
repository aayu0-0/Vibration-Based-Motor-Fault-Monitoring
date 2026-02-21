#include <Arduino.h>
#include <Wire.h>
#include "MPU6050.h"
MPU6050 mpu;

/* ===== Hardware Timer Variables ===== */
hw_timer_t *timer = NULL;
volatile bool sampleFlag = false;

/* ===== Sampling frequency ===== */
#define SAMPLE_FREQ 250                  // 250 Hz sampling
#define TIMER_US (1000000 / SAMPLE_FREQ) // period in microseconds (4 ms)

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

void IRAM_ATTR onTimer()
{
  sampleFlag = true;   // tells loop(): take one measurement now
}

void setup()
{
  Serial.begin(921600);

  Wire.begin(21, 22);
  Wire.setClock(400000);   // 400 kHz I2C

  mpu.initialize();

    /* ===== Timer Setup ===== */
  timer = timerBegin(0, 80, true);  
  // 80 prescaler → 1 timer tick = 1 microsecond

  timerAttachInterrupt(timer, &onTimer, true);

  timerAlarmWrite(timer, TIMER_US, true);
  // fires every 2000 µs (250 Hz)

  timerAlarmEnable(timer);
}

void loop()
{
  if (!sampleFlag)
    return;

  sampleFlag = false;

    mpu.getMotion6(&ax_raw, &ay_raw, &az_raw,
                 &gx_raw, &gy_raw, &gz_raw);

  ax = (ax_raw / 16384.0f) * 9.81f;
  ay = (ay_raw / 16384.0f) * 9.81f;
  az = (az_raw / 16384.0f) * 9.81f;

  gx = (gx_raw / 131.0f) * DEG_TO_RAD;
  gy = (gy_raw / 131.0f) * DEG_TO_RAD;
  gz = (gz_raw / 131.0f) * DEG_TO_RAD;

  float roll_acc  = atan2f(ay, az);
  float pitch_acc = atan2f(-ax, sqrtf(ay * ay + az * az));

  roll  = alpha * (roll  + gx * (1.0f / SAMPLE_FREQ)) + (1.0f - alpha) * roll_acc;
  pitch = alpha * (pitch + gy * (1.0f / SAMPLE_FREQ)) + (1.0f - alpha) * pitch_acc;

  float g_x = -9.81f * sinf(pitch);
  float g_y =  9.81f * sinf(roll) * cosf(pitch);
  float g_z =  9.81f * cosf(roll) * cosf(pitch);

  ax_lin = ax - g_x;
  ay_lin = ay - g_y;
  az_lin = az - g_z;

  Serial.print(ax_lin, 6);
  Serial.print(",");
  Serial.print(ay_lin, 6);
  Serial.print(",");
  Serial.println(az_lin, 6);
}
