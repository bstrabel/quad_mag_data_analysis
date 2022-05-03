import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
import data_processing_lib.Quad_Mag_Plotting as qmp
import data_processing_lib.Quad_Mag_Decoding as qmd
import data_processing_lib.Quad_Mag_Commands as qmc

###Test Functions###


def linearity(ser):
    # Function Definition: Runs a linearity test, place in shield can, vary external field linearly from
    # -100,000 nT to +100,000 nT with steps of 4500 nT, measure each step for 10 seconds, plot the median
    # of 10 second value
    # Input: Serial object used to communicate with the microcontroller
    # Output: String to be ouputted to the user showing the test has completed
    breakLoop = 'Y'
    # no error checking done here
    fileName = input(
        "\nYou will need to create a file to hold median data points, enter a file name here (include file name extension):\n")
    medFile = open((qmd.defaultFilePath +
                    fileName), 'w', newline='')
    medFile.write(
        "Axis, Known Field (nT), magFieldX (nT), magFieldY (nT), magFieldZ (nT)")
    while breakLoop != 'n':
        qmc.takeContinuousMeasurement(ser, 's1')
        readFile = qmd.getReadFile('1')
        dataObject = qmd.decodeGenericFile(readFile, '1')
        medFile.write(dataObject.inputFieldAxis +
                      "," + dataObject.inputField + ",")
        magMedX = float(stat.median(dataObject.mag1x) + stat.median(dataObject.mag2x) +
                        stat.median(dataObject.mag3x) + stat.median(dataObject.mag4x)) / 4.0  # four mags
        magMedY = float(stat.median(dataObject.mag1y) + stat.median(dataObject.mag2y) +
                        stat.median(dataObject.mag3y) + stat.median(dataObject.mag4y)) / 4.0
        magMedZ = float(stat.median(dataObject.mag1z) + stat.median(dataObject.mag2z) +
                        stat.median(dataObject.mag3z) + stat.median(dataObject.mag4z)) / 4.0
        medFile.write(str(magMedX) + "," + str(magMedY) + "," + str(magMedZ))
        breakLoop = input(
            "Press enter to get the next data point or if you are done, input 'n' into the console: ")
    medFile.close()
    qmp.plotCollectedData('1')
    return "Linearity test completed!"


def stability(ser):
    # Function Definition: Runs a stability test, place in shield can, apply known DC field, 100
    # hours collecting data, average over different number of samples
    # Input: Serial object used to communicate with the microcontroller
    # Output: String to be ouputted to the user showing the test has completed
    qmc.takeContinuousMeasurement(ser, 's2')
    qmp.plotCollectedData('2')
    return "Stability test completed!"


def sensitivity(ser):
    # Function Definition: Runs a sensitivity test, in shield can, no external field, take 5 sets of
    # measurements over 30 seconds, do a fast fourier transform
    # Input: Serial object used to communicate with the microcontroller
    # Output: String to be ouputted to the user showing the test has completed

    return "Sensitivity test completed!"


def linFreqResp(ser):
    # Function Definition: Runs a linear frequency response test, place in a shield can, apply field with frequency
    # varying from 1 to 20 Hz (steps of 1 or 2 Hz), take measurements for 30 seconds, do a fast fourier transform
    # Input: Serial object used to communicate with the microcontroller
    # Output: String to be ouputted to the user showing the test has completed

    return "Linear frequency response test completed!"

###Helper Functions###


def getTest(ser):
    # Function Definition: Gets the test to be run during this loop iteration based on user input
    # Input: None
    # Output: Function pointer based on user input
    test_switcher = {
        '1': linearity,
        '2': stability,
        '3': sensitivity,
        '4': linFreqResp
    }
    # Get test to be run from the user
    while 1:
        testNum = input(
            "Which test would you like to run?\n1:Linearity\n2:Stability\n3:Sensitivity\n4:Linear Frequency Response\n\nEnter test number here (1-4): ")
        test = test_switcher.get(testNum, lambda ser: "Test failed!")
        if testNum != '1' and testNum != '2' and testNum != '3' and testNum != '4':
            print("\nInvalid test number", testNum, "try again\n")
        else:
            break
    return test(ser)
