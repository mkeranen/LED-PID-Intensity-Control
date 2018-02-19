/*
 * LED emitted intensity control
 * By: Mark Keranen
 * 
 * This program uses an LED controlled via PWM & a photodiode for measuring the intensity of light emitted by the LED. 
 * The user can input a desired intensity via serial communication, and the LED duty cycle will be adjusted to create 
 * the desired intensity reading at the photodiode.
 *
 * This program utilizes a PID loop control system with empirically adjusted, but un-tuned PID parameters.
 *
 */

 //PID Library
#include <PID_v1.h>
//----------------------------------------------------------------------------------------------------
////Function: takes in desired LED control intensity, writes that value to Pin 3 via PWM (AnalogWrite)
void ledON(int intensity){
  digitalWrite(13, 1);
  analogWrite(3, intensity);
}
////----------------------------------------------------------------------------------------------------
//Function: Turns off LEDs (Currently not used, can be implemented if led should blink)
void ledOFF(void){
  digitalWrite(13, 0);
  digitalWrite(3, 0);
}
//----------------------------------------------------------------------------------------------------
//Function: Reads in emitted LED intensity via photodiode, returns measured intensity
double getLightIntensity(void){
  int i;
  const int n = 20; //Number of elements to average
  int intensityArray[n];
  float sum = 0, avgIntensity = 0;

  //Build array of n elements to smooth out analog reading
  for (i=0; i<n; i++){
    intensityArray[i] = analogRead(A0);
    
    }

  //Sum array in preparation for reporting avg
  for (i=0; i<n; i++){
    sum += intensityArray[i];
    }

  //Report average intensity of all elements in array
  avgIntensity = sum / n;
  
  return avgIntensity;
}
//----------------------------------------------------------------------------------------------------
//Function: Checks serial input for user defined desired actual intensity, maintain desired 
//intensity even when there is no input to serial
double getDesiredIntensity(double desiredInt){
  
  if (Serial.read() == -1){
    desiredInt = desiredInt;
    return desiredInt;
  }
  else{
      desiredInt = Serial.parseInt();
      return desiredInt;
  }
}
//----------------------------------------------------------------------------------------------------
//Variable initializations
double measuredIntensity = 0;     //Input: Actual intensity value measured by A0
double desiredIntensity = 120;    //Setpoint: The initialization of this can be changed, or its value can be changed in use by user via serial input
double ledIntensity = 255;        //Output: Intesity value written to PWM pin controlling LED, initialized high
double Kp = 0, Ki = .5, Kd = 0;   //PID Parameters: Not tuned, could be improved, but oscillations are minimal here

double smoothIntensity = 0;       //Smoothed measuredIntensity
PID myPID(&smoothIntensity, &ledIntensity, &desiredIntensity, Kp, Ki, Kd, DIRECT);
//----------------------------------------------------------------------------------------------------
//Setup Pinmodes, serial monitor
void setup() {

  pinMode(A0, INPUT);
  pinMode(13, OUTPUT);
  pinMode(3, OUTPUT);
  Serial.begin(9600);
  myPID.SetMode(AUTOMATIC);
  myPID.SetTunings(Kp, Ki, Kd);
}
//----------------------------------------------------------------------------------------------------

void loop() {

  //Get desired intensity value from user
  desiredIntensity = getDesiredIntensity(desiredIntensity);
    
  //LED Control & Intensity Aqcuisition
  ledON(ledIntensity);

  //Get light intensity measured by Photodiode
  measuredIntensity = getLightIntensity();
  //Smoothing
  smoothIntensity += (measuredIntensity - smoothIntensity) * 0.5;

  //Calculate next output
  myPID.Compute();

  //Output CSV format for ease of plotting etc.
  Serial.print(smoothIntensity);
  Serial.print(",");
  Serial.print(desiredIntensity);
  Serial.print(",");
  Serial.println(ledIntensity);
  delay(500);
  }
