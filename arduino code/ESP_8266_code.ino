#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <FS.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

//MUX Link: https://github.com/witnessmenow/ESP8266-4051-Multiplexer-Example/blob/master/Esp8266_4051_Multiplexer.ino 
#define MUX_A D4
#define MUX_B D3
#define MUX_C D2
#define ANALOG_INPUT A0

// GPS
TinyGPSPlus gps;
SoftwareSerial SerialGPS(12, 13); //Rx, Tx (D6, D7)
float Latitude, Longitude;  
String LatitudeString, LongitudeString, velocityString;
float velocity;
float velocitymph;

ESP8266WebServer server(80);

String GPS_DATA = "";
String heartRateData = "";
String temperatureData = "";
String emgData = "";

unsigned long lastUpdateTime = 0;
const int updateInterval = 10; // Update data every 1000 milliseconds (1 second)

void changeMux(int c, int b, int a) {
  digitalWrite(MUX_A, a);
  digitalWrite(MUX_B, b);
  digitalWrite(MUX_C, c);
}

void resetData() {
  heartRateData = "";
  temperatureData = "";
  GPS_DATA = "";
  emgData = "";
}

void updateData() {
  float heartRateValue;
  float temperatureValue;
  String emgValue;

  // Switch to heart rate sensor (Option 1 pin of Mux) 3 from nub right
  changeMux(LOW, LOW, HIGH);
  heartRateValue = analogRead(ANALOG_INPUT);
  heartRateData += String(millis()) + "," + String(heartRateValue) + "\n";

  // Switch to temperature sensor (Option 0 pin of Mux)
  changeMux(LOW, LOW, LOW);
  temperatureValue = analogRead(ANALOG_INPUT);
  float millivolts = (temperatureValue / 1024.0) * 3300; // Convert ADC reading to millivolts
  float temperatureC = millivolts / 10; // LM35 outputs 10mV per degree Celsius
  temperatureData += String(millis()) + "," + String(temperatureC) + "\n";


//GPS
  while (SerialGPS.available() > 0)
    if (gps.encode(SerialGPS.read()))
    {
      if (gps.location.isValid())
      {
        Latitude = gps.location.lat();
        LatitudeString = String(Latitude , 6);
        Longitude = gps.location.lng();
        LongitudeString = String(Longitude , 6);
        velocity = gps.speed.kmph();
        //velocitymph = velocity/1000;
        velocityString = String(velocity , 6); 
        GPS_DATA += String(millis()) + "," + LatitudeString + "," + LongitudeString + "," + velocityString + "\n";
        Serial.println(velocity);
      } 
  }

  // Read EMG data
  if (Serial.available() > 0) {
    emgValue = Serial.readStringUntil('\n');
    emgData += String(millis()) + "," + emgValue + "\n"; 
  }
}


void handleRoot() {
  server.send(200, "text/html", "<html><body><h1>ESP8266 Data Recording</h1><p><a href='/heart_rate'>Heart Rate Data</a></p><p><a href='/temperature'>Temperature Data</a></p><p><a href='/gps_data'>GPS Data</a></p><p><a href='/emg_data'>EMG Data</a></p></body></html>");
}

void handleHeartRate() {
  // Send response to client
  server.sendHeader("Content-Disposition", "attachment; filename=heart_rate.csv");
  server.send(200, "text/csv", heartRateData);
  heartRateData = "";
}

void handleTemperature() {
  // Send response to client
  server.sendHeader("Content-Disposition", "attachment; filename=temperature.csv");
  server.send(200, "text/csv", temperatureData);
  temperatureData = "";
}

void handleGPSData() {
  // Send response to client
  server.sendHeader("Content-Disposition", "attachment; filename=gps_data.csv");
  server.send(200, "text/csv", GPS_DATA);
  GPS_DATA = "";
}

void handleEMGData() {
  // Send response to client
  server.sendHeader("Content-Disposition", "attachment; filename=emg_data.csv");
  server.send(200, "text/csv", emgData);
  emgData = "";
}

void setup() {
  Serial.begin(9600);
  SerialGPS.begin(9600);

  // Initialize SPIFFS
  if (!SPIFFS.begin()) {
    Serial.println("Failed to mount file system");
    return;
  }

  // Define output pins for Mux
  pinMode(MUX_A, OUTPUT);
  pinMode(MUX_B, OUTPUT);
  pinMode(MUX_C, OUTPUT);

  // Connect to Wi-Fi
    WiFi.begin("fdr_3terms", "hhhhhhhh"); //hhhhhhhh, fdr_3terms, testing321, Samsung Galaxy S10, Jennifer's iPhone (2), uayfwe4foizxy, EJB-i11, Pop-96325
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  // Print the IP address
  Serial.println("WiFi connected");
  Serial.println("IP address: " + WiFi.localIP().toString());

  // Define web server routes
  server.on("/", HTTP_GET, handleRoot);
  server.on("/heart_rate", HTTP_GET, handleHeartRate);
  server.on("/temperature", HTTP_GET, handleTemperature);
  server.on("/gps_data", HTTP_GET, handleGPSData); 
  server.on("/emg_data", HTTP_GET, handleEMGData); 

  // Start server
  server.begin();
}

void loop() {
  server.handleClient();

  // Periodically update data
  if (millis() - lastUpdateTime >= updateInterval) {
    updateData();
    lastUpdateTime = millis();
  }

  // You can add other non-blocking code here if needed
}
