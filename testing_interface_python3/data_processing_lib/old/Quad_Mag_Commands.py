import numpy as np
import matplotlib.pyplot as plt
import data_processing_lib.Quad_Mag_Plotting as qmp
import data_processing_lib.Quad_Mag_Decoding as qmd

###Various Command Flags###
#
# s -> standard config values
# d -> debug mode (helpful messages are printed to console)
# v -> verbose mode (all serial input is output to console)
# 1 -> linearity test
# 2 -> stability test
# 3 -> sensitivity Test
# 4 -> linear frequency response test
#

###Command Functions###

def setMagConfig(ser, flag):
    # Function Definition: Sets the config of the magnetometer
    # Input: Serial Object, Flag that contains options for function eg. verbose (v), debug (d), standard (s)
    # Output: String that holds the current mag config values
    allDefault = 'Y'
    if flag.find('s') == -1:
        allDefault = input(
            "\nDo you want to use all default values for the magnetometer config (Y/n)?\n")
    command = ""
    if allDefault != 'Y':
        command = b'\x01'
        cycleCount = input(
            "What cycle count do you want the magnetometers to run at (Leave blank for default value)?\nEnter here: ")
        if cycleCount == "":
            command = command + b'\x00\xC8'
        else:
            command = command + int(cycleCount).to_bytes(2, byteorder='big')
        tmrc_switcher = {
            '0': 0x00,  # 600 Hz
            '1': 0x01,  # 300 Hz
            '2': 0x02,  # 150 Hz
            '3': 0x03,  # 75 Hz
            '4': 0x04,  # 37 Hz
            '5': 0x05,  # 18 Hz
            '6': 0x06,  # 9 Hz
            '7': 0x07,  # 4.5 Hz
            '8': 0x08,  # 2.3 Hz
            '9': 0x09,  # 1.2 Hz
            '10': 0x0A,  # 0.6 Hz
            '11': 0x0B,  # 0.3 Hz
            '12': 0x0C,  # 0.15 Hz
            '13': 0x0D  # 0.075 Hz
        }
        tmrcIndex = input("What frequency do you want the magnetometers to sample at (Leave blank for default value)? \n0: 600 Hz\n1: 300 Hz\n2: 150 Hz\n3: 75 Hz\n4: 37 Hz\n5: 18 Hz\n6: 9 Hz\n7: 4.5 Hz\n8: 2.3 Hz\n9: 1.2 Hz\n10: 0.6 Hz\n11: 0.3 Hz\n12: 0.15 Hz\n13: 0.075 Hz\nEnter Here: ")
        if (int(tmrcIndex) < 0 or int(tmrcIndex) > 13) and tmrcIndex != "":
            print("Invalid tmrc index...try again")
            setMagConfig(ser, flag)
        if tmrcIndex == "":
            command = command + b'\x04' + int(0).to_bytes(6, byteorder='big')
        else:
            tmrcVal = tmrc_switcher.get(
                tmrcIndex, lambda ser: "Failed to retrieve tmrc value!")
            command = command + \
                int(tmrcVal).to_bytes(1, byteorder='big') + \
                int(0).to_bytes(6, byteorder='big')
    else:
        #command = b'\x01\x00\x64\x00\x00\x00\x00\x00\x00\x00'  # - 100 cycle counts
        command = b'\x01\x00\xC8\x00\x00\x00\x00\x00\x00\x00' # - 200 cycle counts
        #command = b'\x01\x03\x20\x00\x00\x00\x00\x00\x00\x00' # - 800 cycle counts
    ser.write(command)
    if flag.find('d') != -1:
        print("DEBUG: This is the command you just sent: " + str(command))
    updatedConfig = getResponse(ser)
    getResponse(ser) #Throwaway completion message
    if updatedConfig != command[1:4].hex():
        print("Failed to correctly update config of magnetometers!")
        print("New config: " + updatedConfig)
        print("What the config should be: " + command[1:4].hex())
    else:
        return (updatedConfig)


