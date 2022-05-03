import numpy as np
import matplotlib.pyplot as plt
import data_processing_lib.Quad_Mag_Decoding as qmd
import scipy as sp
from scipy import signal, fft

# All plots, by default, will not have any x axis padding
plt.rcParams['axes.xmargin'] = 0

defaultSaveFigPath = 'data_storage/'

# This affects how data is processed and plotted

# Data will have the first and last 10% of data points removed i.e. if there is 100 data
# points, then 0-10 and 90-100 will be essentially chopped off the data set
CROP_DATA = 1 
# Removes only 0 and FF vals with zscore 3stdev above or below mean
REMOVE_OUTLIERS = 1
# Removes any vals with zscore 3stdev above mean (requires REMOVE_OUTLIERS)
REMOVE_ALL_OUTLIERS = 0 and REMOVE_OUTLIERS
# +/- num stdevs from the mean yaxis scale (4 means the y axis goes from mean-4stdev to mean+4stdev)
Y_BOUNDS_NUM_STDEV = 4
# Horizontal outlier cutoff line drawn on graphs
OUTLIERS_CUTTOFF_NUM_STDEV = 3 
# Plots each mag individually in addition to plotting the four averaged readings
PLOT_ALL_MAGS_INDIVIDUAL = 1


def plotCollectedData(flag):
    # Function Definition: Plots data from a well-formatted file
    # Input: Serial Object
    # Output: String that tells the caller the plots have been completed
    readFile = qmd.getReadFile(flag)
    plotData(readFile, flag)
    readFile.close()
    return "\nData has been processed and plotted"


def removeOutliers(data_arr):
    # Function Definition: Finds and removes outliers from a dataset
    # Input: Array of data
    # Output: Array containing the removed outliers
    outlierArr = []
    returnArr = np.asarray(data_arr)
    dataMean = np.average(np.asarray(data_arr))
    dataStd = np.std(np.asarray(data_arr))
    numOutliers = 0
    if CROP_DATA:
        print("Cropping data, will remove ~" + str(int(len(returnArr)/5)) + " data points\n")
        for index, data in enumerate(returnArr):
            if index <= int(len(returnArr) / 10) or index >= (len(returnArr) - int(len(returnArr) / 10)) :
                outlierArr.append(data)
                data_arr.remove(data)
                returnArr[index] = np.nan
                numOutliers += 1
    for index, data in enumerate(returnArr):
        z_score = (data - dataMean) / dataStd
        if np.abs(z_score) > 3:
            if REMOVE_ALL_OUTLIERS:
                outlierArr.append(data)
                data_arr.remove(data)
                returnArr[index] = np.nan
                numOutliers += 1
            elif data == 0 or data == 0xffffffff:
                outlierArr.append(data)
                data_arr.remove(data)
                returnArr[index] = np.nan
                numOutliers += 1

    print("Removed " + str(numOutliers) + " Outliers")
    return returnArr

#### Plotting Data ####


