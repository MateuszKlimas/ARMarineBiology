import os
import shutil
os.chdir('C:\\Users\\minde\\Desktop\\peces1')
i=1
for filename in os.listdir('C:\\Users\\minde\\Desktop\\peces1'):
    print(filename)
    newName = "photo" + str(i) + ".jpg"
    shutil.move(filename, newName)
    i+=1
    print(newName)
print(os.getcwd())