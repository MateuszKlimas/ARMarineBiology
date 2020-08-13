import glob
import random
import os
import ntpath
from shutil import copyfile

def getFilesDirectory(directory, isExtension = False, extension = ""):
    """
    Used to get files in a directory of the current main file
    """
    if (not isExtension):
        return glob.glob('{}*'.format(directory))
    else:
        return  glob.glob('{}*.{}'.format(directory, extension))
    

if __name__ == '__main__':
    images_path = os.getcwd() + '\created_data\images\\'
    labels_path = os.getcwd() + '\created_data\labels\\'
    splitted_data_path = os.getcwd() + '\splitted_data\\'
    images = getFilesDirectory('{}*'.format(images_path))
    numberImages = len(images)

    #15% of the total images will be taken for test
    nTestImages = int(numberImages * 0.15)
    #Now this images will be taken randomly from the dataset
    testImages = random.sample(range(numberImages), nTestImages)

    #Now we iterate over all the dataset, separating it in the training set and test set
    for i in range(numberImages):
        name = ntpath.basename(images[i])
        print(name)
        if i in testImages:
            copyfile(images[i], '{}\\test\\images\\{}'.format(splitted_data_path, name))
            copyfile('{}{}.txt'.format(labels_path, name[:-4]), '{}\\test\labels\\{}.txt'.format(splitted_data_path, name[:-4]))
        else:
            copyfile(images[i], '{}\\train\\images\\{}'.format(splitted_data_path, name))
            copyfile('{}{}.txt'.format(labels_path, name[:-4]), '{}\\train\labels\\{}.txt'.format(splitted_data_path, name[:-4]))
            
    print(len(testImages))
