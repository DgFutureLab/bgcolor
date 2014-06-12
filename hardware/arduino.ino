const int buttonPin = 2;

int buttonState = 0;
int counter = 0;
boolean pressed = false;
void setup(){
   Serial.begin(9600);
}

void loop(){
    Serial.println(analogRead(buttonPin));
    delay(100);
//   buttonState = digitalRead(buttonPin);
//   Serial.println(buttonState);

//  
//  if (buttonState == HIGH){
//    counter += 1;
//    Serial.println("Good boy!");
//    while (buttonState == HIGH){
//    }
//
//  }
//   if (buttonState == LOW){
//    Serial.println("Press the button, damnit!");
//    while (buttonState == LOW){
//    }
//  }
//  delay(100);
  
}