def setImuConfig(ser, flag):
    # Function Definition: Sets the config of the the imu
    # Input: Serial Object, Flag that contains options for function eg. verbose (v), debug (d), standard (s)
    # Output: String that holds the current imu config values
    allDefault = 'Y'
    if flag.find('s') == -1:
        allDefault = input(
            "\nDo you want to use all default values for the imu config (Y/n)?\n")
    command = ""
    if allDefault != 'Y':
        command = b'\x02'
        accOdr_switcher = {
            '0': 0x01,  # 0.78125 Hz
            '1': 0x02,  # 1.5625 Hz
            '2': 0x03,  # 3.125 Hz
            '3': 0x04,  # 6.25 Hz
            '4': 0x05,  # 12.5 Hz
            '5': 0x06,  # 25 Hz
            '6': 0x07,  # 50 Hz
            '7': 0x08,  # 100 Hz
            '8': 0x09,  # 200 Hz
            '9': 0x0a,  # 400 Hz
            '10': 0x0b,  # 800 Hz
            '11': 0x0c,  # 1600 Hz
        }
        accOdrIndex = input("\nWhat frequency do you want the accelerometer to sample at (Leave blank for default value)? \n0: 0.78125 Hz\n1: 1.5625 Hz\n2: 3.125 Hz\n3: 6.25 Hz\n4: 12.5 Hz\n5: 25 Hz\n6: 50 Hz\n7: 100 Hz\n8: 200 Hz\n9: 400 Hz\n10: 800 Hz\n11: 1600 Hz\nEnter Here: ")
        if accOdrIndex == "":
            command = command + b'\x0c'
        elif (int(accOdrIndex) < 0 or int(accOdrIndex) > 11) and accOdrIndex != "":
            print("Invalid acceleromter Odr index...try again")
            setImuConfig(ser, flag)
        else:
            accOdrVal = accOdr_switcher.get(
                accOdrIndex, lambda ser: "Failed to retrieve accelerometer Odr value!")
            command = command + int(accOdrVal).to_bytes(1, byteorder='big')
        accBwp_switcher = {
            '0': 0x00,  # osr4_avg1
            '1': 0x01,  # osr2_avg2
            '2': 0x02,  # norm_avg4
            '3': 0x03,  # cic_avg8
            '4': 0x04,  # res_avg18
            '5': 0x05,  # res_avg32
            '6': 0x06,  # res_avg64
            '7': 0x07  # res_avg128
        }
        accBwpIndex = input("What bandwidth parameter do you want for the accelerometer (Leave blank for default value)? \n0: osr4_avg1\n1: osr2_avg2\n2: norm_avg4\n3: cic_avg8\n4: res_avg18\n5: res_avg32\n6: res_avg64\n7: res_avg128\nEnter Here: ")
        if accBwpIndex == "":
            command = command + b'\x02'
        elif (int(accBwpIndex) < 0 or int(accBwpIndex) > 7) and accBwpIndex != "":
            print("Invalid acceleromter Bwp index...try again")
            setImuConfig(ser, flag)
        else:
            accBwpVal = accBwp_switcher.get(
                accBwpIndex, lambda ser: "Failed to retrieve accelerometer Bwp value!")
            command = command + int(accBwpVal).to_bytes(1, byteorder='big')
        accFiltPerf_switcher = {
            '0': 0x00,  # ulp
            '1': 0x01,  # hp
        }
        accFiltPerfIndex = input(
            "What filter performance mode do you want for the accelerometer (Leave blank for default value)? \n0: ulp\n1: hp\nEnter Here: ")
        if accFiltPerfIndex == "":
            command = command + b'\x01'
        elif (int(accFiltPerfIndex) < 0 or int(accFiltPerfIndex) > 1) and accFiltPerfIndex != "":
            print("Invalid acceleromter Filter Perf index...try again")
            setImuConfig(ser, flag)
        else:
            accFiltPerfVal = accFiltPerf_switcher.get(
                accFiltPerfIndex, lambda ser: "Failed to retrieve accelerometer Filter Perf value!")
            command = command + \
                int(accFiltPerfVal).to_bytes(1, byteorder='big')
        accRange_switcher = {
            '0': 0x00,  # +/-2g
            '1': 0x01,  # +/-4g
            '2': 0x02,  # +/-8g
            '3': 0x03  # +/-16g
        }
        accRangeIndex = input(
            "What range do you want for the accelerometer (Leave blank for default value)? \n0: +/-2g\n1: +/-4g\n2: +/-8g\n3: +/-16g\nEnter Here: ")
        if accRangeIndex == "":
            command = command + b'\x01'
        elif (int(accRangeIndex) < 0 or int(accRangeIndex) > 1) and accRangeIndex != "":
            print("Invalid acceleromter range index...try again")
            setImuConfig(ser, flag)
        else:
            accRangeVal = accRange_switcher.get(
                accRangeIndex, lambda ser: "Failed to retrieve accelerometer range value!")
            command = command + int(accRangeVal).to_bytes(1, byteorder='big')
        gyrOdr_switcher = {
            '0': 0x06,  # 25 Hz
            '1': 0x07,  # 50 Hz
            '2': 0x08,  # 100 Hz
            '3': 0x09,  # 200 Hz
            '4': 0x0A,  # 400 Hz
            '5': 0x0B,  # 800 Hz
            '6': 0x0C,  # 1600 Hz
            '7': 0x0D,  # 3200 Hz
        }
        gyrOdrIndex = input(
            "What frequency do you want the gyroscope to sample at (Leave blank for default value)? \n0: 25 Hz\n1: 50 Hz\n2: 100 Hz\n3: 200 Hz\n4: 400 Hz\n5: 800 Hz\n6: 1600 Hz\n7: 3200 Hz\nEnter Here: ")
        if gyrOdrIndex == "":
            command = command + b'\x0c'
        elif (int(gyrOdrIndex) < 0 or int(gyrOdrIndex) > 7) and gyrOdrIndex != "":
            print("Invalid gyroscope Odr index...try again")
            setImuConfig(ser, flag)
        else:
            gyrOdrVal = gyrOdr_switcher.get(
                gyrOdrIndex, lambda ser: "Failed to retrieve gyroscope Odr value!")
            command = command + int(gyrOdrVal).to_bytes(1, byteorder='big')
        gyrBwp_switcher = {
            '0': 0x00,  # osr4
            '1': 0x01,  # osr2
            '2': 0x02,  # norm
        }
        gyrBwpIndex = input(
            "What bandwidth parameter do you want for the gyroscope (Leave blank for default value)? \n0: osr4\n1: osr22\n2: norm\nEnter Here: ")
        if gyrBwpIndex == "":
            command = command + b'\x02'
        elif (int(gyrBwpIndex) < 0 or int(gyrBwpIndex) > 2) and gyrBwpIndex != "":
            print("Invalid gyroscope Bwp index...try again")
            setImuConfig(ser, flag)
        else:
            gyrBwpVal = gyrBwp_switcher.get(
                gyrBwpIndex, lambda ser: "Failed to retrieve gyroscope Bwp value!")
            command = command + int(gyrBwpVal).to_bytes(1, byteorder='big')
        gyrNoisePerf_switcher = {
            '0': 0x00,  # ulp
            '1': 0x01,  # hp
        }
        gyrNoisePerfIndex = input(
            "What noise performance mode do you want for the gyroscope (Leave blank for default value)? \n0: ulp\n1: hp\nEnter Here: ")
        if gyrNoisePerfIndex == "":
            command = command + b'\x01'
        elif (int(gyrNoisePerfIndex) < 0 or int(gyrNoisePerfIndex) > 1) and gyrNoisePerfIndex != "":
            print("Invalid gyroscope Noise Perf index...try again")
            setImuConfig(ser, flag)
        else:
            gyrNoisePerfVal = gyrNoisePerf_switcher.get(
                gyrNoisePerfIndex, lambda ser: "Failed to retrieve gyroscope Noise Perf value!")
            command = command + \
                int(gyrNoisePerfVal).to_bytes(1, byteorder='big')
        gyrFiltPerf_switcher = {
            '0': 0x00,  # ulp
            '1': 0x01,  # hp
        }
        gyrFiltPerfIndex = input(
            "What filter performance mode do you want for the gyroscope (Leave blank for default value)? \n0: ulp\n1: hp\nEnter Here: ")
        if gyrFiltPerfIndex == "":
            command = command + b'\x01'
        elif (int(gyrFiltPerfIndex) < 0 or int(gyrFiltPerfIndex) > 1) and gyrFiltPerfIndex != "":
            print("Invalid gyroscope Filt Perf index...try again")
            setImuConfig(ser, flag)
        else:
            gyrFiltPerfVal = gyrFiltPerf_switcher.get(
                gyrFiltPerfIndex, lambda ser: "Failed to retrieve gyroscope Filt Perf value!")
            command = command + \
                int(gyrFiltPerfVal).to_bytes(1, byteorder='big')
        gyrRange_switcher = {
            '0': 0x00,  # +/-2000dps
            '1': 0x01,  # +/-1000dps
            '2': 0x02,  # +/-500dps
            '3': 0x03,  # +/-250dps
            '4': 0x04  # +/-125dps
        }
        gyrRangeIndex = input(
            "What range do you want for the gyroscope (Leave blank for default value)? \n0: +/-2000dps\n1: +/-1000dps\n2: +/-500dps\n3: +/-250dps\n4: +/-125dps\nEnter Here: ")
        if gyrRangeIndex == "":
            command = command + b'\x00'
        elif (int(gyrRangeIndex) < 0 or int(gyrRangeIndex) > 1) and gyrRangeIndex != "":
            print("Invalid gyroscope range index...try again")
            setImuConfig(ser, flag)
        else:
            gyrRangeVal = gyrRange_switcher.get(
                gyrRangeIndex, lambda ser: "Failed to retrieve gyroscope range value!")
            command = command + int(gyrRangeVal).to_bytes(1, byteorder='big')
    else:
        command = b'\x02\x0c\x02\x01\x01\x0c\x02\x01\x01\x00'
    ser.write(command)
    if flag.find('d') != -1:
        print("DEBUG: This is the command you just sent: " + str(command))
    updatedConfig = getResponse(ser)
    getResponse(ser) #Throwaway completion message
    if updatedConfig != command[1:10].hex():
        print("Failed to correctly update imu config!")
        print("New config: " + updatedConfig)
        print("What the config should be: " + command[1:10].hex())
    else:
        return (updatedConfig)


