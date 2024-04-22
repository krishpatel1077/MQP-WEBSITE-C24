int analogSensor1;
int analogSensor2;
int analogSensor3;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);  
}
void loop() {
  analogSensor1 = analogRead(A3);
  analogSensor2 = analogRead(A2);
  analogSensor3 = analogRead(A1);

  Serial.println(analogSensor3); //A1 Hamstring
  Serial.print(",");
  Serial.print(analogSensor1); //A3 Calf
  Serial.print(",");  
  Serial.print(analogSensor2); //A2 Quad
  Serial.println();
  delay(15);
}