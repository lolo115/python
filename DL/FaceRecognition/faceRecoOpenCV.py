import cv2
import os
import numpy as np
from keras.models import model_from_json

root_dir='D:/JetBrains_projects/PycharmProjects/work/'
os.chdir(root_dir)

# Definition du classifier d'image (reconnaissance faciale)
lbp = cv2.CascadeClassifier('classifier/lbpcascade_frontalface.xml')

# Chargement du modèle d'apprentissage
model = model_from_json(open('model.json').read())
model.load_weights('weights.h5')
class_names = ['Unhappy', 'Happy']

def print_indicator(data, model, class_names, bar_width=50):
    probabilities = model.predict(np.array([data]))[0]
    #print(probabilities)
    left_count = int(probabilities[1] * bar_width)
    right_count = bar_width - left_count
    left_side = '-' * left_count
    right_side = '-' * right_count
    return class_names[0]+': '+ left_side + 'XXX' + right_side +': '+class_names[1]+ ' ----> Probability '+str(class_names)+':'+str(probabilities)

def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    # On fait une copie de l'image, afin de ne pas modifier l'image source
    img_copy = colored_img.copy ()

    # On créé deux images en les convertissants en NB pour application du modèle
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    img_crop = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    # On detecte les visages avec le classifieur donné en paramètre. Cette fonction renvoie plusieurs visages si on détecte plusieurs visages.
    faces = f_cascade.detectMultiScale (gray, scaleFactor=scaleFactor, minNeighbors=5);

    # On considere une seule tête
    av=0

    if (np.asarray(faces).size == 4):
        (x, y, w, h)=np.asarray(faces[0]) # on récupère les coordonnées du bas du visage, sa largeur et sa hauteur
        av = int ((h + w) / 2) # On moyenne pour avoir un carré
        cv2.rectangle(img_copy, (x, y), (x + av, y + av), (0, 255, 0), 2)
        img_crop=cv2.resize(img_copy[y:y+av, x:x+av],dsize=(32,32)) # on rapporte à un carré de 32x32 pour analyse dans le modèle qu'on convertit (ensuite) en N&B
        img_crop = cv2.cvtColor (img_crop, cv2.COLOR_BGR2GRAY)
    else:
        img_crop=None # Si pas de visage détecté on renvoie None


    # Detection multiple
    # for (x, y, w, h) in faces:
    #     av=int((h+w)/2)
    #     cv2.rectangle (img_copy, (x, y), (x + av, y + av), (0, 255, 0), 2)
    #     #cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # return img_copy
    return img_copy, img_crop

def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)


# Lancement de la capture video
cap=cv2.VideoCapture(0)
# Check if camera opened successfully
if (cap.isOpened () == False):
    print ("Error opening video stream or file")

# Read until video is completedq
while (cap.isOpened ()):
    # Capture frame-by-frame
    ret, frame = cap.read ()
    # Traitement de la capture
    if ret == True:
        # on récupére la frame pour affichage avec le rectangle et la frame_crop en 32x32 pour alimenter le modèle de DL 
        # On donne le classifier lbp en paramètre et la frame capturée (la frame récupérée est dotée d'un eventuel rectangle pour l'identification du visage)
        frame , frame_crop  = detect_faces(lbp, frame)
        # (1) On affiche la frame à l'écran
        cv2.imshow('Frame',convertToRGB(frame))
        
        # (2) On traite la frame en 32x32 pour affichage des résultats dans la console
        if frame_crop is not None:
            data = frame_crop.astype (np.float) / 255
            data = np.expand_dims (data, axis=2)
            txt = print_indicator (data, model, class_names, bar_width=100)
            print (txt)

        # Taper Q pour quitter la frame
        if cv2.waitKey (25) & 0xFF == ord ('q'):
            break

    # 
    else:
        break

# Quand tout est validé, on relache la capture
cap.release ()

# et on detruit toutes les fenêtres.
cv2.destroyAllWindows()