def plotAllMagData(data_object, fig_num):
    # Function Definition: Creates basic plots for mag data
    # Input: Data object and the figure number for file name
    # Output: None

    #while 1:
    #    allMagsAveraged = input("\nDo you want to plot data for the averaged four mags (Y/n)? ")
    #    if allMagsAveraged == 'Y' or allMagsAveraged == 'n':
    #        break
    #    else:
    #        print("\nInvalid input...try again")

    # Calculations and data adjustments
    quadMagX = (((np.asarray(data_object.mag1x)) + (np.asarray(data_object.mag2x)) +
                 (np.asarray(data_object.mag3x)) + (np.asarray(data_object.mag4x))) / 4.0).tolist()
    quadMagY = (((np.asarray(data_object.mag1y)) + (np.asarray(data_object.mag2y)) +
                 (np.asarray(data_object.mag3y)) + (np.asarray(data_object.mag4y))) / 4.0).tolist()
    quadMagZ = (((np.asarray(data_object.mag1z)) + (np.asarray(data_object.mag2z)) +
                 (np.asarray(data_object.mag3z)) + (np.asarray(data_object.mag4z))) / 4.0).tolist()
    quadMagTotalB = (np.sqrt(np.asarray(quadMagX)**2 +
                             np.asarray(quadMagY)**2 + np.asarray(quadMagZ)**2)).tolist()
    adjustedQuadMagX = np.asarray(quadMagX)
    adjustedQuadMagY = np.asarray(quadMagY)
    adjustedQuadMagZ = np.asarray(quadMagZ)
    adjustedquadMagTotalB = np.asarray(quadMagTotalB)
    mag1TotalB = (np.sqrt(np.asarray(data_object.mag1x)**2 +
                          np.asarray(data_object.mag1y)**2 + np.asarray(data_object.mag1z)**2)).tolist()
    adjustedMag1X = np.asarray(data_object.mag1x)
    adjustedMag1Y = np.asarray(data_object.mag1y)
    adjustedMag1Z = np.asarray(data_object.mag1z)
    adjustedMag1TotalB = np.asarray(mag1TotalB)
    mag2TotalB = (np.sqrt(np.asarray(data_object.mag2x)**2 +
                          np.asarray(data_object.mag2y)**2 + np.asarray(data_object.mag2z)**2)).tolist()
    adjustedMag2X = np.asarray(data_object.mag2x)
    adjustedMag2Y = np.asarray(data_object.mag2y)
    adjustedMag2Z = np.asarray(data_object.mag2z)
    adjustedMag2TotalB = np.asarray(mag2TotalB)
    mag3TotalB = (np.sqrt(np.asarray(data_object.mag3x)**2 +
                          np.asarray(data_object.mag3y)**2 + np.asarray(data_object.mag3z)**2)).tolist()
    adjustedMag3X = np.asarray(data_object.mag3x)
    adjustedMag3Y = np.asarray(data_object.mag3y)
    adjustedMag3Z = np.asarray(data_object.mag3z)
    adjustedMag3TotalB = np.asarray(mag3TotalB)
    mag4TotalB = (np.sqrt(np.asarray(data_object.mag4x)**2 +
                          np.asarray(data_object.mag4y)**2 + np.asarray(data_object.mag4z)**2)).tolist()
    adjustedMag4X = np.asarray(data_object.mag4x)
    adjustedMag4Y = np.asarray(data_object.mag4y)
    adjustedMag4Z = np.asarray(data_object.mag4z)
    adjustedMag4TotalB = np.asarray(mag4TotalB)
    if REMOVE_OUTLIERS:
        print("\nAdjusting All Mags Averaged X Axis Data Set")
        adjustedQuadMagX = removeOutliers(quadMagX)
        print("\nAdjusting All Mags Averaged Y Axis Data Set")
        adjustedQuadMagY = removeOutliers(quadMagY)
        print("\nAdjusting All Mags Averaged Z Axis Data Set")
        adjustedQuadMagZ = removeOutliers(quadMagZ)
        print("\nAdjusting All Mags Averaged |B| Data Set")
        adjustedquadMagTotalB = removeOutliers(quadMagTotalB)
        print("\nAdjusting Mag1 X Axis Data Set")
        adjustedMag1X = removeOutliers(data_object.mag1x)
        print("\nAdjusting Mag1 Y Axis Data Set")
        adjustedMag1Y = removeOutliers(data_object.mag1y)
        print("\nAdjusting Mag1 Z Axis Data Set")
        adjustedMag1Z = removeOutliers(data_object.mag1z)
        print("\nAdjusting Mag1 |B| Data Set")
        adjustedMag1TotalB = removeOutliers(mag1TotalB)
        print("\nAdjusting Mag2 X Axis Data Set")
        adjustedMag2X = removeOutliers(data_object.mag2x)
        print("\nAdjusting Mag2 Y Axis Data Set")
        adjustedMag2Y = removeOutliers(data_object.mag2y)
        print("\nAdjusting Mag2 Z Axis Data Set")
        adjustedMag2Z = removeOutliers(data_object.mag2z)
        print("\nAdjusting Mag2 |B| Data Set")
        adjustedMag2TotalB = removeOutliers(mag2TotalB)
        print("\nAdjusting Mag3 X Axis Data Set")
        adjustedMag3X = removeOutliers(data_object.mag3x)
        print("\nAdjusting Mag3 Y Axis Data Set")
        adjustedMag3Y = removeOutliers(data_object.mag3y)
        print("\nAdjusting Mag3 Z Axis Data Set")
        adjustedMag3Z = removeOutliers(data_object.mag3z)
        print("\nAdjusting Mag3 |B| Data Set")
        adjustedMag3TotalB = removeOutliers(mag3TotalB)
        print("\nAdjusting Mag4 X Axis Data Set")
        adjustedMag4X = removeOutliers(data_object.mag4x)
        print("\nAdjusting Mag4 Y Axis Data Set")
        adjustedMag4Y = removeOutliers(data_object.mag4y)
        print("\nAdjusting Mag4 Z Axis Data Set")
        adjustedMag4Z = removeOutliers(data_object.mag4z)
        print("\nAdjusting Mag4 |B| Data Set")
        adjustedMag4TotalB = removeOutliers(mag4TotalB)

    # Plotting all mags averaged data
    plt.figure(figsize=(16, 12))
    plt.margins(x=0)
    # Need to use an axis object to configure subplots correctly
    ax1 = plt.subplot(4, 1, 1)
    ax1.set_xlabel('System Time (s)')
    ax1.set_ylabel('B (nT)')
    ax1.set_title('QuadMag-X v Time')
    ax1.set_ylim(((np.average(np.asarray(quadMagX))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(quadMagX)))),
                 ((np.average(np.asarray(quadMagX))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(quadMagX)))))
    ax1.plot(data_object.timestamp, adjustedQuadMagX,
             c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(quadMagX))) + '\nStdev: ' + str(np.std(np.asarray(quadMagX)))))
    ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
        quadMagX)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(quadMagX)))), c='blue', marker="")
    ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
        quadMagX)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(quadMagX)))), c='blue', marker="")
    plt.legend(loc='lower right')
    ax2 = plt.subplot(4, 1, 2)
    ax2.set_xlabel('System Time (s)')
    ax2.set_ylabel('B (nT)')
    ax2.set_title('QuadMag-Y v Time')
    ax2.set_ylim(((np.average(np.asarray(quadMagY))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(quadMagY)))),
                 ((np.average(np.asarray(quadMagY))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(quadMagY)))))
    ax2.plot(data_object.timestamp, adjustedQuadMagY,
             c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(quadMagY))) + '\nStdev: ' + str(np.std(np.asarray(quadMagY)))))
    ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
        quadMagY)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(quadMagY)))), c='blue', marker="")
    ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
        quadMagY)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(quadMagY)))), c='blue', marker="")
    plt.legend(loc='lower right')
    ax3 = plt.subplot(4, 1, 3)
    ax3.set_xlabel('System Time (s)')
    ax3.set_ylabel('B (nT)')
    ax3.set_title('QuadMag-Z v Time')
    ax3.set_ylim(((np.average(np.asarray(quadMagZ))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(quadMagZ)))),
                 ((np.average(np.asarray(quadMagZ))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(quadMagZ)))))
    ax3.plot(data_object.timestamp, adjustedQuadMagZ,
             c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(quadMagZ))) + '\nStdev: ' + str(np.std(np.asarray(quadMagZ)))))
    ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
        quadMagZ)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(quadMagZ)))), c='blue', marker="")
    ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
        quadMagZ)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(quadMagZ)))), c='blue', marker="")
    plt.legend(loc='lower right')
    ax4 = plt.subplot(4, 1, 4)
    ax4.set_xlabel('System Time (s)')
    ax4.set_ylabel('B (nT)')
    ax4.set_title('QuadMag-|B| v Time')
    ax4.set_ylim(((np.average(np.asarray(quadMagTotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(quadMagTotalB)))),
                 ((np.average(np.asarray(quadMagTotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(quadMagTotalB)))))
    ax4.plot(data_object.timestamp, adjustedquadMagTotalB,
             c='m', marker="", label=str('Average: ' + str(np.average(np.asarray(quadMagTotalB))) + '\nStdev: ' + str(np.std(np.asarray(quadMagTotalB)))))
    ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(quadMagTotalB)
                                                                                   ) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(quadMagTotalB)))), c='blue', marker="")
    ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(quadMagTotalB)
                                                                                   ) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(quadMagTotalB)))), c='blue', marker="")
    plt.legend(loc='lower right')
    plt.tight_layout(h_pad=2.0)
    # plt.show()
    figName = "QuadMag_Data_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)

    # Individual Mag Plots
    if PLOT_ALL_MAGS_INDIVIDUAL:
        # Mag 1
        plt.figure(figsize=(16, 12))
        plt.margins(x=0)
        ax1 = plt.subplot(4, 1, 1)
        ax1.set_xlabel('System Time (s)')
        ax1.set_ylabel('B (nT)')
        ax1.set_title('Mag1-BX v Time')
        ax2 = plt.subplot(4, 1, 2)
        ax2.set_xlabel('System Time (s)')
        ax2.set_ylabel('B (nT)')
        ax2.set_title('Mag1-BY v Time')
        ax3 = plt.subplot(4, 1, 3)
        ax3.set_xlabel('System Time (s)')
        ax3.set_ylabel('B (nT)')
        ax3.set_title('Mag1-BZ v Time')
        ax4 = plt.subplot(4, 1, 4)
        ax4.set_xlabel('System Time (s)')
        ax4.set_ylabel('B (nT)')
        ax4.set_title('Mag1-|B| v Time')
        ax1.plot(data_object.timestamp, adjustedMag1X,
                 c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag1x))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag1x)))))
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1x)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1x)))), c='blue', marker="")
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1x)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1x)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, adjustedMag1Y,
                 c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag1y))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag1y)))))
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1y)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1y)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1y)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1y)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, adjustedMag1Z,
                 c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag1z))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag1z)))))
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1z)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1z)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1z)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1z)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, adjustedMag1TotalB,
                 c='m', marker="", label=str('Average: ' + str(np.average(mag1TotalB)) + '\nStdev: ' + str(np.std(mag1TotalB))))
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag1TotalB)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag1TotalB)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag1TotalB)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag1TotalB)))), c='blue', marker="")
        ax1.set_ylim(((np.average(np.asarray(data_object.mag1x))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1x)))),
                     ((np.average(np.asarray(data_object.mag1x))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1x)))))
        ax2.set_ylim(((np.average(np.asarray(data_object.mag1y))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1y)))),
                     ((np.average(np.asarray(data_object.mag1y))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1y)))))
        ax3.set_ylim(((np.average(np.asarray(data_object.mag1z))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1z)))),
                     ((np.average(np.asarray(data_object.mag1z))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1z)))))
        ax4.set_ylim(((np.average(np.asarray(mag1TotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag1TotalB)))),
                     ((np.average(np.asarray(mag1TotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag1TotalB)))))
        ax1.legend(loc='lower right')
        ax2.legend(loc='lower right')
        ax3.legend(loc='lower right')
        ax4.legend(loc='lower right')
        plt.tight_layout(h_pad=2.0)
        # plt.show()
        figName = "Mag_1_Data_" + str(fig_num) + ".png"
        plt.savefig(defaultSaveFigPath + '/' + figName)

        # Mag 2
        plt.figure(figsize=(16, 12))
        plt.margins(x=0)
        ax1 = plt.subplot(4, 1, 1)
        ax1.set_xlabel('System Time (s)')
        ax1.set_ylabel('B (nT)')
        ax1.set_title('Mag2-BX v Time')
        ax2 = plt.subplot(4, 1, 2)
        ax2.set_xlabel('System Time (s)')
        ax2.set_ylabel('B (nT)')
        ax2.set_title('Mag2-BY v Time')
        ax3 = plt.subplot(4, 1, 3)
        ax3.set_xlabel('System Time (s)')
        ax3.set_ylabel('B (nT)')
        ax3.set_title('Mag2-BZ v Time')
        ax4 = plt.subplot(4, 1, 4)
        ax4.set_xlabel('System Time (s)')
        ax4.set_ylabel('B (nT)')
        ax4.set_title('Mag2-|B| v Time')
        ax1.plot(data_object.timestamp, adjustedMag2X,
                 c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag2x))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag2x)))))
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2x)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2x)))), c='blue', marker="")
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2x)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2x)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, adjustedMag2Y,
                 c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag2y))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag2y)))))
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2y)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2y)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2y)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2y)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, adjustedMag2Z,
                 c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag2z))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag2z)))))
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2z)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2z)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2z)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2z)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, adjustedMag2TotalB,
                 c='m', marker="", label=str('Average: ' + str(np.average(mag2TotalB)) + '\nStdev: ' + str(np.std(mag2TotalB))))
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag2TotalB)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag2TotalB)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag2TotalB)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag2TotalB)))), c='blue', marker="")
        ax1.set_ylim(((np.average(np.asarray(data_object.mag2x))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2x)))),
                     ((np.average(np.asarray(data_object.mag2x))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2x)))))
        ax2.set_ylim(((np.average(np.asarray(data_object.mag2y))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2y)))),
                     ((np.average(np.asarray(data_object.mag2y))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2y)))))
        ax3.set_ylim(((np.average(np.asarray(data_object.mag2z))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2z)))),
                     ((np.average(np.asarray(data_object.mag2z))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2z)))))
        ax4.set_ylim(((np.average(np.asarray(mag2TotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag2TotalB)))),
                     ((np.average(np.asarray(mag2TotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag2TotalB)))))
        ax1.legend(loc='lower right')
        ax2.legend(loc='lower right')
        ax3.legend(loc='lower right')
        ax4.legend(loc='lower right')
        plt.tight_layout(h_pad=2.0)
        # plt.show()
        figName = "Mag_2_Data_" + str(fig_num) + ".png"
        plt.savefig(defaultSaveFigPath + '/' + figName)

        # Mag 3
        plt.figure(figsize=(16, 12))
        plt.margins(x=0)
        ax1 = plt.subplot(4, 1, 1)
        ax1.set_xlabel('System Time (s)')
        ax1.set_ylabel('B (nT)')
        ax1.set_title('Mag3-BX v Time')
        ax2 = plt.subplot(4, 1, 2)
        ax2.set_xlabel('System Time (s)')
        ax2.set_ylabel('B (nT)')
        ax2.set_title('Mag3-BY v Time')
        ax3 = plt.subplot(4, 1, 3)
        ax3.set_xlabel('System Time (s)')
        ax3.set_ylabel('B (nT)')
        ax3.set_title('Mag3-BZ v Time')
        ax4 = plt.subplot(4, 1, 4)
        ax4.set_xlabel('System Time (s)')
        ax4.set_ylabel('B (nT)')
        ax4.set_title('Mag3-|B| v Time')
        ax1.plot(data_object.timestamp, adjustedMag3X,
                 c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag3x))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag3x)))))
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3x)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3x)))), c='blue', marker="")
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3x)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3x)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, adjustedMag3Y,
                 c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag3y))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag3y)))))
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3y)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3y)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3y)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3y)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, adjustedMag3Z,
                 c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag3z))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag3z)))))
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3z)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3z)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3z)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3z)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, adjustedMag3TotalB,
                 c='m', marker="", label=str('Average: ' + str(np.average(mag3TotalB)) + '\nStdev: ' + str(np.std(mag3TotalB))))
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag3TotalB)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag3TotalB)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag3TotalB)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag3TotalB)))), c='blue', marker="")
        ax1.set_ylim(((np.average(np.asarray(data_object.mag3x))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3x)))),
                     ((np.average(np.asarray(data_object.mag3x))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3x)))))
        ax2.set_ylim(((np.average(np.asarray(data_object.mag3y))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3y)))),
                     ((np.average(np.asarray(data_object.mag3y))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3y)))))
        ax3.set_ylim(((np.average(np.asarray(data_object.mag3z))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3z)))),
                     ((np.average(np.asarray(data_object.mag3z))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3z)))))
        ax4.set_ylim(((np.average(np.asarray(mag3TotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag3TotalB)))),
                     ((np.average(np.asarray(mag3TotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag3TotalB)))))
        ax1.legend(loc='lower right')
        ax2.legend(loc='lower right')
        ax3.legend(loc='lower right')
        ax4.legend(loc='lower right')
        plt.tight_layout(h_pad=2.0)
        # plt.show()
        figName = "Mag_3_Data_" + str(fig_num) + ".png"
        plt.savefig(defaultSaveFigPath + '/' + figName)

        # Mag 4
        plt.figure(figsize=(16, 12))
        plt.margins(x=0)
        ax1 = plt.subplot(4, 1, 1)
        ax1.set_xlabel('System Time (s)')
        ax1.set_ylabel('B (nT)')
        ax1.set_title('Mag4-BX v Time')
        ax2 = plt.subplot(4, 1, 2)
        ax2.set_xlabel('System Time (s)')
        ax2.set_ylabel('B (nT)')
        ax2.set_title('Mag4-BY v Time')
        ax3 = plt.subplot(4, 1, 3)
        ax3.set_xlabel('System Time (s)')
        ax3.set_ylabel('B (nT)')
        ax3.set_title('Mag4-BZ v Time')
        ax4 = plt.subplot(4, 1, 4)
        ax4.set_xlabel('System Time (s)')
        ax4.set_ylabel('B (nT)')
        ax4.set_title('Mag4-|B| v Time')
        ax1.plot(data_object.timestamp, adjustedMag4X,
                 c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag4x))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag4x)))))
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4x)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4x)))), c='blue', marker="")
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4x)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4x)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, adjustedMag4Y,
                 c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag4y))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag4y)))))
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4y)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4y)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4y)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4y)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, adjustedMag4Z,
                 c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag4z))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag4z)))))
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4z)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4z)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4z)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4z)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, adjustedMag4TotalB,
                 c='m', marker="", label=str('Average: ' + str(np.average(mag4TotalB)) + '\nStdev: ' + str(np.std(mag4TotalB))))
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag4TotalB)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag4TotalB)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag4TotalB)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag4TotalB)))), c='blue', marker="")
        ax1.set_ylim(((np.average(np.asarray(data_object.mag4x))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4x)))),
                     ((np.average(np.asarray(data_object.mag4x))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4x)))))
        ax2.set_ylim(((np.average(np.asarray(data_object.mag4y))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4y)))),
                     ((np.average(np.asarray(data_object.mag4y))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4y)))))
        ax3.set_ylim(((np.average(np.asarray(data_object.mag4z))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4z)))),
                     ((np.average(np.asarray(data_object.mag4z))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4z)))))
        ax4.set_ylim(((np.average(np.asarray(mag4TotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag4TotalB)))),
                     ((np.average(np.asarray(mag4TotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag4TotalB)))))
        ax1.legend(loc='lower right')
        ax2.legend(loc='lower right')
        ax3.legend(loc='lower right')
        ax4.legend(loc='lower right')
        plt.tight_layout(h_pad=2.0)
        # plt.show()
        figName = "Mag_4_Data_" + str(fig_num) + ".png"
        plt.savefig(defaultSaveFigPath + '/' + figName)

    # Print some stats to the console
    print("\n\nMag1 Average B-field X component: " +
          str(np.average(np.asarray(data_object.mag1x))))
    print("Mag1 Average B-field Y component: " +
          str(np.average(np.asarray(data_object.mag1y))))
    print("Mag1 Average B-field Z component: " +
          str(np.average(np.asarray(data_object.mag1z))))
    print("Mag1 Average B-field: " + str(np.average(mag1TotalB)))
    print("Mag2 Average B-field X component: " +
          str(np.average(np.asarray(data_object.mag2x))))
    print("Mag2 Average B-field Y component: " +
          str(np.average(np.asarray(data_object.mag2y))))
    print("Mag2 Average B-field Z component: " +
          str(np.average(np.asarray(data_object.mag2z))))
    print("Mag2 Average B-field: " + str(np.average(mag2TotalB)))
    print("Mag3 Average B-field X component: " +
          str(np.average(np.asarray(data_object.mag3x))))
    print("Mag3 Average B-field Y component: " +
          str(np.average(np.asarray(data_object.mag3y))))
    print("Mag3 Average B-field Z component: " +
          str(np.average(np.asarray(data_object.mag3z))))
    print("Mag3 Average B-field: " + str(np.average(mag3TotalB)))
    print("Mag4 Average B-field X component: " +
          str(np.average(np.asarray(data_object.mag4x))))
    print("Mag4 Average B-field Y component: " +
          str(np.average(np.asarray(data_object.mag4y))))
    print("Mag4 Average B-field Z component: " +
          str(np.average(np.asarray(data_object.mag4z))))
    print("Mag4 Average B-field: " + str(np.average(mag4TotalB)))
    print("All mags average B-field: " + str(np.average(quadMagTotalB)))
    print("\n")


