""" 
Code is inspired from a youtube video made by the channel 
"Murtaza's Workshop- Robotics and AI"
Video title: "Hand Tracking 30 FPS using CPI | OpenCV Python (2021) | Computer Vision
Video link: https://www.youtube.com/watch?v=NZde8Xt78Iw&t=902s
"""

import cv2
import mediapipe as mp # contains gesture recognition ml model
import pygame

class HandDetector:


    def __init__(self, a_max_num_hands=1, a_min_detection_confidence=0.85) -> None:
        """Constuctor

        Args:
            a_max_num_hands (int, optional): Number of hands the detector will detect at once. Defaults to 1.
            a_min_detection_confidence (float, optional): min confidence that must be achieved for algorithm to claim it sees a hand. Defaults to 0.5.
        """
        # load the video from the webcam
        self.capture = cv2.VideoCapture(0)

        #### setting parameters for the webcam capture
        self.capture.set(3, 640) # the width of the window
        self.capture.set(4, 480) # height of the window

        # getting hand identification models
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands = a_max_num_hands, min_detection_confidence = a_min_detection_confidence)

        # get built in drawing tools for drawing hand detection
        self.mpDraw = mp.solutions.drawing_utils

        # clock object to help track framerate
        self.clock = pygame.time.Clock()

        # boolean storing if the window should close or not
        self.shouldClose = False

        # dictionary to store hand landmarks
        self.landmarkDictionary = {}


    def update(self) -> None:
        """Opens and updates a window that displays webcam feed. It also stores the positions of
        landmark points on an identified hand in a dictionary.
        """
        # loop through every frame of the video and show it (stops when you reach the end of the video)
        if self.capture.isOpened():
            # read the next frame of the video. "isLoaded" is a boolean representing whether the frame was loaded or not
            isLoaded, img = self.capture.read()

            if isLoaded == True:
                # the hand predictive model was trained on RGB images
                # so we need to convert our image to RGB
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # results of hand model on our image
                self.results = self.hands.process(imgRGB)

                # record and display the framerate of the video
                timePassed = self.clock.tick()
                fps = 1/(timePassed/1000)


                # draw the framerate as text
                cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,0))

                # clear the dictionary of all the hand's landmarks
                self.landmarkDictionary = {}

                # if there are any hands detected on the image (via their landmarks)
                if self.results.multi_hand_landmarks:
                    
                    # for every set of landmarks (1 set per hand) in the image
                    for setId, landmarkSet in enumerate(self.results.multi_hand_landmarks):
                        # make dictionary to store all landmarks for a single hand
                        handDictionary = {}
                        # for every landmark in the current set of landmarks
                        for landmarkId, landmark in enumerate(landmarkSet.landmark):
                            # get the width height and channels of the image
                            height, width, channels = img.shape
                            # convert the position of the landmarks from a fraction to a location on the img
                            xPos, yPos, zPos = int(landmark.x*width), int(landmark.y*height), int(landmark.z*height)
                            # Save list of lists storing x and y pos
                            handDictionary[landmarkId] = [xPos, yPos, zPos]
                        # update the dictionary storing all the hand's landmarks
                        self.landmarkDictionary[setId] = handDictionary


                        # draw landmarks on the hand
                        self.mpDraw.draw_landmarks(img, landmarkSet, self.mpHands.HAND_CONNECTIONS)

                # show the current frame in a window titled "Webcam feed"
                cv2.imshow("Webcam feed", img)
                # if you press the q key or click on the exit button, then close the video window (& is bitwise "and")
                # This also makes it wait 1ms between each frame
                # Note: "getWindowProperty"
                if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Webcam feed", 0) < 0:
                    self.shouldClose = True