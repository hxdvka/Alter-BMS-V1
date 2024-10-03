// minified code to test sync things on esp8266

//#include <String>
//#include <sys/stat.h>
// Pin definitions
//#define   S2_OUT  6
//#define   S3_OUT  7


#define   Noise_in  A0    // LOW = ENABLED 

//#define   LED     12
#define   BAUDS   57600    // LOW = ENABLED 



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

// clear all characters from the serial input
void clearBuffers()
{
  //Serial.flush();
	while (Serial.available()){
    Serial.read();
  }
}

// changed to output timestamp
void rgbPrintln(){
static int  i = 0;
Serial.println(analogRead(Noise_in));
Serial.println(analogRead(i));
i++;
}



bool readSensor()
{
  //change to flip a coin to be done
  static  bool  waiting;
  if (!waiting)
  {
    waiting = true;
  }
  else
  {
    if ( rand()%25 == 0 ) 
    {      
      waiting = false;
    }
  }
  return waiting;
}


void calibrate(){

  Serial.println("Dunkel");
  clearBuffers();
  getChar();
  delay(500);
  Serial.print("Dunkel values:");
  rgbPrintln();

  Serial.println("Weiss");
  clearBuffers();
  getChar();
  delay(500);
  Serial.print("Weiss values:");
  rgbPrintln();
  Serial.println("done");

}

int menu(){
  //Serial.println("menu, waiting int");
  clearBuffers();
  return getInt();
}

int collectData(int status){
  clearBuffers();
  while(status == 1){
    if(Serial.available()){
      if(Serial.read() == '3'){
            clearBuffers();
            status = 3;}
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
  pinMode(Noise_in, INPUT);
}

void loop() {
  // 0 waiting ; 1 read ; 2 cal ; 3 stop ; 4 clear and back to zero
  
  static short status = 0;
  switch (status){

    case 0: 
      status = menu();
      break;
    case 1: 
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