def plotSingleMagData(data_object, fig_num):
    # Function Definition: Creates basic plots for data from a single mag
    # Input: Data object and the figure number for file name
    # Output: None

    # Magnetometer Data
    while 1:
        magNum = input("\nWhat mag do you want to plot data for (1-4)? ")
        if int(magNum) >= 1 and int(magNum) <= 4:
            break
        else:
            print("\nNumber is outside allowed bounds...try again\n")
    # Basic plot setup
    plt.figure(figsize=(16, 12))
    ax1 = plt.subplot(4, 1, 1)
    ax1.set_xlabel('System Time (s)')
    ax1.set_ylabel('B (nT)')
    ax1.set_title('Mag' + magNum + '-BX v Time')
    ax2 = plt.subplot(4, 1, 2)
    ax2.set_xlabel('System Time (s)')
    ax2.set_ylabel('B (nT)')
    ax2.set_title('Mag' + magNum + '-BY v Time')
    ax3 = plt.subplot(4, 1, 3)
    ax3.set_xlabel('System Time (s)')
    ax3.set_ylabel('B (nT)')
    ax3.set_title('Mag' + magNum + '-BZ v Time')
    ax4 = plt.subplot(4, 1, 4)
    ax4.set_xlabel('System Time (s)')
    ax4.set_ylabel('B (nT)')
    ax4.set_title('Mag' + magNum + '-|B| v Time')
    if int(magNum) == 1:
        mag1TotalB = (np.sqrt(np.asarray(data_object.mag1x)**2 + np.asarray(
            data_object.mag1y)**2 + np.asarray(data_object.mag1z)**2)).tolist()
        adjustedMag1X = np.asarray(data_object.mag1x)
        adjustedMag1Y = np.asarray(data_object.mag1y)
        adjustedMag1Z = np.asarray(data_object.mag1z)
        adjustedMag1TotalB = np.asarray(mag1TotalB)
        # Remove outliers
        if REMOVE_OUTLIERS:
            print("\nAdjusting Mag1 X Axis Data Set")
            adjustedMag1X = removeOutliers(data_object.mag1x)
            print("\nAdjusting Mag1 Y Axis Data Set")
            adjustedMag1Y = removeOutliers(data_object.mag1y)
            print("\nAdjusting Mag1 Z Axis Data Set")
            adjustedMag1Z = removeOutliers(data_object.mag1z)
            print("\nAdjusting Mag1 |B| Data Set")
            adjustedMag1TotalB = removeOutliers(mag1TotalB)
        # Plot adjusted data
        ax1.plot(data_object.timestamp, adjustedMag1X,
                 c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag1x))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag1x)))))
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1x)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1x)))), c='blue', marker="")
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1x)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1x)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, adjustedMag1Y,
                 c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag1y))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag1y)))))
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1y)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1y)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1y)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1y)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, adjustedMag1Z,
                 c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag1z))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag1z)))))
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1z)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1z)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag1z)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1z)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, adjustedMag1TotalB,
                 c='m', marker="", label=str('Average: ' + str(np.average(mag1TotalB)) + '\nStdev: ' + str(np.std(mag1TotalB))))
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag1TotalB)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag1TotalB)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag1TotalB)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag1TotalB)))), c='blue', marker="")
        ax1.set_ylim(((np.average(np.asarray(data_object.mag1x))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1x)))),
                     ((np.average(np.asarray(data_object.mag1x))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1x)))))
        ax2.set_ylim(((np.average(np.asarray(data_object.mag1y))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1y)))),
                     ((np.average(np.asarray(data_object.mag1y))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1y)))))
        ax3.set_ylim(((np.average(np.asarray(data_object.mag1z))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1z)))),
                     ((np.average(np.asarray(data_object.mag1z))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag1z)))))
        ax4.set_ylim(((np.average(np.asarray(mag1TotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag1TotalB)))),
                     ((np.average(np.asarray(mag1TotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag1TotalB)))))
        # Print some stats to the command line
        print("\n\nMag1 Average B-field X component: " +
              str(np.average(np.asarray(data_object.mag1x))))
        print("Mag1 Average B-field Y component: " +
              str(np.average(np.asarray(data_object.mag1y))))
        print("Mag1 Average B-field Z component: " +
              str(np.average(np.asarray(data_object.mag1z))))
        print("Mag1 Average |B|-field: " +
              str(np.average(np.asarray(mag1TotalB))))
    elif int(magNum) == 2:
        mag2TotalB = (np.sqrt(np.asarray(data_object.mag2x)**2 + np.asarray(
            data_object.mag2y)**2 + np.asarray(data_object.mag2z)**2)).tolist()
        adjustedMag2X = np.asarray(data_object.mag2x)
        adjustedMag2Y = np.asarray(data_object.mag2y)
        adjustedMag2Z = np.asarray(data_object.mag2z)
        adjustedMag2TotalB = np.asarray(mag2TotalB)
        # Remove outliers
        if REMOVE_OUTLIERS:
            print("\nAdjusting Mag2 X Axis Data Set")
            adjustedMag2X = removeOutliers(data_object.mag2x)
            print("\nAdjusting Mag2 Y Axis Data Set")
            adjustedMag2Y = removeOutliers(data_object.mag2y)
            print("\nAdjusting Mag2 Z Axis Data Set")
            adjustedMag2Z = removeOutliers(data_object.mag2z)
            print("\nAdjusting Mag2 |B| Data Set")
            adjustedMag2TotalB = removeOutliers(mag2TotalB)
        # Plot adjusted data
        ax1.plot(data_object.timestamp, adjustedMag2X,
                 c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag2x))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag2x)))))
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2x)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2x)))), c='blue', marker="")
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2x)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2x)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, adjustedMag2Y,
                 c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag2y))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag2y)))))
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2y)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2y)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2y)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2y)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, adjustedMag2Z,
                 c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag2z))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag2z)))))
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2z)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2z)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag2z)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2z)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, adjustedMag2TotalB,
                 c='m', marker="", label=str('Average: ' + str(np.average(mag2TotalB)) + '\nStdev: ' + str(np.std(mag2TotalB))))
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag2TotalB)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag2TotalB)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag2TotalB)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag2TotalB)))), c='blue', marker="")
        ax1.set_ylim(((np.average(np.asarray(data_object.mag2x))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2x)))),
                     ((np.average(np.asarray(data_object.mag2x))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2x)))))
        ax2.set_ylim(((np.average(np.asarray(data_object.mag2y))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2y)))),
                     ((np.average(np.asarray(data_object.mag2y))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2y)))))
        ax3.set_ylim(((np.average(np.asarray(data_object.mag2z))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2z)))),
                     ((np.average(np.asarray(data_object.mag2z))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag2z)))))
        ax4.set_ylim(((np.average(np.asarray(mag2TotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag2TotalB)))),
                     ((np.average(np.asarray(mag2TotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag2TotalB)))))
        # Print some stats to the command line
        print("\n\nMag2 Average B-field X component: " +
              str(np.average(np.asarray(data_object.mag2x))))
        print("Mag2 Average B-field Y component: " +
              str(np.average(np.asarray(data_object.mag2y))))
        print("Mag2 Average B-field Z component: " +
              str(np.average(np.asarray(data_object.mag2z))))
        print("Mag2 Average |B|-field: " +
              str(np.average(np.asarray(mag2TotalB))))
    elif int(magNum) == 3:
        mag3TotalB = (np.sqrt(np.asarray(data_object.mag3x)**2 + np.asarray(
            data_object.mag3y)**2 + np.asarray(data_object.mag3z)**2)).tolist()
        adjustedMag3X = np.asarray(data_object.mag3x)
        adjustedMag3Y = np.asarray(data_object.mag3y)
        adjustedMag3Z = np.asarray(data_object.mag3z)
        adjustedMag3TotalB = np.asarray(mag3TotalB)
        # Remove outliers
        if REMOVE_OUTLIERS:
            print("\nAdjusting Mag3 X Axis Data Set")
            adjustedMag3X = removeOutliers(data_object.mag3x)
            print("\nAdjusting Mag3 Y Axis Data Set")
            adjustedMag3Y = removeOutliers(data_object.mag3y)
            print("\nAdjusting Mag3 Z Axis Data Set")
            adjustedMag3Z = removeOutliers(data_object.mag3z)
            print("\nAdjusting Mag3 |B| Data Set")
            adjustedMag3TotalB = removeOutliers(mag3TotalB)
        # Plot adjusted data
        ax1.plot(data_object.timestamp, adjustedMag3X,
                 c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag3x))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag3x)))))
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3x)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3x)))), c='blue', marker="")
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3x)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3x)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, adjustedMag3Y,
                 c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag3y))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag3y)))))
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3y)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3y)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3y)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3y)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, adjustedMag3Z,
                 c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag3z))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag3z)))))
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3z)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3z)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag3z)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3z)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, adjustedMag3TotalB,
                 c='m', marker="", label=str('Average: ' + str(np.average(mag3TotalB)) + '\nStdev: ' + str(np.std(mag3TotalB))))
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag3TotalB)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag3TotalB)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag3TotalB)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag3TotalB)))), c='blue', marker="")
        ax1.set_ylim(((np.average(np.asarray(data_object.mag3x))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3x)))),
                     ((np.average(np.asarray(data_object.mag3x))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3x)))))
        ax2.set_ylim(((np.average(np.asarray(data_object.mag3y))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3y)))),
                     ((np.average(np.asarray(data_object.mag3y))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3y)))))
        ax3.set_ylim(((np.average(np.asarray(data_object.mag3z))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3z)))),
                     ((np.average(np.asarray(data_object.mag3z))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag3z)))))
        ax4.set_ylim(((np.average(np.asarray(mag3TotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag3TotalB)))),
                     ((np.average(np.asarray(mag3TotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag3TotalB)))))
        # Print some stats to the command line
        print("\n\nMag3 Average B-field X component: " +
              str(np.average(np.asarray(data_object.mag3x))))
        print("Mag3 Average B-field Y component: " +
              str(np.average(np.asarray(data_object.mag3y))))
        print("Mag3 Average B-field Z component: " +
              str(np.average(np.asarray(data_object.mag3z))))
        print("Mag3 Average |B|-field: " +
              str(np.average(np.asarray(mag3TotalB))))
    else:
        mag4TotalB = (np.sqrt(np.asarray(data_object.mag4x)**2 + np.asarray(
            data_object.mag4y)**2 + np.asarray(data_object.mag4z)**2)).tolist()
        adjustedMag4X = np.asarray(data_object.mag4x)
        adjustedMag4Y = np.asarray(data_object.mag4y)
        adjustedMag4Z = np.asarray(data_object.mag4z)
        adjustedMag4TotalB = np.asarray(mag4TotalB)
        # Remove outliers
        if REMOVE_OUTLIERS:
            print("\nAdjusting Mag4 X Axis Data Set")
            adjustedMag4X = removeOutliers(data_object.mag4x)
            print("\nAdjusting Mag4 Y Axis Data Set")
            adjustedMag4Y = removeOutliers(data_object.mag4y)
            print("\nAdjusting Mag4 Z Axis Data Set")
            adjustedMag4Z = removeOutliers(data_object.mag4z)
            print("\nAdjusting Mag4 |B| Data Set")
            adjustedMag4TotalB = removeOutliers(mag4TotalB)
        # Plot adjusted data
        ax1.plot(data_object.timestamp, adjustedMag4X,
                 c='red', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag4x))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag4x)))))
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4x)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4x)))), c='blue', marker="")
        ax1.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4x)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4x)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, adjustedMag4Y,
                 c='green', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag4y))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag4y)))))
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4y)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4y)))), c='blue', marker="")
        ax2.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4y)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4y)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, adjustedMag4Z,
                 c='orange', marker="", label=str('Average: ' + str(np.average(np.asarray(data_object.mag4z))) + '\nStdev: ' + str(np.std(np.asarray(data_object.mag4z)))))
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4z)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4z)))), c='blue', marker="")
        ax3.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            data_object.mag4z)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4z)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, adjustedMag4TotalB,
                 c='m', marker="", label=str('Average: ' + str(np.average(mag4TotalB)) + '\nStdev: ' + str(np.std(mag4TotalB))))
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag4TotalB)) - OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag4TotalB)))), c='blue', marker="")
        ax4.plot(data_object.timestamp, np.full(len(data_object.timestamp), np.average(np.asarray(
            mag4TotalB)) + OUTLIERS_CUTTOFF_NUM_STDEV*abs(np.std(np.asarray(mag4TotalB)))), c='blue', marker="")
        ax1.set_ylim(((np.average(np.asarray(data_object.mag4x))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4x)))),
                     ((np.average(np.asarray(data_object.mag4x))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4x)))))
        ax2.set_ylim(((np.average(np.asarray(data_object.mag4y))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4y)))),
                     ((np.average(np.asarray(data_object.mag4y))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4y)))))
        ax3.set_ylim(((np.average(np.asarray(data_object.mag4z))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4z)))),
                     ((np.average(np.asarray(data_object.mag4z))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(data_object.mag4z)))))
        ax4.set_ylim(((np.average(np.asarray(mag4TotalB))) - Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag4TotalB)))),
                     ((np.average(np.asarray(mag4TotalB))) + Y_BOUNDS_NUM_STDEV*abs(np.std(np.asarray(mag4TotalB)))))
        # Print some stats to the command line
        print("\n\nMag4 Average B-field X component: " +
              str(np.average(np.asarray(data_object.mag4x))))
        print("Mag4 Average B-field Y component: " +
              str(np.average(np.asarray(data_object.mag4y))))
        print("Mag4 Average B-field Z component: " +
              str(np.average(np.asarray(data_object.mag4z))))
        print("Mag4 Average |B|-field: " +
              str(np.average(np.asarray(mag4TotalB))))
    print("\n")
    ax1.legend(loc='lower right')
    ax2.legend(loc='lower right')
    ax3.legend(loc='lower right')
    ax4.legend(loc='lower right')
    plt.tight_layout(h_pad=2.0)
    # plt.show()
    figName = "Mag_" + magNum + "_Data_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)


