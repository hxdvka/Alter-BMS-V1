#TODO :optional set/change path, port and baudrate

import asyncio
import serial
import  queue

import csv
import random
"""
TODO :: change this to dict or enum and std thing
Serial Codes:
req_in      := requesting input
done        := signals a process has completed (i.e. calibration), clear event after completion

"""
outF_name = "testfile_m"
outF_path = "./"
SERIAL_PORT = "COMX"
TEST_MODE = 1
CSV_Header = "testme"

class DataCollector:
    def __init__(self, serial_port):
        if (not TEST_MODE):
            self.ser = serial.Serial(serial_port, baudrate=57600, timeout=1)
        self.stop_event = asyncio.Event()  # Event to signal data collection stop
        self.done_event = asyncio.Event()
        self.outF_count = 0
        self.data = queue.deque()


    async def collect_data(self):        
        self.stop_event.clear()
        self.data.append(CSV_Header)
        while not self.stop_event.is_set():
            try:
                ser_read = [random.randint(0,22550)*6] if TEST_MODE else self.ser.readline().decode().strip()
                self.data.append(ser_read)
                #store read on dequeue
            except Exception as e:
                data.append(f"Error reading data: {e}")
                print(f"Error reading data: {e}")
            if TEST_MODE:
                await asyncio.sleep(1) 
     

    async def calibrate_sensor(self):
        
        while not self.done_event.is_set():
            try:
                data = random.randint(0,155) if TEST_MODE else self.ser.readline().decode().strip()
                if TEST_MODE and data%7==0:
                    data = 'done'
                if(data == 'req_in'):
                    self.ser.write(input("input required").encode())
                elif(data == 'done'):
                    self.done_event.set()
                else:
                    print(f"Received data: {data}")
            except Exception as e:
                print(f"Error reading data: {e}")
            #await asyncio.sleep(1)
        self.done_event.clear()
        

    async def stop_collection(self):

        self.stop_event.set()  # Signal data collection coroutine to stop
        print("Stopping data collection.")
        if TEST_MODE: # if test wait a bit else signal interface to stop data collection 
            await asyncio.sleep(1)
        else:
            self.ser.write('3'.encode())

        while not TEST_MODE and self.ser.readline().decode().strip() != 'done':
            pass

        print("Saving collected data.")
        with open( f"{outF_path}{outF_name}{self.outF_count}.csv",'w', newline ='' ) as outFile:
            self.outF_count +=1
            writer = csv.writer(outFile)
            writer.writerows(self.data)
        outFile.close()
        print(f"# rows: {self.data.__len__()}")
        self.data.clear()
        self.stop_event.clear()
#
#
#
#
#
#


async def main_menu(serial_port):
    collector = DataCollector(serial_port)

    print("\n_____________________________\n\\Welcome to the greatest show!\\\n ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    
    while True:
        print("Serial Sensor Data Collection Menu:")
        print("1. Run data collection loop")    # non blocking bc need to stop on command -> run conc
        print("2. Calibrate sensor")            # input should be blocking, so calling with awaiy 
        print("3. Stop data collection")        # ties w 1 
        print("4. Exit")
        #list ports
        #set up stuff
        choice = input("Enter your choice (1/2/3/4): ")
        

        if choice == '1':
            print("Collecting data...")
            asyncio.create_task(collector.collect_data())

        elif choice == '2':
            print("Calibrating sensor...")
            await collector.calibrate_sensor()
            print("Calibratitinated")

        elif choice == '3':
            await collector.stop_collection()
        elif choice == '4':
            print("Have a waandafool deeeiiyum!")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    asyncio.run(main_menu(serial_port=SERIAL_PORT))