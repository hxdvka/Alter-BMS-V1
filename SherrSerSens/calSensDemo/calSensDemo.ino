#include <MD_TCS230.h>
#include <FreqCount.h>
//#include <String>
//#include <sys/stat.h>
// Pin definitions
#define   S2_OUT  6
#define   S3_OUT  7
#define   OE_OUT  8    // LOW = ENABLED 

//#define   LED     12
#define   BAUDS   57600    // LOW = ENABLED 


MD_TCS230	CS(S2_OUT, S3_OUT, OE_OUT);



//move this to utils xx
// blocking wait for an input character from the input stream
String getChar()
{ 
  Serial.println("req_in");
	while (Serial.available() == 0);
	return(Serial.readString()); // why bother tho___?¡
}

int getInt()
{ 
  clearBuffers();
  Serial.println("req_in");
	while (Serial.available() == 0);
	return(Serial.parseInt());
}

// clear all characters from the serial input/output
void clearBuffers()
{
  //Serial.flush();
	while (Serial.available()){
    Serial.read();
  }
}

void rgbPrintln(){
colorData rgb;
sensorData sd;
CS.getRGB(&rgb);
CS.getRaw(&sd);
String str_out ="";
//QUIERO AGREGAR EL SENSOR BLANCO BTW y esto deberia ser una fstring(?) spätter mebby
str_out +=  String(rgb.value[TCS230_RGB_R]) +   ","
        +   String(rgb.value[TCS230_RGB_G]) +   ","
        +   String(rgb.value[TCS230_RGB_B]) +   ","
        +   String(sd.value[TCS230_RGB_R])  +   ","
        +   String(sd.value[TCS230_RGB_G])  +   ","
        +   String(sd.value[TCS230_RGB_B]);
Serial.println(str_out);
}


bool readSensor()
{
  static  bool  waiting;
  if (!waiting)
  {
    CS.read();
    waiting = true;
  }
  else
  {
    if (CS.available()) 
    {      
      waiting = false;
    }
  }
  return waiting;
}

void dark(){
  sensorData sd;
  while(readSensor());
  CS.getRaw(&sd);	
  CS.setDarkCal(&sd);
}

void white(){
  sensorData sd;
  while(readSensor());
  CS.getRaw(&sd);	
  CS.setWhiteCal(&sd);
}

void calibrate(){

  Serial.println("Dunkel");
  getChar();
  clearBuffers();
  dark();
  Serial.print("Dunkel values:");
  rgbPrintln();

  Serial.println("Weiss");
  getChar();
  clearBuffers();
  white();
  Serial.print("Weiss values:");
  rgbPrintln();
  Serial.println("done");

}

int menu(){
  //Serial.println("menu, waiting int");
  return getInt();
}

int collectData(int status){
  while(status == 1){
    if(Serial.available()){
      //Serial.println(Serial.read());
      status = 3;
    }
    while(readSensor());
    rgbPrintln();  
  }
  return status;
}

int stop(){
  clearBuffers();
  Serial.println("done");
  return 0;
}

int reset(){
  Serial.println("why tf are we here__?");
  return 0;
}

void setup() {
  // put your setup code here, to run once:

  Serial.begin(BAUDS);
  clearBuffers();	//  pinMode(LED , OUTPUT);
  CS.begin();
}

void loop() {
  // 0 waiting ; 1 read ; 2 cal ; 3 stop ; 4 clear and back to zero
  
  static short status = 0;
  Serial.print("stat post : ");
  Serial.println(status);

  switch (status){

    case 0: 
      status = menu();
      clearBuffers();
      break;
    case 1: 
      clearBuffers();
      status = collectData(status);
      break;
    case 2: 
      calibrate();
      status = 0;
      break;
    case 3: 
      status = stop();
      break;
    case 4: 
      status = reset();
      break;
  }
  //sensorData sd;

}

