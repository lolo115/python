import cv2
import os
import numpy as np
# from skimage.measure import block_reduce
# from skimage.io import imread

# from keras.models import model_from_json

root_dir='D:/JetBrains_projects/PycharmProjects/work/'
os.chdir(root_dir)

lbp = cv2.CascadeClassifier('classifier/lbpcascade_frontalface.xml')


def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    # just making a copy of image passed, so that passed image is not changed
    img_copy = colored_img.copy ()

    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    img_crop = img_copy
    # let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale (gray, scaleFactor=scaleFactor, minNeighbors=5);

    # On considere une seule tête
    av=0

    if (np.asarray(faces).size == 4):
        (x, y, w, h)=np.asarray(faces[0])
        av = int ((h + w) / 2)
        cv2.rectangle(img_copy, (x, y), (x + av, y + av), (0, 255, 0), 2)
        img_crop=img_copy[y:y+av, x:x+av]
        img_crop=cv2.resize(img_crop,dsize=(32,32))
    # Detection multiple
    # for (x, y, w, h) in faces:
    #     av=int((h+w)/2)
    #     cv2.rectangle (img_copy, (x, y), (x + av, y + av), (0, 255, 0), 2)
    #     #cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # return img_copy
    return img_copy, img_crop


def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

cap=cv2.VideoCapture(0)
# Check if camera opened successfully
if (cap.isOpened () == False):
    print ("Error opening video stream or file")

# Read until video is completed
while (cap.isOpened ()):
    # Capture frame-by-frame
    ret, frame = cap.read ()
    #frame_2_analyze=cv2.resize(frame,dsize=(32,32))
    #frame_2_analyze=cv2.cvtColor (frame_2_analyze, cv2.COLOR_BGR2GRAY)

    if ret == True:
        frame , frame_crop  = detect_faces(lbp, frame)
        cv2.imshow('Frame',convertToRGB(frame))
        cv2.imshow('Sub', frame_crop)
        # Press Q on keyboard to  exit
        if cv2.waitKey (25) & 0xFF == ord ('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release ()

# Closes all the frames
cv2.destroyAllWindows()