def getMagConfig(ser, flag):
    # Function Definition: Gets the config of the magnetometer
    # Input: Serial Object, Flag that contains options for function eg. verbose (v), debug (d)
    # Output: String that holds the current mag config values
    command = b'\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ser.write(command)
    config = getResponse(ser)
    getResponse(ser) #Throwaway completion message
    if flag.find('d') != -1:
        print(config)
    return config


def getImuConfig(ser, flag):
    # Function Definition: Gets the config of the imu
    # Input: Serial Object, Flag that contains options for function eg. verbose (v), debug (d)
    # Output: String that holds the current imu config values
    command = b'\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ser.write(command)
    config = getResponse(ser)
    getResponse(ser) #Throwaway completion message
    if flag.find('d') != -1:
        print(config)
    return config


def takeSingleMeasurement(ser, flag):
    # Function Definition: Requests a single measurement from the quad-mag
    # Input: Serial Object, Flag that contains options for function eg. verbose (v), debug (d)
    # Output: String that tells the caller the measurement has been completed
    enabledIMU = input("\nIs the BMI270 enabled (Y/n)? ")
    enabledTMP = input("Is the TMP36 enabled (Y/n)? ")
    print("")
    writeFile = qmd.getWriteFile(flag)
    sensorConfigs = setMagConfig(ser, flag)
    sensorConfigsCSV = sensorConfigs[0:4] + ","
    if enabledIMU == 'Y':
        sensorConfigs = sensorConfigs + setImuConfig(ser, flag)
        sensorConfigsCSV = sensorConfigsCSV + sensorConfigs[12:14] + ","
        sensorConfigsCSV = sensorConfigsCSV + sensorConfigs[22:24]
        writeFile.write(
            "Mag Gain, Accel Gain, Gyro Gain (all sensor readings are raw and need to be converted out of lsb form)\n")
    else:
        writeFile.write(
            "Mag Gain (all sensor readings are raw and need to be converted out of lsb form)\n")
    writeFile.write(sensorConfigsCSV)
    if enabledTMP == 'Y' and enabledIMU == 'Y':
        writeFile.write(
            "\nMeas-Num, Syst-Time (sec), Fract-Syst-Time (1/32768 sec), B1-X , B1-Y, B1-Z, B2-X, B2-Y, B2-Z, B3-X, B3-Y, B3-Z, B4-X, B4-Y, B4-Z, Acc-X, Acc-Y, Acc-Z, Gyr-X, Gyr-Y, Gyr-Z, Temp\n")
    elif enabledTMP != 'Y' and enabledIMU != 'Y':
        writeFile.write(
            "\nMeas-Num, Syst-Time (sec), Fract-Syst-Time (1/32768 sec), B1-X , B1-Y, B1-Z, B2-X, B2-Y, B2-Z, B3-X, B3-Y, B3-Z, B4-X, B4-Y, B4-Z\n")
    elif enabledIMU == 'Y':
        writeFile.write(
            "\nMeas-Num, Syst-Time (sec), Fract-Syst-Time (1/32768 sec), B1-X , B1-Y, B1-Z, B2-X, B2-Y, B2-Z, B3-X, B3-Y, B3-Z, B4-X, B4-Y, B4-Z, Acc-X, Acc-Y, Acc-Z, Gyr-X, Gyr-Y, Gyr-Z\n")
    else:
        writeFile.write(
            "\nMeas-Num, Syst-Time (sec), Fract-Syst-Time (1/32768 sec), B1-X , B1-Y, B1-Z, B2-X, B2-Y, B2-Z, B3-X, B3-Y, B3-Z, B4-X, B4-Y, B4-Z, Temp\n")
    command = b'\x05'
    disableMags = input("\nDo you want to disable any mags (Y/n)?\n") #all mags are enabled by default
    magsEnabled = 0b1111
    if disableMags == 'Y' :
        magsToDisable = input("\nEnter the mag numbers you would like to disable as a single string eg. 1234")
        if magsToDisable.find('1') != -1 :
            magsEnabled = magsEnabled & 0b1110
        if magsToDisable.find('2') != -1 :
            magsEnabled = magsEnabled & 0b1101
        if magsToDisable.find('3') != -1 :
            magsEnabled = magsEnabled & 0b1011
        if magsToDisable.find('4') != -1 :
            magsEnabled = magsEnabled & 0b0111
    command = command + (magsEnabled).to_bytes(1, byteorder='big')
    command = command + (0).to_bytes(8, byteorder='big')
    ser.write(command)  # Single meas command
    if flag.find('d') != -1:
        print("\nDEBUG: THIS IS THE COMMAND YOU JUST SENT\n" + str(command) + "\n")
    invalidPacketCount = 0
    invalidPacketThreshold = 9  # Arbitrarily chosen
    returnString = ""
    while 1:
        returnedBytesStr = getResponse(ser)
        # Stops the python program from attempting invalid string
        # operations....
        if returnedBytesStr == "COMPLETE":
            returnString = "\nSingle measurement completed successfully!"
            break
        elif invalidPacketCount > invalidPacketThreshold:
            return "\nToo many invalid packets received, single measurement did not complete successfully!"
        elif len(returnedBytesStr) > 0:  # includes commas and packet flag
            if flag.find('v') != -1:
                print("1," + returnedBytesStr)
            writeFile.write("1," + returnedBytesStr + "\n")
            break
        else:
            invalidPacketCount = invalidPacketCount + 1
    print("\n******Finished a single measurement******\n")
    writeFile.close()
    if flag.find('p') != -1:
        createPlots = input(
            "Data has finished collecting...do you want to create plots (Y/n) \n")
        if createPlots == 'Y':
            readFile = qmd.getReadFile(flag)
            qmp.plotData(readFile, 'u')
            readFile.close()
    return returnString


