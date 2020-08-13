import os
import sys
import glob

def getFilesDirectory(directory, isExtension = False, extension = ""):
    """
    Used to get files in a directory of the current main file
    """
    if (not isExtension):
        return glob.glob('{}*'.format(directory))
    else:
        return  glob.glob('{}*.{}'.format(directory, extension))
    

if __name__ == '__main__':

    trainPath = sys.argv[1]
    testPath = sys.argv[2]
    if (os.path.exists(trainPath) & os.path.exists(testPath)):
        trainImages = getFilesDirectory(trainPath)
        testImages = getFilesDirectory(testPath)
        
        with open("train_labels.txt",'a') as f1:
            for trainImage in trainImages:
                f1.write('{}\n'.format(trainImage))

        with open("test_labels.txt",'w') as f2:
            for testImage in testImages:
                f2.write('{}\n'.format(testImage))

    else:
        print("ERROR: Wrong paths.")