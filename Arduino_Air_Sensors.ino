/* 
Notes for the Grove Gas Sensor
GM102B = Nitrogen Dioxide
GM302B = Alcohol Gas
GM502B = VOC 
GM702B = Carbon Monoxide


*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
#include <Adafruit_SHT4x.h>
#include <Multichannel_Gas_GMXXX.h>

#ifdef SOFTWAREWIRE
    #include <SoftwareWire.h>
    SoftwareWire myWire(3, 2);
    GAS_GMXXX<SoftwareWire> gas;
#else
    #include <Wire.h>
    GAS_GMXXX<TwoWire> gas;
#endif

static uint8_t recv_cmd[8] = {};

// Create an instance of the sensor
Adafruit_BME680 bme;
Adafruit_SHT4x sht4 = Adafruit_SHT4x();

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Initialize the BME
  if (!bme.begin()) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1);
  }

  // initalize the SHT45
  if (!sht4.begin()) {
    Serial.println("Could not find a valid SHT45 sensor, check wiring!");
    while (1);

  }

  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms

  // Initialize the Grove Multichannel Gas Sensor with default I2C address
  gas.begin(Wire, 0x08);
}

void loop() {
  // Perform a reading for BME
  if (!bme.performReading()) {
    Serial.println("Failed to perform reading :(");
    return;
  }

  // perfrom a reading for SHT
  sensors_event_t humidity, temp;
  sht4.getEvent(&humidity, &temp); // populate temp and humidity objects with fresh data

  // Get sensor data
  float bme_temperature = bme.temperature;
  float bme_pressure = bme.pressure / 100.0;
  float bme_humidity = bme.humidity;
  float bme_gas_resistance = bme.gas_resistance / 1000.0;

  float sht_temperature = temp.temperature;
  float sht_humidity = humidity.relative_humidity;

  uint32_t gm102b = gas.getGM102B();
  uint32_t gm302b = gas.getGM302B();
  uint32_t gm502b = gas.getGM502B();
  uint32_t gm702b = gas.getGM702B();
  uint32_t gmtest = gas.measure_NO2();

  // Print BME680 sensor data
  // temp = C, press = hPa, hum = %, gas = KOhms
  Serial.print("BME680 Sensor TPHG:");
  Serial.print(bme_temperature);
  Serial.print(",");
  Serial.print(bme_pressure);
  Serial.print(",");
  Serial.print(bme_humidity);
  Serial.print(",");
  Serial.println(bme_gas_resistance);

  // Print SHT4x sensor data
  Serial.print("SHT4x Sensor TH:");
  Serial.print(sht_temperature);
  Serial.print(",");
  Serial.println(sht_humidity);
  
  // Print Grove Multichannel Gas Sensor data
  // PPM, V, in order : nitrogen dioxide, Alcohol Gas, VOC, Carbon Monoxide
  Serial.print("Grove Multichannel Gas Sensor:");
  Serial.print(gm102b);
  Serial.print(",");
  Serial.print(gas.calcVol(gm102b));
  Serial.print(",");
  Serial.print(gm302b);
  Serial.print(",");
  Serial.print(gas.calcVol(gm302b));
  Serial.print(",");
  Serial.print(gm502b);
  Serial.print(",");
  Serial.print(gas.calcVol(gm502b));
  Serial.print(",");
  Serial.print(gm702b);
  Serial.print(",");
  Serial.println(gas.calcVol(gm702b));
  Serial.println();
  Serial.print("Test NO2 :");
  Serial.print(gmtest);
  delay(5000); // Wait for 5 seconds before the next loop
}