def takeContinuousMeasurement(ser, flag):
    # Function Definition: Requests continuous measurements from mag for specified period of time
    # Input: Serial Object, Flag that contains options for function eg. verbose (v), debug (d), stability (2)
    # Output: String that tells the caller the measurements have been completed
    enabledIMU = input("\nIs the BMI270 enabled (Y/n)? ")
    enabledTMP = input("Is the TMP36 enabled (Y/n)? ")
    writeFile = qmd.getWriteFile(flag)
    sensorConfigs = setMagConfig(ser, flag)
    sensorConfigsCSV = sensorConfigs[0:4] + ","
    if enabledIMU == 'Y':
        sensorConfigs = sensorConfigs + setImuConfig(ser, flag)
        sensorConfigsCSV = sensorConfigsCSV + sensorConfigs[12:14] + ","
        sensorConfigsCSV = sensorConfigsCSV + sensorConfigs[22:24]
    command = b'\x06'
    measurementLength = 0.00
    #sampleRate = sampleRate = ((2**(-(int(sensorConfigs[5:6], 16)))) * 600)
    sampleRate = 1
    if flag.find('u') != -1:
        averaged = input("\nDo you want to average the data (Y/n)? ")
        if averaged == 'Y':
            command = command + b'\x01'
            sampleRate = 1
        else:
            command = command + b'\x00'
            sampleRate = int(
                input("\nWhat rate would you like to sample at (Hz)? "))
        command = command + sampleRate.to_bytes(1, byteorder='big')
        disableMags = input("\nDo you want to disable any mags (Y/n)? ") #all mags are enabled by default
        magsEnabled = 0b1111
        if disableMags == 'Y' :
            magsToDisable = input("\nEnter the mag numbers you would like to disable as a single string eg. 1234\n")
            if magsToDisable.find('1') != -1 :
                magsEnabled = magsEnabled & 0b1110
            if magsToDisable.find('2') != -1 :
                magsEnabled = magsEnabled & 0b1101
            if magsToDisable.find('3') != -1 :
                magsEnabled = magsEnabled & 0b1011
            if magsToDisable.find('4') != -1 :
                magsEnabled = magsEnabled & 0b0111
        command = command + (magsEnabled).to_bytes(1, byteorder='big')
        measurementLength = input(
            "\nEnter how many minutes do you want to take measurements for: ")
        command = command + (int(float(measurementLength) * 60)).to_bytes(6, byteorder='big')
    elif flag.find('1') != -1:  # Vary external field, measure for 10 sec and take median
        writeFile.write(
            "******Linearity Test File******\n\nExternal Field (nT), Axis\n")
        inputFld = input(
            "\nWhat is the value of the external field you are applying (nT)? ")
        axis = input("Which axis are you applying this field to (x,y,z)? ")
        print("\n")
        writeFile.write(inputFld + ',' + axis + '\n')
        measurementLength = 10.0 / 60.0  # Minutes
        command = command + b'\x00' + \
            int(measurementLength * 60).to_bytes(8, byteorder='big')
    elif flag.find('2') != -1:  # Stability test, average data over a second and run for 100 hours
        writeFile.write("******Stability Test File******\n\n")
        measurementLength = 100 * 60  # Minutes
        command = command + b'\x00' + \
            (measurementLength * 60).to_bytes(8, byteorder='big')
    elif flag.find('3') != -1:
        writeFile.write("******Sensitivity Test File******\n\n")
        measurementLength = 0.5  # Minutes
        command = command + b'\x00' + \
            int(measurementLength * 60).to_bytes(8, byteorder='big')
    elif flag.find('4') != -1:
        # Temp need to implement yet
        writeFile.write("******Linear Frequency Reponse Test File******\n\n")
    if enabledIMU == 'Y':
        writeFile.write(
            "Mag Gain, Accel Gain, Gyro Gain (all sensor readings are raw and need to be converted out of lsb form)\n")
    else:
        writeFile.write(
            "Mag Gain (all sensor readings are raw and need to be converted out of lsb form)\n")
    writeFile.write(sensorConfigsCSV)
    if enabledTMP == 'Y' and enabledIMU == 'Y':
        writeFile.write(
            "\nMeas-Num, Syst-Time (sec), Fract-Syst-Time (1/32768 sec), B1-X , B1-Y, B1-Z, B2-X, B2-Y, B2-Z, B3-X, B3-Y, B3-Z, B4-X, B4-Y, B4-Z, Acc-X, Acc-Y, Acc-Z, Gyr-X, Gyr-Y, Gyr-Z, Temp\n")
    elif enabledTMP != 'Y' and enabledIMU != 'Y':
        writeFile.write(
            "\nMeas-Num, Syst-Time (sec), Fract-Syst-Time (1/32768 sec), B1-X , B1-Y, B1-Z, B2-X, B2-Y, B2-Z, B3-X, B3-Y, B3-Z, B4-X, B4-Y, B4-Z\n")
    elif enabledIMU == 'Y':
        writeFile.write(
            "\nMeas-Num, Syst-Time (sec), Fract-Syst-Time (1/32768 sec), B1-X , B1-Y, B1-Z, B2-X, B2-Y, B2-Z, B3-X, B3-Y, B3-Z, B4-X, B4-Y, B4-Z, Acc-X, Acc-Y, Acc-Z, Gyr-X, Gyr-Y, Gyr-Z\n")
    else:
        writeFile.write(
            "\nMeas-Num, Syst-Time (sec), Fract-Syst-Time (1/32768 sec), B1-X , B1-Y, B1-Z, B2-X, B2-Y, B2-Z, B3-X, B3-Y, B3-Z, B4-X, B4-Y, B4-Z, Temp\n")
    ser.write(command)
    if flag.find('d') != -1:
        print("\nDEBUG: THIS IS THE COMMAND YOU JUST SENT\n" + str(command) + "\n")
    totalMeasurements = 0
    expectedMeasurements = (int(measurementLength) * 60) * int(sampleRate)
    invalidPacketCount = 0
    invalidPacketThreshold = 9  # Arbitrarily chosen
    returnString = ""
    while 1:
        # Will either be roughly once every second or every 40 seconds
        if flag.find('v') == -1 and totalMeasurements % 40 == 0:
            print(str(totalMeasurements) + "/" +
                  str(expectedMeasurements) + " measurements received")
        returnedBytesStr = getResponse(ser)
        # Stops the python program from attempting invalid string
        # operations....
        if returnedBytesStr == "COMPLETE":
            returnString = "\nContinuous measurement completed successfully!"
            break
        elif invalidPacketCount > invalidPacketThreshold:
            return "\nToo many invalid packets received, continuous measurement did not complete successfully!"
        elif len(returnedBytesStr) > 0:
            totalMeasurements = totalMeasurements + 1
            if flag.find('v') != -1:
                print(str(totalMeasurements) + "," + returnedBytesStr)
            writeFile.write(str(totalMeasurements) +
                            "," + returnedBytesStr + "\n")
        else:
            invalidPacketCount = invalidPacketCount + 1
    print("\n******Finished a continuous measurement******\n")
    print("\nExpected Measurements: " + str(expectedMeasurements))
    print("\nMissing Measurements: " +
          str(expectedMeasurements - totalMeasurements) + "\n")
    print("\nInvalid Packets Received: " + str(invalidPacketCount) + "\n")
    writeFile.close()
    if flag.find('p') != -1:
        createPlots = input(
            "Data has finished collecting...do you want to create plots (Y/n)\n")
        if createPlots == 'Y':
            readFile = qmd.getReadFile(flag)
            qmp.plotData(readFile, 'u')
            readFile.close()
    return returnString


