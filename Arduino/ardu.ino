#include <AFMotor.h>
#include <Servo.h>
 
AF_DCMotor motor2(2);
AF_DCMotor motor1(1);
bool st =false;
bool dr=false;
bool stanga =false;
bool dreapta =false;
// defines variables
long duration;
int distance;
 
void setup()
{
 Serial.begin(9600);
 Serial.setTimeout(1);     
  motor1.setSpeed(100);
  motor2.setSpeed(100);
 
  pinMode(A0,OUTPUT); //TRIG#include <Wire.h> 
 
 
pinMode(A1,INPUT); // ECHO
 
  motor1.run(RELEASE);
  motor2.run(RELEASE);
}
 
void exec()
{
  if(stanga && dreapta)
  {
    motor1.run(BACKWARD);
    motor2.run(FORWARD);
    Serial.println("INAINTE");
 
    return;
  }
 
  if(stanga&& !st)
  {
    st=true;
    dr=false;
    motor1.run(BACKWARD);
    motor2.run(BACKWARD);
 
    Serial.println("STANGA");
    return;
  }
 
  if(dreapta && !dr)
  {
    st=false;
    dr=true;
  motor1.run(FORWARD);
  motor2.run(FORWARD);
 
  Serial.println("DREAPTA");
  return;
  }
 
  if(!stanga && !dreapta)
  {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  return;
  }
}
void loop()
{
  int dissum=0;
  for(int i=0;i<100;i++)
  {
  digitalWrite(A0,LOW);
  delayMicroseconds(2);
  digitalWrite(A0,HIGH);
  delayMicroseconds(10);
  digitalWrite(A0,LOW);
  duration = pulseIn(A1,HIGH);
  distance = duration * 0.034/2;
  dissum=dissum+distance;
  }
  dissum=dissum/100;
 
 
  if(Serial.available() > 0)
  {
    String data = Serial.readStringUntil('\n');
    if(data.compareTo("GO")==0 && dissum>30)
      {stanga= true; dreapta=true;}
      else
        if(data.compareTo("STOP")==0)
        {stanga = false; dreapta=false;}
        else
          if(data.compareTo("LEFT")==0)
          {stanga = true; dreapta = false;}
          else
            if(data.compareTo("RIGHT")==0)
            {stanga = false; dreapta = true;}
 
    exec();
    Serial.println(data);
    delay(300);
    motor1.run(RELEASE);
  motor2.run(RELEASE);
  }
 
 
}