def plotImuData(data_object, fig_num):
    # Function Definition: Creates basic plots for imu data
    # Input: Data object and the figure number for file name
    # Output: None

    # Accelerometer Data (range of sensor is -8 to 8 g's)
    plt.figure(figsize=(16, 12))
    ax1 = plt.subplot(2, 3, 1)
    ax1.set_xlabel('System Time (s)')
    ax1.set_ylabel('Acceleration (g)')
    ax1.set_title('Acc-X v Time')
    # ax1.set_ylim(-4, 4)
    ax1.scatter(data_object.timestamp, data_object.accx, c='r', marker=".")
    ax2 = plt.subplot(2, 3, 2)
    ax2.set_xlabel('System Time (s)')
    ax2.set_ylabel('Acceleration (g)')
    ax2.set_title('Acc-Y v Time')
    # ax2.set_ylim(-4, 4)
    ax2.scatter(data_object.timestamp, data_object.accy, c='g', marker=".")
    ax3 = plt.subplot(2, 3, 3)
    ax3.set_xlabel('System Time (s)')
    ax3.set_ylabel('Acceleration (g)')
    ax3.set_title('Acc-Z v Time')
    # ax3.set_ylim(-4, 4)
    ax3.scatter(data_object.timestamp, data_object.accz, c='b', marker=".")
    ax4 = plt.subplot(2, 1, 2)
    ax4.set_xlabel('System Time (s)')
    ax4.set_ylabel('Acceleration (g)')
    ax4.set_title('Acc-XYZ v Time')
    # ax4.set_ylim(-4, 4)
    ax4.scatter(data_object.timestamp, data_object.accx,
                c='r', marker='.', label='X')
    ax4.scatter(data_object.timestamp, data_object.accy,
                c='g', marker='.', label='Y')
    ax4.scatter(data_object.timestamp, data_object.accz,
                c='b', marker='.', label='Z')
    figName = "Acc_Data_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)
    # Gyroscope Data (range of sensor is -360 to 360 deg/s)
    plt.figure(figsize=(16, 12))
    ax1 = plt.subplot(2, 3, 1)
    ax1.set_xlabel('System Time (s)')
    ax1.set_ylabel('Angular Velocity (Deg/s)')
    ax1.set_title('Gyr-X v Time')
    # ax1.set_ylim(-60, 60)
    ax1.scatter(data_object.timestamp, data_object.gyrx, c='r', marker=".")
    ax2 = plt.subplot(2, 3, 2)
    ax2.set_xlabel('System Time (s)')
    ax2.set_ylabel('Angular Velocity (Deg/s)')
    ax2.set_title('Gyr-Y v Time')
    # ax2.set_ylim(-60, 60)
    ax2.scatter(data_object.timestamp, data_object.gyry, c='g', marker=".")
    ax3 = plt.subplot(2, 3, 3)
    ax3.set_xlabel('System Time (s)')
    ax3.set_ylabel('Angular Velocity (Deg/s)')
    ax3.set_title('Gyr-Z v Time')
    # ax3.set_ylim(-60, 60)
    ax3.scatter(data_object.timestamp, data_object.gyrz, c='b', marker=".")
    ax4 = plt.subplot(2, 1, 2)
    ax4.set_xlabel('System Time (s)')
    ax4.set_ylabel('Angular Velocity (Deg/s)')
    ax4.set_title('Gyr-XYZ v Time')
    # ax4.set_ylim(-60, 60)
    ax4.scatter(data_object.timestamp, data_object.gyrx,
                c='r', marker='.', label='X')
    ax4.scatter(data_object.timestamp, data_object.gyry,
                c='g', marker='.', label='Y')
    ax4.scatter(data_object.timestamp, data_object.gyrz,
                c='b', marker='.', label='Z')
    figName = "Gyr_Data_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)


