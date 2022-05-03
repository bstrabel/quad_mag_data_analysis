import numpy as np
import csv
import os

defaultFilePath = 'data_storage/'
num_mags = 1


def getReadFile(flag):
    # Function Description: Requests and attempts to open file specified by user
    #Input: Flag
    # Output: Read-only file object
    filePath = ""
    while 1:
        if flag.find('1') != -1:
            fileName = input(
                "\nWhat is the name of the file you want to get data from for the next data point in the linearity test (exclude the file extension)?\n")
            filePath = defaultFilePath + '/' + fileName + ".txt"
        else:
            fileName = input(
                "\nWhat is the name of the file you want to get data from (include file extension...must be in a csv format)?\n")
            filePath = input(
                "What is the file path, relative to this directory (Leave blank for default)?\n")
            if filePath == "":
                filePath = defaultFilePath + '/' + fileName
            else:
                filePath = filePath + '/' + fileName
        try:
            readFile = open(filePath, 'r', newline='')
            return readFile
        except FileNotFoundError:
            print("\nThat file could not be found...try again\n")


def getWriteFile(flag):
    # Function Description: Requests and attempts to open file specified by user
    #Input: Flag
    # Output: Write-only file object
    filePath = ""
    while 1:
        if flag.find('1') != -1:
            fileName = input(
                "\nWhat is the name of the file you want to write data to for the next linearity test point (exclude the file extension)?\n")
            filePath = defaultFilePath + '/' + fileName + ".txt"
        else:
            fileName = input(
                "\nWhat is the name of the file you want to write data to (include file extension...must be in a csv format)?\n")
            filePath = input(
                "What is the file path, relative to this directory (Leave blank for default)?\n")
            if filePath == "":
                filePath = defaultFilePath + '/' + fileName
            else:
                filePath = filePath + '/' + fileName
        try:
            writeFile = open(filePath, 'w')
            return writeFile
        except FileExistsError:
            print("\nThat file could not be written to...try again\n")

# General data container for use in plotting, data processing, etc...


class dataPacket:  # 59 byte packet sent via serial comms
    def __init__(self):
        self.sampleRate = 37.0
        self.inputFieldAxis = ""
        self.inputField = 0  # Applied external field
        self.packetFlag = []  # 1 byte tag that determines message type
        self.timestamp = []  # 6 byte timestamp
        self.mag1x = []  # 3 byte x-axis
        self.mag1y = []  # 3 byte y-axis
        self.mag1z = []  # 3 byte z-axis
        self.mag2x = []  # 3 byte x-axis
        self.mag2y = []  # 3 byte y-axis
        self.mag2z = []  # 3 byte z-axis
        self.mag3x = []  # 3 byte x-axis
        self.mag3y = []  # 3 byte y-axis
        self.mag3z = []  # 3 byte z-axis
        self.mag4x = []  # 3 byte x-axis
        self.mag4y = []  # 3 byte y-axis
        self.mag4z = []  # 3 byte z-axis
        self.accx = []  # 2 byte x-axis
        self.accy = []  # 2 byte y-axis
        self.accz = []  # 2 byte z-axis
        self.gyrx = []  # 2 byte x-axis
        self.gyry = []  # 2 byte y-axis
        self.gyrz = []  # 2 byte z-axis
        self.temp = []  # 2 byte temperature
        self.dataIndex = 0  # current index for arrays of data/final size


def valid_checksum(byte_object_in, flag):
    packetSum = 0
    cks = 0
    if flag == '04':
        cks = int(byte_object_in[42:44].hex(), 16)
        for index in range(0, 42):
            packetSum = packetSum + byte_object_in[index]
    elif flag == '05':
        cks = int(byte_object_in[56:58].hex(), 16)
        for index in range(0, 56):
            packetSum = packetSum + byte_object_in[index]
    elif flag == '06':
        cks = int(byte_object_in[44:46].hex(), 16)
        for index in range(0, 44):
            packetSum = packetSum + byte_object_in[index]
    elif flag == '07':
        cks = int(byte_object_in[54:56].hex(), 16)
        for index in range(0, 54):
            packetSum = packetSum + byte_object_in[index]
    if packetSum == cks:
        return True
    return False


def decode_serial_byte_stream_quad(byte_object_in, flag):
    # Function Definition: Decodes data read from serial port
    # Input: Byte Object, Well-Formatted
    # Output: String, comma seperated
    sss = byte_object_in.hex()
    i = 0
    return_string_csv = int(sss[i:i+8],16) + \
        "," + int(sss[i+8:i+12], 16) + ","
    i = i + 12
    if flag == '01':
        while i < 30:
            return_string_csv = return_string_csv + \
                int(sss[i:i+6], 16) + ","
            i = i + 6
    elif flag == '04':
        while i < 84:
            return_string_csv = return_string_csv + \
                int(sss[i:i+6], 16) + ","
            i = i + 6
    elif flag == '05':
        while i < 84:
            return_string_csv = return_string_csv + \
                int(sss[i:i+6], 16) + ","
            i = i + 6
        while i < 108:
            return_string_csv = return_string_csv + \
                int(sss[i:i+4], 16) + ","
            i = i + 4
        return_string_csv = return_string_csv + \
            int(sss[i:i+4], 16)
    elif flag == '06':
        while i < 84:
            return_string_csv = return_string_csv + \
                int(sss[i:i+6], 16) + ","
            i = i + 6
        return_string_csv = return_string_csv + \
            int(sss[i:i+4], 16)
    elif flag == '07':
        while i < 84:
            return_string_csv = return_string_csv + \
                int(sss[i:i+6], 16) + ","
            i = i + 6
        while i < 108:
            return_string_csv = return_string_csv + \
                int(sss[i:i+4], 16) + ","
            i = i + 4
    # We discard the checksum
    return return_string_csv


