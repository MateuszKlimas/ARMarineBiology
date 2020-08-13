from PIL import Image
import os
import glob
import ntpath

def mirror_image(image_path, saved_location):
    """
    Flip or mirror the image
 
    @param image_path: The path to the image to edit
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_image.save(saved_location)
    #rotated_image.show()

def rotate_image(image_path, degrees_to_rotate, saved_location):
    """
    Rotate the given photo the amount of given degreesk, show it and save it
 
    @param image_path: The path to the image to edit
    @param degrees_to_rotate: The number of degrees to rotate the image
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    rotated_image = image_obj.rotate(degrees_to_rotate)
    rotated_image.save(saved_location)
    #rotated_image.show()

def calculateMirroredLabels(labels):
    """
    Used to calculate the new labels of the mirrored image
    Parameters:
        :param label:
        :type label:
        :return:
        :type return: 
    """
    newLabels = []
    for label in labels:
        label = label.strip("\n").split()
        label[1] = round(1 - float(label[1]), 6)
        newLabels.append(label)
    return newLabels

def calculateRotatedLabels(labels):
    """
    Used to calculate the new labels of the rotated image
    Parameters:
        :param label:
        :type label:
        :return:
        :type return: 
    """
    newLabels = []
    for label in labels:
        label = label.strip("\n").split()
        label[1] = round(1 - float(label[1]), 6)
        label[2] = round(1 - float(label[2]), 6)
        newLabels.append(label)
    return newLabels

def writeLabels(labels, file):
    """
    Used to write the new calculated labels into the file
    """
    with open (file,'w') as f:
        for label in labels:
            #label = label.strip('\n').split()
            f.write('{} {} {} {} {}\n'.format(label[0],label[1],label[2],label[3],label[4]))
        
def getLabels(file):
    """
    Used to retrieve labels from a text file
    """
    with open (file) as f:
        return f.readlines()

def getFilesDirectory(directory, isExtension = False, extension = ""):
    """
    Used to get files in a directory of the current main file
    """
    if (not isExtension):
        return glob.glob('{}*'.format(directory))
    else:
        return  glob.glob('{}*.{}'.format(directory, extension))
    
 
if __name__ == '__main__':

    original_images_path = os.getcwd() + "\original_data\images\\"
    original_labels_path = os.getcwd() + "\original_data\labels\\"
    created_images_path = os.getcwd() + "\created_data\images\\"
    created_labels_path = os.getcwd() + "\created_data\labels\\"

    files = getFilesDirectory(original_images_path)
    for image in files:
        name = ntpath.basename(image[:-4])
        txt = "{}{}.txt".format(original_labels_path, name)
        labels = getLabels(txt)
        print("Processing image: {}".format(ntpath.basename(image)))

        mirror_image(image, '{}{}_mirrored.jpg'.format(created_images_path,name))
        rotate_image(image, 180, '{}{}_rotated.jpg'.format(created_images_path,name))
        mirroredLabels = calculateMirroredLabels(labels)
        rotatedLabels = calculateRotatedLabels(labels)

        writeLabels(mirroredLabels, '{}{}_mirrored.txt'.format(created_labels_path, name))
        writeLabels(rotatedLabels, '{}{}_rotated.txt'.format(created_labels_path, name))

   