def plotTempData(data_object, fig_num):
    # Function Definition: Creates basic plots for temp data
    # Input: Data object and the figure number for file name
    # Output: None

    # Temperature Data (range of sensor is -60 to 120 degrees c)
    plt.figure(figsize=(16, 12))
    ax1 = plt.subplot(111)
    ax1.set_xlabel('System Time (s)')
    ax1.set_ylabel('Temperature (c)')
    ax1.set_title('Temperature v Time')
    # ax1.set_ylim(-20, 50)
    ax1.scatter(data_object.timestamp, data_object.temp, c='r', marker=".")
    figName = "Temp_Data_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)


def plotAllData(data_object, fig_num):
    plotImuData(data_object, fig_num)
    plotTempData(data_object, fig_num)
    plotMagPowerSpectralDensity(data_object, fig_num)
    plotAllMagData(data_object, fig_num)
    plotTimeData(data_object, fig_num)


def plotLinearityAnalysis(data_object, fig_num):
    inF = np.array(data_object.inputField)
    x = np.array(data_object.medMagX)
    y = np.array(data_object.medMagY)
    z = np.array(data_object.medMagZ)
    mx, mxb = np.polyfit(inF, x, 1)
    my, myb = np.polyfit(inF, y, 1)
    mz, mzb = np.polyfit(inF, z, 1)
    plt.figure(figsize=(16, 12))
    ax1 = plt.subplot(111)
    ax1.set_xlabel('Input Field (nT)')
    ax1.set_ylabel('Measured Field (nT)')
    if(data_object.axis == "x"):
        ax1.set_title('X-axis Linearity (slope: {mx}, offset: {mxb}')
    elif(data_object.axis == "y"):
        ax1.set_title('Y-axis Linearity (slope: {my}, offset: {myb}')
    elif(data_object.axis == "z"):
        ax1.set_title('Z-axis Linearity (slope: {mz}, offset: {mzb}')
    ax1.plot(inF, (mx*inF + mxb), c='r', marker='.', label='X-Axis')
    ax1.plot(inF, (my*inF + myb), c='g', marker='.', label='Y-Axis')
    ax1.plot(inF, (mz*inF + mzb), c='b', marker='.', label='Z-Axis')
    figName = "Linearity_Test" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)