def decode_twos_comp(ntc, nb):
    # Function Definition: Decodes twos complement input into a signed decimal number
    # Input: int twos complement number, int size of number in bits
    # Output: int converted signed decimal num
    if(ntc >> (nb - 1) & 1):
        return ntc - (1 << nb)
    return ntc


def decodeGenericFile(file_object_in, flag):
    # Function Definition: Decodes data from an inputted csv file object
    # Input: The file object and its type, eg. imu_data...not implemented at the moment
    # Output: Data Object

    returnDataObject = dataPacket()

    # Start at first line in file
    file_object_in.seek(0)
    fileObjectReader = csv.reader(file_object_in)
    if flag.find('1') != -1 or flag.find('2') != -1 or flag.find('3') != -1 or flag.find('4') != -1:
        next(fileObjectReader)
        next(fileObjectReader)
    if flag.find('1') != -1:
        dataParams = next(fileObjectReader)
        dataParams = next(fileObjectReader)
        returnDataObject.inputField = dataParams[0]
        returnDataObject.inputFieldAxis = dataParams[1]
    # Grab gain for each sensor from first line of file
    # Format should be Mag Cycle Count, Acc Range Index, Gyr Range Index
    next(fileObjectReader)
    dataParams = next(fileObjectReader)
    magGain = float(1000 / (0.3671 * int(dataParams[0], 16) + 1.5))
    if len(dataParams) != 2:
        accGain = float(2**-(int(dataParams[1], 16)) * 16384.00)
        gyrGain = float(2**-(int(dataParams[2], 16)) * 262.1)
    next(fileObjectReader)
    # Decode remaining data lines from file, placing into correct container
    for row in fileObjectReader:
        # Row[0] is the measurement number...not really needed
        returnDataObject.packetFlag.append(int(row[1], 16))
        returnDataObject.timestamp.append(
            float(int(row[2], 16) + (float(int(row[3], 16)) / 32768.00)))
        returnDataObject.mag1x.append(
            float(decode_twos_comp(int(row[4], 16), 24) * magGain))
        returnDataObject.mag1y.append(
            float(decode_twos_comp(int(row[5], 16), 24) * magGain))
        returnDataObject.mag1z.append(
            float(decode_twos_comp(int(row[6], 16), 24) * magGain))
        returnDataObject.mag2x.append(
            float(decode_twos_comp(int(row[7], 16), 24) * magGain))
        returnDataObject.mag2y.append(
            float(decode_twos_comp(int(row[8], 16), 24) * magGain))
        returnDataObject.mag2z.append(
            float(decode_twos_comp(int(row[9], 16), 24) * magGain))
        returnDataObject.mag3x.append(
            float(decode_twos_comp(int(row[10], 16), 24) * magGain))
        returnDataObject.mag3y.append(
            float(decode_twos_comp(int(row[11], 16), 24) * magGain))
        returnDataObject.mag3z.append(
            float(decode_twos_comp(int(row[12], 16), 24) * magGain))
        returnDataObject.mag4x.append(
            float(decode_twos_comp(int(row[13], 16), 24) * magGain))
        returnDataObject.mag4y.append(
            float(decode_twos_comp(int(row[14], 16), 24) * magGain))
        returnDataObject.mag4z.append(
            float(decode_twos_comp(int(row[15], 16), 24) * magGain))
        if int(row[1], 16) == 5 or int(row[1], 16) == 7:
            returnDataObject.accx.append(
                float(decode_twos_comp(int(row[16], 16), 16) / accGain))
            returnDataObject.accy.append(
                float(decode_twos_comp(int(row[17], 16), 16) / accGain))
            returnDataObject.accz.append(
                float(decode_twos_comp(int(row[18], 16), 16) / accGain))
            returnDataObject.gyrx.append(
                float(decode_twos_comp(int(row[19], 16), 16) / gyrGain))
            returnDataObject.gyry.append(
                float(decode_twos_comp(int(row[20], 16), 16) / gyrGain))
            returnDataObject.gyrz.append(
                float(decode_twos_comp(int(row[21], 16), 16) / gyrGain))
        if int(row[1], 16) == 5:
            returnDataObject.temp.append(
                float(((int(row[22], 16) * 2500) >> 12) - 500) / 10.0)
        elif int(row[1], 16) == 6:
            returnDataObject.temp.append(
                float(((int(row[16], 16) * 2500) >> 12) - 500) / 10.0)

        returnDataObject.dataIndex = returnDataObject.dataIndex + 1

    # Return the data container object

    return returnDataObject
