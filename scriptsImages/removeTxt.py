import os
import shutil
os.chdir('C:\\Users\\minde\\Desktop\\pruebas-fotos')

k = 0
j = 0
d = []
for i in range (1,3000):
    photoExists = os.path.isfile('mateusz/photo{}.jpg'.format(i))
    txtExists = os.path.isfile('peces1etiquetas/photo{}.txt'.format(i))

    """if(not(photoExists & txtExists)):
        #print("HERE")
        k+=1
        d.append(['photo{}.jpg'.format(i), 'photo{}.txt'.format(i)])"""
    if((not photoExists) & txtExists):
        k+=1
        d.append(['photo{}.jpg'.format(i), 'photo{}.txt'.format(i)])
        os.remove('peces1etiquetas/photo{}.txt'.format(i))
    else:
        #print("THERE")
        j+=1

    #print("photo: {} txt: {}".format(photoExists,txtExists))

print(k)
print(j)
print(d)