def plotStabilityAnalysis(data_object, fig_num):
    plt.figure(figsize=(16, 12))
    ax1 = plt.subplot(111)
    ax1.set_xlabel('B (nT)')
    ax1.set_ylabel('Number of data points')
    ax1.set_title('Stability Analysis of Four PNI Magnetometers')
    ax1.hist(data_object.mag1x, data_object.mag1y, data_object.mag1z, data_object.mag2x, data_object.mag2y, data_object.mag2z,
             data_object.mag3x, data_object.mag3y, data_object.mag3z, data_object.mag4x, data_object.mag4y, data_object.mag4z)
    figName = "Stability_Mag_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)
    plt.figure(figsize=(16, 12))
    ax1 = plt.subplot(211)
    ax1.set_xlabel('Acceleration (g)')
    ax1.set_ylabel('Number of data points')
    ax1.set_title('Stability Analysis of BMI270 IMU-Accelerometer')
    ax1.hist(data_object.accx, data_object.accy, data_object.accz)
    ax2 = plt.subplot(212)
    ax2.set_xlabel('Angular Velocity (Deg/s)')
    ax2.set_ylabel('Number of data points')
    ax2.set_title('Stability Analysis of BMI270 IMU-Gyroscope')
    ax2.hist(data_object.gyrx, data_object.gyry, data_object.gyrz)
    figName = "Stability_IMU_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)
    plt.figure(figsize=(16, 12))
    ax1 = plt.subplot(111)
    ax1.set_xlabel('Temperature (c)')
    ax1.set_ylabel('Number of data points')
    ax1.set_title('Stability Analysis of TMP36 Temperature Sensor')
    ax1.hist(data_object.temp)
    figName = "Stability_TMP36_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)

