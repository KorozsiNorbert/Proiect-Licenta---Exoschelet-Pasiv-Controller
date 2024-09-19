const int potPins[] = {A0, A1, A2, A3, A4};
const int numPots = 5;
int potValues[numPots];

void setup() {
  Serial.begin(9600);    // Initialize serial communication at 9600 bps
  for(int i=0; i<numPots;i++){
    pinMode(potPins[i], INPUT);
  }
}

void loop() {
 for(int i = 0; i< numPots; i++){
    int sensorValue = analogRead(potPins[i]);
    if(i == 0){
      sensorValue = map(sensorValue, 90 , 800 , 0 , 180);
      potValues[i] = sensorValue;
    };
    if (i == 3) {
      sensorValue = map(sensorValue, 400 , 900 , 0 , 180);
      potValues[i] = sensorValue;
    };
    if (i == 4) {
      sensorValue = map(sensorValue, 10 , 600 , 0 , 180);
      potValues[i] = sensorValue;
    };
 }
 for(int i = 0; i< numPots; i++){
    
    Serial.print(potValues[i]);
    Serial.print(" ");
 }
 Serial.println();

 delay(100);
}
