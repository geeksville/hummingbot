#!/usr/bin/env python3

"""Hummingbot

A simple twitterbot that tweets Google AIY-Vision machine vision
photos when it thinks it sees a hummingbird.
"""
import tweeter
import datetime

from aiy.vision.inference import CameraInference
from aiy.vision.models import image_classification
from picamera import PiCamera

# For debugging purposes we track what
oldclasses = set()
count = 1
testing = False

# a date in the far past
lasttime = datetime.datetime.min
#
maxdelta = datetime.timedelta(minutes = 30)

# "obelisk",
# "apiary", "mosquito", "shovel", "altar", "ladle", "banana",
interesting = [ "humming",  "finch", "macaw", "hornbill" ]

def classes_info(classes, count):
    return ', '.join('%s (%.2f)' % pair for pair in classes)

# 0.02 was too low, 0.03 pretty good
threshold = 0.05

def removeold(pair):
    """given a list of google vision match pairs, return true if we think this frame is interesting"""
    global oldclasses, threshold
    hasbird = list(filter(lambda canidate: (canidate in pair[0]), interesting))
    if pair[0] not in oldclasses and float(pair[1]) > threshold:
        if not hasbird:
            oldclasses.add(pair[0])
        return True
    else:
        return False

def main():
    global count
    global lasttime
    global testing

    num_frames = None
    num_objects = 8 # just for debug printing

    # Forced sensor mode, 1640x1232, full FoV. use mode 4, was using frame rate of 10
    # https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
    # kevinh 3280x2464 is mode 3 (but that is too large for twitter)
    with PiCamera(sensor_mode=4, framerate=3) as camera:
        camera.awb_mode = 'sunlight'
        camera.exposure_mode = 'sports'
        # if out of memory err occurs see https://stackoverflow.com/questions/39251815/python-not-taking-picture-at-highest-resolution-from-raspberry-pi-camera
        camera.resolution = (1920, 1080)


        with CameraInference(image_classification.model(image_classification.MOBILENET)) as inference:
            for result in inference.run(num_frames):
                classes = image_classification.get_classes(result)
                newclasses = list(filter(removeold, classes))
                if newclasses:
                    print(classes_info(newclasses, num_objects))
                    name = newclasses[0][0]

                    filename = name.replace("/","_").replace(" ", ".")
                    hasbird = list(filter(lambda canidate: (canidate in name), interesting))

                    if hasbird:
                        # filename += str(count) # we keep all bird images for testing
                        count += 1

                    filename += ".jpg"
                    # print('writing', filename)
                    if hasbird:
                        camera.capture(filename)

                    if hasbird:
                        now = datetime.datetime.now()
                        deltat = now - lasttime
                        if deltat > maxdelta:
                            lasttime = now
                            if not testing:
                                tweeter.tweet(filename, 'I just saw a hummingbird! tweet tweet!')
                                print('tweet a bird')
                            else:
                                print('test a bird')
                        else:
                            print('ignore a bird')

if __name__ == '__main__':
    main()
