from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

from send_serial import Serial_Class
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

RESOLUTION = (200, 200)
FRAMERATE = 5 

camera = PiCamera()
camera.resolution = RESOLUTION
camera.framerate = FRAMERATE
camera.rotation = 180
rawCapture = PiRGBArray(camera, size = RESOLUTION)



# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# initialize the Serial connection
Serial_Class.create_serial_connection()

counter = 0
time.sleep(.1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):


    image = frame.array
    image.setflags(write=1)
    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # apply non-maxima suppression to the bounding boxes using a 
    # fairly large overlap threshold to try to maintain overlapping 
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    center_of_mass_for_biggest_pedestrian = (-1,-1)
    biggest_area = 0

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        area = abs(xB - xA) * abs(yB - yA)
        if area > biggest_area:
            center_of_mass_for_biggest_pedestrian = ((xA + xB) / 2, (yA + yB) / 2)
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv2.rectangle(image,((xA + xB) / 2 - 4, (yA + yB) / 2 - 4), ((xA + xB) / 2 + 4, (yA + yB) / 2 + 4), (0, 255, 0), 2)

#    cv2.imshow("Image", image)
   
    if center_of_mass_for_biggest_pedestrian[0] >= 0: 
        print(center_of_mass_for_biggest_pedestrian)
        int_to_send = center_of_mass_for_biggest_pedestrian[0] / 2 # / 2 because the max window is 200 and we 
                                                                   # want to give a number between 0 and 100, inclusive.
        # Right now int_to_send is the distance from the CAMERA'S left.  
        # We need to flip this because we are faceing the opposide direction as the camera.
        int_to_send = 100 - int_to_send
        Serial_Class.write_to_serial(int_to_send)

    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    if key == ord("q"):
        break
    counter+=1



    # show some info on the number of bounding boxes
#    filename = imagePath[imagePath.rfind("/") + 1:]
#    print("[INFO] {}: {} original boxes, {} after suppression".format(filename, len(rects), len(pick)))




    

'''
# construct the arguemnt parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to images directory")
args = vars(ap.parse_args())





# loop over the image paths
for imagePath in paths.list_images(args["images"]):
    # load the image and resize it to (1) reduce detection time and (2) improve detection accuracy
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=min(200, image.shape[1]))
    orig = image.copy()


    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
    
    
    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # apply non-maxima suppression to the bounding boxes using a 
    # fairly large overlap threshold to try to maintain overlapping 
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # show some info on the number of bounding boxes
    filename = imagePath[imagePath.rfind("/") + 1:]
    print("[INFO] {}: {} original boxes, {} after suppression".format(filename, len(rects), len(pick)))


    # show the output images
    cv2.imshow("Before NMS", orig)
    cv2.imshow("After NMS", image)
    cv2.waitKey(0)    
'''

print('hello world')
