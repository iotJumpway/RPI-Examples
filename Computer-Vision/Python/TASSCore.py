# *****************************************************************************
# Copyright (c) 2016 TechBubble Technologies and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html 
#
# Contributors:
#   Adam Milton-Barker - TechBubble Technologies Limited
#   Andrej Petelin - TechBubble Technologies Limited
# *****************************************************************************

import numpy as np

import struct
import cv2
import os
import fnmatch
import json
from datetime import datetime

class TassCore():

    def __init__(self):	

        with open('config.json') as configs:   

            self._configs = json.loads(configs.read())
            
    def captureAndDetect(self,frame):

        faceCascade = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES"])
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray,
            scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
            minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
            minSize=(30,30)
        )


        if not len(faces):
            faceCascade = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES2"])
            faces = faceCascade.detectMultiScale(gray,
                scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                minSize=(30,30)
            )

        if not len(faces):
            faceCascade = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES3"])
            faces = faceCascade.detectMultiScale(gray,
                scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                minSize=(30,30)
            )

        if not len(faces):
            faceCascade = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_PROFILES"])
            faces = faceCascade.detectMultiScale(gray,
                scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                minSize=(30,30)
            )

        print( "Found " + str(len(faces)) + " face(s)")

        if len(faces):

            return frame, faces[0]

        else:

            return frame, None   

    def resize(self,image):

            return cv2.resize(image,(self._configs["ClassifierSettings"]["width"], self._configs["ClassifierSettings"]["height"]),interpolation=cv2.INTER_LANCZOS4)

    def crop(self,image, x, y, w, h):
        crop_height = int((self._configs["ClassifierSettings"]["width"] / float(self._configs["ClassifierSettings"]["height"]))*w)
        midy = y + h/2
        y1 = max(0, midy-crop_height/2)
        y2 = min(image.shape[0]-1, midy+crop_height/2)
        return image[int(y1):int(y2), int(x):int(x)+int(w)]

    def prepareImage(self,filename):
            return self.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

    def normalize(self,X, low, high, dtype=None):
            X = np.asarray(X)
            minX, maxX = np.min(X), np.max(X)
            X = X - float(minX)
            X = X / float((maxX - minX))
            X = X * (high-low)
            X = X + low
            if dtype is None:
                    return np.asarray(X)
            return np.asarray(X, dtype=dtype)

    def processTrainingData(self):

        print("Processing Training Data")
        rootdir=os.getcwd()+"/training/"
        processeddir=os.getcwd()+"/processed/"

        count = 0

        for subdir, dirs, files in os.walk(rootdir):

                dirname = os.path.basename(os.path.normpath(subdir))

                for file in files:

                    newPayload = cv2.imread(os.getcwd()+'/training/'+dirname+"/"+file,1)
                    faceCascade = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES"])
                    faces = faceCascade.detectMultiScale(newPayload,
                        scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                        minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                        minSize=(30,30),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )

                    if not len(faces):
                        faceCascade = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES2"])
                        faces = faceCascade.detectMultiScale(newPayload,
                            scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                            minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                            minSize=(30,30),
                            flags=cv2.CASCADE_SCALE_IMAGE
                        )

                    if not len(faces):
                        faceCascade = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES3"])
                        faces = faceCascade.detectMultiScale(newPayload,
                            scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                            minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                            minSize=(30,30),
                            flags=cv2.CASCADE_SCALE_IMAGE
                        )

                    if not len(faces):
                        faceCascade = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_PROFILES"])
                        faces = faceCascade.detectMultiScale(newPayload,
                            scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                            minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                            minSize=(30,30),
                            flags=cv2.CASCADE_SCALE_IMAGE
                        )

                    print(os.getcwd()+'/training/'+dirname+"/"+file)

                    if len(faces):

                        x, y, w, h = faces[0]
                        print("Cropping image")
                        cropped = self.crop(newPayload, x, y, w, h)
                        print("Writing image " + dirname+"/"+file)

                        if not os.path.exists(processeddir+'/'+dirname):
                            os.makedirs(processeddir+'/'+dirname)

                        
                        newFile=datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.pgm'

                        cv2.imwrite(processeddir+'/'+dirname+"/"+newFile, cropped)
                        os.remove(os.getcwd()+'/training/'+dirname+"/"+file)

                    else:

                        os.remove(os.getcwd()+'/training/'+dirname+"/"+file)
                        print('REMOVED FILE')
        print("Finished Processing Training Data")
        
    def trainModel(self):

        print("Training")

        rootdir=os.getcwd()+"/processed/"

        faceArray=[]
        labelArray=[]
        count = 0

        MEAN_FILE = 'model/mean.png'
        POSITIVE_EIGENFACE_FILE = 'model/modelEigenvector.png'

        for subdir, dirs, files in os.walk(rootdir):
                dirname = os.path.basename(os.path.normpath(subdir))
                print(dirname)
                for file in files:
                        print (file)
                        faceArray.append(self.prepareImage(rootdir+'/'+dirname+'/'+file))
                        labelArray.append(int(dirname))
                        print (file)
                        count += 1

        print('Collected '+str(count)+' training images')

        print('Training model....')

        model = cv2.face.createEigenFaceRecognizer()
        model.train(np.asarray(faceArray), np.asarray(labelArray))
        model.save(self._configs["ClassifierSettings"]["Model"])
        print("Model saved to "+self._configs["ClassifierSettings"]["Model"])

        mean = model.getMean().reshape(faceArray[0].shape)
        cv2.imwrite(MEAN_FILE,self.normalize(mean, 0, 255, dtype=np.uint8))
        eigenvectors = model.getEigenVectors()
        eigenvector = eigenvectors[:,0].reshape(faceArray[0].shape)
        cv2.imwrite(POSITIVE_EIGENFACE_FILE,self.normalize(eigenvector, 0, 255, dtype=np.uint8))

        print("Finished Training")