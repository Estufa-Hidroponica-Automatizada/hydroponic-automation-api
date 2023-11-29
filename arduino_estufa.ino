#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
#include <ph4502c_sensor.h>

#define POWERPIN 4
#define DHTPIN 3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

OneWire oneWire(2);
DallasTemperature sensors(&oneWire);

const int TDS_SENSOR_PIN = A3;
const int LIGHT_SENSOR_PIN = A2;

const int PH4502C_TEMPERATURE_PIN = A1;
const int PH4502C_PH_PIN = A0;

PH4502C_Sensor ph4502c(PH4502C_PH_PIN, PH4502C_TEMPERATURE_PIN);

void setup() {
    Serial.begin(9600);
    pinMode(POWERPIN, OUTPUT);
    digitalWrite(POWERPIN, HIGH);

    sensors.begin();
    ph4502c.init();
    dht.begin();
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        if (command == 'R') {
            // Read DHT22 sensor values
            float temperatureDHT = dht.readTemperature();
            float humidityDHT = dht.readHumidity();

            // Check if any reads failed and exit early (to try again).
            if (isnan(temperatureDHT) || isnan(humidityDHT)) {
              digitalWrite(POWERPIN, LOW);
              delay(2000);
              digitalWrite(POWERPIN, HIGH);
              delay(2000);
              float temperatureDHT = dht.readTemperature();
              float humidityDHT = dht.readHumidity();
            }

            // Read DS18B20 sensor value
            sensors.requestTemperatures();
            float temperatureDS18B20 = sensors.getTempCByIndex(0);

            // Read TDS sensor value
            int tdsValue = analogRead(TDS_SENSOR_PIN);

            // Read light sensor value
            int lightValue = analogRead(LIGHT_SENSOR_PIN);

            // Read pH sensor value
            float pHLevel = ph4502c.read_ph_level();

            // Print sensor values on serial output
            Serial.print(lightValue);
            Serial.print(",");
            Serial.print(temperatureDS18B20);
            Serial.print(",");
            Serial.print(tdsValue);
            Serial.print(",");
            Serial.print(pHLevel);
            Serial.print(",");
            Serial.print(temperatureDHT);
            Serial.print(",");
            Serial.println(humidityDHT);
        }
    }
}
