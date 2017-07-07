# LED-PID-Intensity-Control


LED emitted intensity control by Mark Keranen
This program uses an LED controlled via PWM & a photodiode for measuring the intensity of light emitted by the LED. The user can 
input a desired intensity via serial communication, and the LED duty cycle will be adjusted to create the desired intensity reading at the photodiode. This program utilizes a PID loop control system with empirically adjusted, but un-tuned PID parameters.
