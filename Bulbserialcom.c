//This code is part of serial communication betwwen your esp32 and Python Script,upload it into esp32

const int whiteRelay = 5;   // White bulb
const int greenRelay = 18;  // Green bulb
const int orangeRelay = 19;  // Orange bulb

void setup() {
  Serial.begin(9600);
  
  pinMode(whiteRelay, OUTPUT);
  pinMode(greenRelay, OUTPUT);
  pinMode(orangeRelay, OUTPUT);

  // Initialize with all lights OFF (relays HIGH)
  digitalWrite(whiteRelay, HIGH);
  digitalWrite(greenRelay, HIGH);
  digitalWrite(orangeRelay, HIGH);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n'); // Read until newline
    
    if (command == "white_on") {
      digitalWrite(whiteRelay, LOW);  // Turn white light ON (relay LOW)
      Serial.println("White bulb ON");
    } else if (command == "white_off") {
      digitalWrite(whiteRelay, HIGH);  // Turn white light OFF (relay HIGH)
      Serial.println("White bulb OFF");
    } else if (command == "green_on") {
      digitalWrite(greenRelay, LOW);  // Turn green light ON (relay LOW)
      Serial.println("Green bulb ON");
    } else if (command == "green_off") {
      digitalWrite(greenRelay, HIGH);  // Turn green light OFF (relay HIGH)
      Serial.println("Green bulb OFF");
    } else if (command == "orange_on") {
      digitalWrite(orangeRelay, LOW);  // Turn orange light ON (relay LOW)
      Serial.println("Orange bulb ON");
    } else if (command == "orange_off") {
      digitalWrite(orangeRelay, HIGH);  // Turn orange light OFF (relay HIGH)
      Serial.println("Orange bulb OFF");
    } else if (command == "all_on") {
      digitalWrite(whiteRelay, LOW);  // Turn all lights ON (relays LOW)
      digitalWrite(greenRelay, LOW);
      digitalWrite(orangeRelay, LOW);
      Serial.println("All bulbs ON");
    } else if (command == "all_off") {
      digitalWrite(whiteRelay, HIGH);  // Turn all lights OFF (relays HIGH)
      digitalWrite(greenRelay, HIGH);
      digitalWrite(orangeRelay, HIGH);
      Serial.println("All bulbs OFF");
    } else {
      Serial.println("Invalid command");
    }
  }
}
