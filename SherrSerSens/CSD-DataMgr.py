#TODO :optional set/change path, port and baudrate

import asyncio
import serial
import  queue

import csv
import random
import time
"""
TODO :: change this to dict or enum and std thing
Serial Codes:
req_in      := requesting input
done        := signals a process has completed (i.e. calibration), clear event after completion

"""



outF_name = "testfile_m"
outF_path = "./"
SERIAL_PORT = "COMx"
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
        self.ser.write('1'.encode())
        aux = time.time()
        while not self.stop_event.is_set():
            try:
                ser_read = [random.randint(0,22550)*6] if TEST_MODE else self.ser.readline().decode().strip()
                self.data.append(ser_read)
                #store read on dequeue
            except Exception as e:
                self.data.append(f"Error reading data: {e}")
                print(f"Error reading data: {e}")
            if TEST_MODE or 3 < (time.time() - aux):
                aux = time.time()
                await asyncio.sleep(0.1) 
        self.stop_event.clear()

     

    def calibrate_sensor(self):
        self.ser.write('2'.encode())
        while not self.done_event.is_set():
            try:
                data = random.randint(0,155) if TEST_MODE else self.ser.readline().decode().strip()
                if TEST_MODE and data%7==0:
                    data = 'done'
                if(data == 'req_in'):
                    self.ser.write(input("input required").strip().encode())
                elif(data == 'done'):
                    self.done_event.set()
                else:
                    print(f"Received data: {data}")
            except Exception as e:
                print(f"Error reading data: {e}")
            #await asyncio.sleep(1)
        self.done_event.clear()
        

    async   def stop_collection(self):

        self.stop_event.set()  # Signal data collection coroutine to stop
        print("Stopping data collection.")
        if TEST_MODE: # if test wait a bit else signal interface to stop data collection 
            await asyncio.sleep(1)
        else:
            self.ser.write('3'.encode())

        while self.stop_event.set() or (not TEST_MODE and self.ser.readline().decode().strip() != 'done'):
            pass

        print("Saving collected data.")
        with open( f"{outF_path}{outF_name}{self.outF_count}.csv",'w', newline ='' ) as outFile:
            auxData = map(lambda row : row.split(','), self.data)
            self.outF_count +=1
            writer = csv.writer(outFile)
            writer.writerows(auxData)
        outFile.close()
        print(f"# rows: {self.data.__len__()}")
        self.data.clear()
#
#
#
#
#
#

async def ainput(prompt):
    return input(prompt)

async def main_menu(serial_port):
    collector = DataCollector(serial_port)
    tasks = set()
    print("\n_____________________________\n\\Welcome to the greatest show!\\\n ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    
    while True:
        print("Serial Sensor Data Collection Menu:")
        print("1. Run data collection loop")    # non blocking bc need to stop on command -> run conc
        print("2. Calibrate sensor")            # input should be blocking, so calling with awaiy 
        print("3. Stop data collection")        # ties w 1 
        print("4. Exit")
        #list ports
        #set up stuff
        print(f'discarded junk:{collector.ser.in_waiting}')
        collector.ser.reset_input_buffer()

        choice =  await asyncio.to_thread(input,"Enter your choice (1/2/3/4):")
        print(choice)
        if choice == '1':
            print("Collecting data...")
            c_task = asyncio.create_task((collector.collect_data()))
            #await asyncio.sleep(5)
            #await ainput("input anything to continue.")


        elif choice == '2':
            print("Calibrating sensor...")
            collector.calibrate_sensor()
            print("Calibratitinated")

        elif choice == '3':
            await   collector.stop_collection()
        elif choice == '4':
            print("Have a waandafool deeeiiyum!")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    asyncio.run(main_menu(serial_port=SERIAL_PORT))