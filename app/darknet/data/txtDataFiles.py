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
    cwd = os.getcwd()
    print(cwd)
    trainPath = sys.argv[1]
    testPath = sys.argv[2]
    if (os.path.exists(trainPath) & os.path.exists(testPath)):
        trainImages = getFilesDirectory(trainPath)
        testImages = getFilesDirectory(testPath)
        
        with open("train_images.txt",'a') as f1:
            for trainImage in trainImages:
                print('{}/{}\n'.format(cwd,trainImage))
                f1.write('{}/{}\n'.format(cwd,trainImage))

        with open("test_images.txt",'w') as f2:
            for testImage in testImages:
                f2.write('{}/{}\n'.format(cwd,testImage))

    else:
        print("ERROR: Wrong paths.")