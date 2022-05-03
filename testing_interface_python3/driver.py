import serial
import sys
import data_processing_lib.data_commands_lib as dcl
import data_processing_lib.data_plotting_lib as dpl

#### Config Options ####
imu_enabled = 0
temperature_enabled = 0

#### Serial Port ####


def openSerialPort():
    # Function Definition: Attempt to open a serial connection
    # Input: Port to open
    # Output: Serial object

    # See python serial library for more documentation
    baudrate = 115200  # Pre-Defined
    timeout = 3  # Pre-Defined
    tries = 5  # Arbitrary number of times we try to open serial port before giving up
    linux = input('\nAre you running this program in linux (Y/n): ')
    portNum = input(
        "\nEnter the port number you wish to establish a serial connection with (0,1,2,etc.): ")
    port = ""
    if linux == 'Y':
        #port = '/dev/ttyS' + portNum
        port = '/dev/ttyACM' + portNum
    else:
        port = 'COM' + portNum
    while tries > 0:  # Attempt to establish serial port connection
        try:
            ser = serial.Serial(
                port, baudrate, timeout=timeout, write_timeout=timeout)
            print("Serial port", port, "was opened successfully\n")
            break
        except serial.SerialException:
            print("Could not open", port,
                  "check connection or port configuration")
            tries -= 1
    if tries == 0:
        print("Failed to open specified port! Exiting...")
        sys.exit()
    return ser  # Return the serial object created
#### End Serial Port ####

#### Main ####


def main():
    # Loop that runs tests until user ends the program
    run_switcher = {
        '1': dcl.get_command,
        '2': dpl.plot_data
    }
    while 1:
        # Retrieve the function the user wants to run
        run_num = input(
            "Would you like to send a command, or plot previously collected data?\n1:Send Command\n2:Plot Previous Data\n\nEnter a number here (1-2): ")
        run = run_switcher.get(
            run_num, lambda ser: "The function you selected failed!")
        if run_num != '1' and run_num != '2' :
            print("\nInvalid number", run_num, "try again\n")
        # Run the test and print its output
        if run_num == '2':
            print(run('uf'))
        else:
            # Open the serial port
            ser = openSerialPort()
            f = 'i' if imu_enabled else ''
            f = (f + 't') if temperature_enabled else f 
            print(run(ser, f))
            ser.close()
        # Continue to run tests until the user ends the program
        cont = input("Do you want to run another this program again (Y/n)? \n")
        if cont != 'Y' and cont != 'qY':
            break
    return
#### End Main ####


#### Run ####
main()
#### End Run ####
