import cv2
import numpy as np
import time
import PoseModule as pm
from pygame import mixer
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="project"
)

mycursor = mydb.cursor()

detector = pm.poseDetector()
count = 0
dir = 0  # 0 going up and 1 going down
pTime = 0
dalycount = 5
mxCount = 0
my_input = []
my_angle = []


class SqE(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        #self.video = cv2.VideoCapture('Video/5.mp4')

    def __del__(self):
        self.video.release()

    @property
    def get_curl(self):

        global count
        global dir
        global pTime
        global dalycount
        global mxCount

        while True:
            ret, frame = self.video.read()

            frame = cv2.resize(frame, (1280, 720))
            frame = detector.findPose(frame, False)  # detect pose
            lmList = detector.findPosition(frame, False)  # find position on human body

            if len(lmList) != 0:

                # Right Arm
                # angle1 = detector.findAngle(frame, 16, 14, 12)
                angle1 = detector.findAngle(frame, 16, 14, 12)
                # left Arm
                #angle2 = detector.findAngle(frame, 11, 13, 15)

                # Angle of right hip
                angle3 = detector.findAngle(frame, 26, 24, 12)
                # Angle of left hip
                # angle4 = detector.findAngle(frame, 25, 23, 11)

                # Angle of right knee
                angle5 = detector.findAngle(frame, 24, 26, 28)
                # Angle of left knee
                # angle6 = detector.findAngle(frame, 23, 25, 27)

                # check hip angle correct or not
                if 150 < angle1 < 190:
                    # check knee angle correct or not
                    # if 160 < angle5 < 200:

                        per = np.interp(angle3, (68, 170), (0, 100))  # get presantage angle between 210 to 310
                        bar = np.interp(angle3, (68, 170), (100, 650))  # min & max

                        # Check for the up  ad down routes
                        color = (255, 0, 255)
                        if per == 0:
                            color = (0, 255, 0)
                            if dir == 0:
                                count += 0.5
                                dir = 1

                        if per == 100:
                            color = (0, 255, 0)
                            if dir == 1:
                                count += 0.5
                                dir = 0

                        totalCount = int(count)
                        # print(totalCount)

                        if totalCount not in my_input:
                            my_input.append(totalCount)
                            # print(totalCount)
                            # do stuff
                            if (dalycount == totalCount):
                                mixer.init()
                                sound = mixer.Sound('Audio/stop.ogg')
                                sound.play()
                                mxCount = totalCount
                                # print(mxCount)
                                sql = "INSERT INTO sq (count) VALUES (%s)"
                                val = mxCount
                                params = (val,)
                                mycursor.execute(sql, params)
                                mydb.commit()

                            elif (totalCount == 0):
                                print('null')
                            elif (totalCount == 1):
                                mixer.init()
                                sound = mixer.Sound('Audio/1.ogg')
                                sound.play()
                            elif (totalCount == 2):
                                mixer.init()
                                sound = mixer.Sound('Audio/2.ogg')
                                sound.play()
                            elif (totalCount == 3):
                                mixer.init()
                                sound = mixer.Sound('Audio/3.ogg')
                                sound.play()
                            elif (totalCount == 4):
                                mixer.init()
                                sound = mixer.Sound('Audio/4.ogg')
                                sound.play()
                            elif (totalCount == 5):
                                mixer.init()
                                sound = mixer.Sound('Audio/5.ogg')
                                sound.play()
                            elif (totalCount == 6):
                                mixer.init()
                                sound = mixer.Sound('Audio/6.ogg')
                                sound.play()
                            elif (totalCount == 7):
                                mixer.init()
                                sound = mixer.Sound('Audio/7.ogg')
                                sound.play()
                            elif (totalCount == 8):
                                mixer.init()
                                sound = mixer.Sound('Audio/8.ogg')
                                sound.play()
                            elif (totalCount == 9):
                                mixer.init()
                                sound = mixer.Sound('Audio/9.ogg')
                                sound.play()
                            elif (totalCount == 10):
                                mixer.init()
                                sound = mixer.Sound('Audio/10.ogg')
                                sound.play()
                            else:
                                print('error')
                        else:
                            print('available')

                        # Draw Bar
                        cv2.rectangle(frame, (1100, 100), (1175, 650), color, 3)
                        cv2.rectangle(frame, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
                        cv2.putText(frame, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                                    color, 4)

                        # Draw  Count

                        cv2.rectangle(frame, (0, 450), (250, 720), (255, 255, 255), cv2.FILLED)
                        cv2.putText(frame, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                                    (255, 0, 0), 10)

                    # else:
                    #     print("error knee")
                    #     # playsound('Audio/angle.mp3')
                    #     # mixer.init()
                    #     # sound = mixer.Sound('Audio/angle.ogg')
                    #     # sound.play()
                else:
                    if angle3 not in my_angle:
                        my_angle.append(angle3)
                        mixer.init()
                        sound = mixer.Sound('Audio/hand.ogg')
                        sound.play()
                    else:
                        print('angle correct')

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime

            ret, jpg = cv2.imencode('.jpg', frame)
            return jpg.tobytes()