def sendAvailableData(ser, flag):
    # Function Definition: Send any data we have available
    # Input: Serial object, Flag that contains options for function eg. verbose (v), debug (d)
    # Output: String that holds data if it was valid
    command = b'\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ser.write(command)
    returnedBytesStr = getResponse(ser)
    if returnedBytesStr == "":
        return "The data was either corrupted or invalid"
    else:
        return returnedBytesStr
    return "The data checksum was invalid"


def stopAllOps(ser, flag):
    # Function Definition: Stops all sensors and puts controller in ulp mode
    # Input: serial object, Flag that contains options for function eg. verbose (v), debug (d)
    # Output: String confirming whether the command was successfully executed
    command = b'\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ser.write(command)
    returnedBytesStr = getResponse(ser)
    if returnedBytesStr == "COMPLETE":
        return "\nSuccessfully stopped all operations and put controller into low power mode!\n"
    return "\nDid not successfully stop all operations, an error occurred!\n"

###Helper Functions###


def getResponse(ser):
    # Temporary to create object
    returnedBytes = (0).to_bytes(1, byteorder='big')
    returnedBytes = ser.read(1)  # Gets packet flag
    packetFlag = returnedBytes.hex()
    # Stops the python program from attempting invalid string
    # operations....
    if packetFlag == "0a":
        return "COMPLETE"
    # Debug Flag
    elif packetFlag == '01':
        returnedBytes = ser.read(17)
        if len(returnedBytes) == 17:
            if qmd.validChecksum(returnedBytes, packetFlag):
                return packetFlag + "," + qmd.decodeSerialByteStream(returnedBytes, packetFlag)
            else:
                return ""
    # Mag Config Flag
    elif packetFlag == '02':
        return (ser.read(3).hex())
    # IMU Config Flag
    elif packetFlag == '03':
        return (ser.read(9).hex())
    # Mag Data Only Flag
    elif packetFlag == '04':
        returnedBytes = ser.read(44)
        if len(returnedBytes) == 44:
            if qmd.validChecksum(returnedBytes, packetFlag):
                return packetFlag + "," + qmd.decodeSerialByteStream(returnedBytes, packetFlag)
            else:
                return ""
    # All Sensors Data Flag
    elif packetFlag == '05':
        returnedBytes = ser.read(58)
        if len(returnedBytes) == 58:
            if qmd.validChecksum(returnedBytes, packetFlag):
                return packetFlag + "," + qmd.decodeSerialByteStream(returnedBytes, packetFlag)
            else:
                return ""
    # Mag and TMP data flag
    elif packetFlag == '06':
        returnedBytes = ser.read(46)
        if len(returnedBytes) == 46:
            if qmd.validChecksum(returnedBytes, packetFlag):
                return packetFlag + "," + qmd.decodeSerialByteStream(returnedBytes, packetFlag)
            else:
                return ""
    # Mag and IMU data flag
    elif packetFlag == '07':
        returnedBytes = ser.read(56)
        if len(returnedBytes) == 56:
            if qmd.validChecksum(returnedBytes, packetFlag):
                return packetFlag + "," + qmd.decodeSerialByteStream(returnedBytes, packetFlag)
            else:
                return ""
    # Invalid Packet
    else:
        return ""


def getCommand(ser):
    # Function Definition: Gets the command to be run during this loop iteration based on user input
    # Input: None
    # Output: Function pointer based on user input
    command_switcher = {
        '1': setMagConfig,
        '2': setImuConfig,
        '3': getMagConfig,
        '4': getImuConfig,
        '5': takeSingleMeasurement,
        '6': takeContinuousMeasurement,
        '7': sendAvailableData,
        '8': stopAllOps
    }
    # Get command to be run from the user
    while 1:
        commandNum = input(
            "What command would you like to send?\n\n1: Set Mag Config\n2: Set IMU Config\n3: Get Mag Config\n4: Get IMU Config\n5: Take Single Measurement\n6: Take Continuous Measurement\n7: Send Available Data\n8: Stop All Operations\n\nEnter a command number here (1-8): ")
        command = command_switcher.get(
            commandNum, lambda ser: "Command failed!")
        if int(commandNum) < 1 or int(commandNum) > 8:
            print("\nInvalid command number", commandNum, "try again\n")
        else:
            break
    return command(ser, 'vdpu')
