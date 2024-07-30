int greenLight = 0;
int blueLight = 3;
int redLight = 4;
int yellowLight = 5;

void setup() {
  pinMode(greenLight, OUTPUT);
  pinMode(blueLight, OUTPUT);
  pinMode(redLight, OUTPUT);
  pinMode(yellowLight, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch (command) {
      case '1':
        digitalWrite(greenLight, HIGH);
        break;
      case '2':
        digitalWrite(greenLight, LOW);
        break;
      case '3':
        digitalWrite(blueLight, HIGH);
        break;
      case '4':
        digitalWrite(blueLight, LOW);
        break;
      case '5':
        digitalWrite(redLight, HIGH);
        break;
      case '6':
        digitalWrite(redLight, LOW);
        break;
      case '7':
        digitalWrite(yellowLight, HIGH);
        break;
      case '8':
        digitalWrite(yellowLight, LOW);
        break;
      case '9':
        digitalWrite(greenLight, HIGH);
        digitalWrite(blueLight, HIGH);
        digitalWrite(redLight, HIGH);
        digitalWrite(yellowLight, HIGH);
        break;
      case '10':
        digitalWrite(greenLight, LOW);
        digitalWrite(blueLight, LOW);
        digitalWrite(redLight, LOW);
        digitalWrite(yellowLight, LOW);
        break;
    }
  }
}