def plotMagPowerSpectralDensity(data_object, fig_num):
    # Function Definition: Creates PSD for mag data (should expand to other data)
    # Input: Data object and the figure number for file name
    # Output: None

    # Calculations
    timeBetweenMeasurements = np.array(data_object.timestamp)[1:] - np.array(data_object.timestamp)[:-1]
    data_object.sampleRate = 1.0 / np.median(timeBetweenMeasurements)

    quadMagX = (((np.asarray(data_object.mag1x)) + (np.asarray(data_object.mag2x)) +
                 (np.asarray(data_object.mag3x)) + (np.asarray(data_object.mag4x))) / 4.0).tolist()
    quadMagY = (((np.asarray(data_object.mag1y)) + (np.asarray(data_object.mag2y)) +
                 (np.asarray(data_object.mag3y)) + (np.asarray(data_object.mag4y))) / 4.0).tolist()
    quadMagZ = (((np.asarray(data_object.mag1z)) + (np.asarray(data_object.mag2z)) +
                 (np.asarray(data_object.mag3z)) + (np.asarray(data_object.mag4z))) / 4.0).tolist()
    quadMagTotalB = (np.sqrt(np.asarray(quadMagX)**2 +
                             np.asarray(quadMagY)**2 + np.asarray(quadMagZ)**2)).tolist()
    mag1TotalB = (np.sqrt(np.asarray(data_object.mag1x)**2 +
                          np.asarray(data_object.mag1y)**2 + np.asarray(data_object.mag1z)**2)).tolist()
    mag2TotalB = (np.sqrt(np.asarray(data_object.mag2x)**2 +
                          np.asarray(data_object.mag2y)**2 + np.asarray(data_object.mag2z)**2)).tolist()
    mag3TotalB = (np.sqrt(np.asarray(data_object.mag3x)**2 +
                          np.asarray(data_object.mag3y)**2 + np.asarray(data_object.mag3z)**2)).tolist()
    mag4TotalB = (np.sqrt(np.asarray(data_object.mag4x)**2 +
                          np.asarray(data_object.mag4y)**2 + np.asarray(data_object.mag4z)**2)).tolist()
    # Plotting all mags averaged data
    plt.figure(figsize=(16, 12))
    plt.margins(x=0)
    # Need to use an axis object to configure subplots correctly
    ax1 = plt.subplot(4, 1, 1)
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Power Spectral Density (nT^2/Hz)')
    ax1.set_title('PSD Mag 1 X Component')
    fx, Px_den = signal.welch(signal.detrend(data_object.mag1x, type='constant'), data_object.sampleRate)
    ax1.semilogy(fx, Px_den)
    #plt.legend(loc='lower right')
    ax2 = plt.subplot(4, 1, 2)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Power Spectral Density (nT^2/Hz)')
    ax2.set_title('PSD Mag 1 Y Component')
    fy, Py_den = signal.welch(signal.detrend(data_object.mag1y, type='constant'), data_object.sampleRate)
    ax2.semilogy(fy, Py_den)
    ax3 = plt.subplot(4, 1, 3)
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Power Spectral Density (nT^2/Hz)')
    ax3.set_title('PSD Mag 1 Z Component')
    fz, Pz_den = signal.welch(signal.detrend(data_object.mag1z, type='constant'), data_object.sampleRate)
    ax3.semilogy(fz, Pz_den)
    ax4 = plt.subplot(4, 1, 4)
    ax4.set_xlabel('Frequency (Hz)')
    ax4.set_ylabel('Power Spectral Density (nT^2/Hz)')
    ax4.set_title('PSD Mag 1 Magnitude')
    fxyz, Pxyz_den = signal.welch(signal.detrend(mag1TotalB, type='constant'), data_object.sampleRate)
    ax4.semilogy(fxyz, Pxyz_den)
    plt.tight_layout(h_pad=2.0)
    #plt.show()
    figName = "Mag1_PSD_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)

    # Plotting all mags averaged data
    plt.figure(figsize=(16, 12))
    plt.margins(x=0)
    # Need to use an axis object to configure subplots correctly
    ax1 = plt.subplot(4, 1, 1)
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('')
    ax1.set_title('FFT Mag 1 X Component')
    ax1.plot(sp.fft.fftfreq(len(data_object.timestamp), 1.0/data_object.sampleRate), sp.fft.fft(signal.detrend(data_object.mag1x, type='constant')))
    ax2 = plt.subplot(4, 1, 2)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('')
    ax2.set_title('FFT Mag 1 Y Component')
    ax2.plot(sp.fft.fftfreq(len(data_object.timestamp), 1.0/data_object.sampleRate), sp.fft.fft(signal.detrend(data_object.mag1y, type='constant')))
    ax3 = plt.subplot(4, 1, 3)
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('')
    ax3.set_title('FFT Mag 1 Z Component')
    ax3.plot(sp.fft.fftfreq(len(data_object.timestamp), 1.0/data_object.sampleRate), sp.fft.fft(signal.detrend(data_object.mag1z, type='constant')))
    ax4 = plt.subplot(4, 1, 4)
    ax4.set_xlabel('Frequency (Hz)')
    ax4.set_ylabel('')
    ax4.set_title('FFT Mag 1 Magnitude')
    ax4.plot(sp.fft.fftfreq(len(data_object.timestamp), 1.0/data_object.sampleRate), sp.fft.fft(signal.detrend(mag1TotalB, type='constant')))
    plt.tight_layout(h_pad=2.0)
    #plt.show()
    figName = "Mag1_FFT_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)

