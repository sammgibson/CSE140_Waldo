from PIL import Image
from keras.models import load_model
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
import heapq
import cv2

#------------------------#
#  simple progress bar   #
#------------------------#
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


#-----------------------------------------------#
#  parse argument                               #
#  the argument contains the name of the image  #
#  which will be analysed by the model          #
#-----------------------------------------------#
parser = argparse.ArgumentParser()
parser.add_argument("name", help="Filename of the 'Find-Waldo' image. The file has to be in the same folder as main.py")
args = parser.parse_args()
image_name=args.name


#----------------------------------------#
#  creating file path and loading model  #
#----------------------------------------#
directory = os.path.dirname(__file__)
filepath = os.path.join(directory, '../Saved_Models/trained_model.hdf5')
model = tf.keras.models.load_model(filepath)


#--------------#
#  load image  #
#--------------#
img = Image.open(image_name)


#---------------------------------------#
#  calculate number of times an image   #
#  has to be cropped to get an overlap  #
#  of 50% between adjacent pictures     #
#---------------------------------------#
width = img.size[0]
height = img.size[1]
w = int(width / 64) - 1
h = int(height / 64) - 1

print(w)
print(h)


#------------------------#
#  some other variables  #
#------------------------#
count_waldo = 0
bestList = []
result = np.zeros((1, 2))
prog=0
total=w*h


#---------------------------------------------------#
#  Convert rgb image with 3 channels to             #
#  gray scale with 1 channel by calculating         #
#  the mean of the rgb values. An additional        #
#  axis is added in order to get the desired input  #
#  shape for the model                              #
#---------------------------------------------------#
#img2 = np.mean(np.asarray(img), axis=2, keepdims=True)
#img3 = img2[np.newaxis, :, :, :] / 255
img2 = np.asarray(img)
img3 = img2[np.newaxis, :, :, :] / 255

cv_img = cv2.imread(image_name, cv2.COLOR_BGR2RGB)
val = []

'''
#print(img2)
for i in range(1):
    for j in range(1):
        cropped_img = cv_img[32*0:32*0+64, 32*0:32*0+64]
        cropped_img_clr = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        cropped_img_np = np.asarray(cropped_img_clr)
        cropped_img_naxis = cropped_img_np[np.newaxis,:,:,:]/255
        val.append(cropped_img_naxis)
        #print(cropped_img)
        plt.imshow(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
        plt.show()


print(np.asarray(val[0]))
prediction = model.predict(np.asarray(val[0]))
print(prediction[0,0])
'''
#print(img2)
for i in range(1):
    for j in range(1):
        cropped_img = cv_img[64*j:64*j+128, 64*i:64*i+128]
        cropped_img_clr = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        cropped_img_np = np.asarray(cropped_img_clr)
        cropped_img_naxis = cropped_img_np[np.newaxis,:,:,:]/255
        val.append(cropped_img_naxis)
        #print(cropped_img)
        plt.imshow(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
        plt.show()


#print(np.asarray(val[0]))
prediction = model.predict(np.asarray(val[0]))
print(prediction[0,0])

#----------------------------------------------#
#  run through image by cutting out            #
#  128 by 128 pictures and feed it to the model  #
#----------------------------------------------#
'''
for x in range(w):
    for y in range(h):
        prog += 1
        prediction = model.predict(img3[:, 32 * y:32 * y + 64, 32 * x:32 * x + 64, :])  #prediction of the model
        if prediction[0, 0] > 0.8:
            bestList.append(prediction[0,0])
            result = np.concatenate((result, np.array([32 * x, 32 * y])[np.newaxis, ...]), 0)
            count_waldo += 1

print('[')
ind = heapq.nlargest(4, range(len(bestList)), bestList.__getitem__) #select 4 of the predictions with highest value
print("{} Waldos predicted.".format(count_waldo))
result = result.astype(np.int32)
result = result[1:len(result),:]
toshow = np.concatenate((img2, img2, img2), 2) / 255.
for i in range(len(ind)):
    color = img.crop((result[ind[i], 0], result[ind[i], 1], result[ind[i], 0] + 64, result[ind[i], 1] + 64))
    toshow[result[ind[i], 1]:result[ind[i], 1] + 64, result[ind[i], 0]:result[ind[i], 0] + 64, :] = np.array(color).astype(
        np.float32) / 255.
plt.imshow(toshow)
plt.show()

'''