def plotTimeData(data_object, fig_num) :
    # Function Definition: Analyze time steps provided by msp430
    # Input: Data object and the figure number for file name
    # Output: None
    timeBetweenMeasurements = np.array(data_object.timestamp)[1:] - np.array(data_object.timestamp)[:-1]
    print("\nMedian time (ms) between measurements " + str(np.median(timeBetweenMeasurements) * 1E3))
    print("Median sample rate (hz) " + str(1 / np.median(timeBetweenMeasurements)) + "\n")
    print("Mean time (ms) between measurements " + str(np.mean(timeBetweenMeasurements) * 1E3))
    print("Mean sample rate (hz) " + str(1 / np.mean(timeBetweenMeasurements)) + "\n")
    print("Std dev (ms) between measurements " + str(np.std(timeBetweenMeasurements) * 1E3) + "\n")
    plt.figure(figsize=(16, 12))
    plt.margins(x=0)
    plt.hist(timeBetweenMeasurements * 1E3, bins='auto')
    plt.xlabel('Time (ms)')
    plt.ylabel('#')
    plt.title('Time Between Each Successive Measurement Histogram')
    figName = "Time_Hist_" + str(fig_num) + ".png"
    plt.savefig(defaultSaveFigPath + '/' + figName)
    


def plotData(read_file_in, flag):
    # Function Description: Plots data from input file, saving figures as .png
    # Input: Read-only file object, Flag that determines function execution eg. user (u), stability (st)
    #Output: None
    saveFigNum = input(
        "What should the plot number be (Avoids overwriting previous plots that have been saved to the same folder)? \n")
    if flag.find('1') != -1:
        dataObject = qmd.decodeLinearityMedianFile(read_file_in)
        plotLinearityAnalysis(dataObject, saveFigNum)
    elif flag.find('2') != -1:
        dataObject = qmd.decodeGenericFile(read_file_in, flag)
        plotStabilityAnalysis(dataObject, saveFigNum)
    else:
        plotNum = input("\nWhat data do you want to plot? \n1: Generic Magnetometer Plot\n2: Single Mag Plot\n3: Generic IMU Plot\n4: Generic Temperature Plot\n5: Generic Plot for all Data\n6: Stability Analysis Plot\n7: Power Spectral Density Plot\n8: Time Plot\nEnter Plot Number Here: ")
        dataFormat_switcher = {
            '1': plotAllMagData,
            '2': plotSingleMagData,
            '3': plotImuData,
            '4': plotTempData,
            '5': plotAllData,
            '6': plotStabilityAnalysis,
            '7': plotMagPowerSpectralDensity,
            '8': plotTimeData
        }
        plotFunction = dataFormat_switcher.get(
            plotNum, lambda ser: "Failed to plot data!")
        if int(plotNum) < 1 | int(plotNum) > 9:
            print("Invalid plotting function try again")
            plotData(read_file_in, flag)
        if int(plotNum) == 6:
            dataObject = qmd.decodeGenericFile(read_file_in, '2')
            plotFunction(dataObject, saveFigNum)
        else:
            dataObject = qmd.decodeGenericFile(read_file_in, flag)
            plotFunction(dataObject, saveFigNum)
    print("Plotting has completed....")
    return
#### End Plotting Data ####
