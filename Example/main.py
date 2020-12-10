import cv2
import numpy as np
import dlib
from math import hypot
import pyglet
import time

#Ses yükleme
sound=pyglet.media.load("sound.wav",streaming=False)
leftSound=pyglet.media.load("left.m4a",streaming=False)
rightSound=pyglet.media.load("right.m4a",streaming=False)

cap=cv2.VideoCapture(0)
board=np.zeros((300,800),np.uint8)
board[:]=255

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")



#Klavye ayarları
keyboard=np.zeros((600,1000,3),np.uint8)
keysSet1={0:"Q",1:"W",2:"E",3:"R",4:"T",
            5:"A",6:"S",7:"D",8:"F",9:"G",
            10:"Z",11:"X",12:"C",13:"V",14:"<"}
keysSet2={0:"Y",1:"U",2:"I",3:"O",4:"P",
            5:"H",6:"J",7:"K",8:"L",9:"_",
            10:"V",11:"B",12:"N",13:"M",14:"<"}
def letter(letterIndex,text,letterLight):
    # Harfler
    if letterIndex==0:
        x=0
        y=0
    elif letterIndex==1:
        x=100
        y=0
    elif letterIndex==2:
        x = 300
        y = 0
    elif letterIndex==3:
        x=500
        y=0
    elif letterIndex==4:
        x=700
        y=0
    elif letterIndex == 5:
        x = 0
        y = 100
    elif letterIndex==6:
        x=100
        y=100
    elif letterIndex == 7:
        x = 300
        y = 100
    elif letterIndex == 8:
        x = 500
        y = 100
    elif letterIndex == 9:
        x = 700
        y = 100
    elif letterIndex==10:
        x=0
        y=300
    elif letterIndex==11:
        x=100
        y=300
    elif letterIndex==12:
        x=100
        y=100
    elif letterIndex==13:
        x=500
        y=300
    elif letterIndex==14:
        x=700
        y=300




    #x=0
    #y=0
    width=200
    height=200
    thickness=3


    fontLetter=cv2.FONT_HERSHEY_PLAIN

    fontScale=10
    fontThickness=4
    textSize=cv2.getTextSize(text,fontLetter,fontScale,font_th)[0]
    widthText,heighttext=textSize[0],textSize[1]
    text_x=int((width-widthText)//2)+x
    text_y=int((height+heighttext)//2)+y
    if letterLight is True:
        cv2.rectangle( keyboard, (x + thickness, y + thickness), (x + width - thickness, y + height - thickness), (255, 255, 255), -1 )
        cv2.putText( keyboard, text, (text_x, text_y), fontLetter, fontScale, (51, 51, 51), fontThickness )
    else:
        cv2.rectangle(keyboard,(x+thickness,y+thickness),(x+width-thickness,y+height-thickness),(51,51,51),-1)
        cv2.putText( keyboard, text, (text_x, text_y), fontLetter, fontScale, (255, 255, 255), fontThickness )
def draw():
    row, col, _ = keyboard.shape
    thickknessLines = 4
    cv2.line(keyboard, (int(cols/2) - int(thickknessLines/2), 0),(int(col/2) - int(thickknessLines/2), row),
             (51, 51, 51), thickknessLines)
    cv2.putText(keyboard, "LEFT", (80, 300), font, 6, (255, 0, 0), 4)
    cv2.putText(keyboard, "RIGHT", (80 + int(cols/2), 300), font, 6, (255, 255, 255), 4)



def midpoint(ort1,ort2):
    return int((ort1.x+ort2.x))//2,int((ort1.y+ort2.y))//2
font=cv2.FONT_HERSHEY_PLAIN

def blink(eyePoints, faceMarks):
    leftPoint = (faceMarks.part( eyePoints[0] ).x, faceMarks.part( eyePoints[0] ).y)
    rightPoint = (faceMarks.part( eyePoints[3] ).x, faceMarks.part( eyePoints[3] ).y)
    centerTop = midpoint( faceMarks.part( eyePoints[1] ), faceMarks.part( eyePoints[2] ) )
    centerBottom = midpoint( faceMarks.part( eyePoints[5] ), faceMarks.part( eyePoints[4] ) )

    # horizantalLine= cv2.line( frame, leftPoint, rightPoint, (0, 255, 0), 2 )
    #veritacalLine = cv2.line( frame, centerTop, centerBottom, (0, 255, 0), 2 )

    horizantalLenght = hypot( (leftPoint[0] - rightPoint[0]), (leftPoint[1] - rightPoint[1]) )
    verticalLenght = hypot( (centerTop[0] - centerBottom[0]), (centerTop[1] - centerBottom[1]) )

    ratio = horizantalLenght / verticalLenght
    return ratio
def eyePoints(faceMarks):
    eyeLeft = []
    eyeRight = []
    for n in range(36, 42):
        x = faceMarks.part(n).x
        y = faceMarks.part(n).y
        eyeLeft.append([x, y])
    for n in range(42, 48):
        x = faceMarks.part(n).x
        y = faceMarks.part(n).y
        eyeRight.append([x, y])
        eyeLeft = np.array(eyeLeft, np.int32)
        eyeRight = np.array(eyeRight, np.int32)
        return eyeLeft, eyeRight
def gaze(eyePoints,faceMarks):
    leftRegion = np.array( [(faceMarks.part( eyePoints[0] ).x, faceMarks.part( eyePoints[0] ).y),
                                 (faceMarks.part( eyePoints[1]).x, faceMarks.part( eyePoints[1] ).y),
                                 (faceMarks.part( eyePoints[2]).x, faceMarks.part( eyePoints[2] ).y),
                                 (faceMarks.part( eyePoints[3] ).x, faceMarks.part( eyePoints[3] ).y),
                                 (faceMarks.part( eyePoints[4] ).x, faceMarks.part( eyePoints[4] ).y),
                                 (faceMarks.part( eyePoints[5] ).x, faceMarks.part( eyePoints[5] ).y)], np.int32 )
    # cv2.polylines(frame,[left_eye_region],True,(0,0,255),2)

    height, width, _ = frame.shape
    mask = np.zeros( (height, width), np.uint8 )
    cv2.polylines( mask, [leftRegion], True, 255, 2 )
    cv2.fillPoly( mask, [leftRegion], 255 )
    eye = cv2.bitwise_and( gray, gray, mask=mask )

    minX = np.min( leftRegion[:, 0] )
    maxX = np.max( leftRegion[:, 0] )
    minY = np.min( leftRegion[:, 1] )
    maxY = np.max( leftRegion[:, 1] )

    gray_eye = eye[minY:maxY, minX:maxX]
    _, thresholdEye = cv2.threshold( gray_eye, 70, 255, cv2.THRESH_BINARY )
    height, width = threshold_eye.shape
    leftThresold = threshold_eye[0:height, 0:int( width / 2 )]
    leftSideWhite = cv2.countNonZero( leftThresold )
    rightThresold = thresholdEye[0:height, int( width / 2 ):width]
    rightWhite = cv2.countNonZero( rightThresold )



    if leftSideWhite ==0:
        gazeRatio=1
    elif right_side_white ==0:
        gazeRatio=5
    else:
        gazeRatio = leftSideWhite / rightWhite
    return gazeRatio

frames=0
letterIndex=0
blinksFrame=0
frameBlink= 6
frameLetter = 9

text = ""
selectedKey = "left"
lastKeySelected = "left"
keyMenu = True
keyFrames = 0


while True:
    _, frame = cap.read()
    # frame = cv2.resize(frame, None, fx=0.8, fy=0.8)
    row, col, _ = frame.shape
    keyboard[:] = (26, 26, 26)
    frames += 1
    gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )

    frame[row - 50: row, 0: cols] = (255, 255, 255)
    if keyMenu is True:
        draw()

    #Klavye seçimi
    if selectedKey == "left":
        keys_set = keysSet1
    else:
        keys_set = keysSet2
    activeLetter = keys_set[letterIndex]

    faces = detector( gray )
    for face in faces:
        #x,y=face.left(),face.top()
        #x1,y1=face.right(),face.bottom()
        #cv2.rectangle(frame,(x,y),(x1,y1),(0,255,0),2)

        marks = predictor( gray, face )
         #Yanıp sönme algılama
        leftRatio=getBlink([36,37,38,39,40,41],marks)
        rightRatio=getBlink([42,43,44,45,46,47],marks)
        blink=(leftRatio+rightRatio)/2



        if keyMenu is True:
            #detectörle sol ve sağ bakışı seçmek
            gazeRatioLeft= gazeRatio( [36, 37, 38, 39, 40, 41], marks )
            gazeRatioRight = gazeRatio( [42, 43, 44, 45, 46, 47], marks )
            gazeRatio = (gazerRatioRight + gazeRatioRight) / 2

            if gazeRatio <= 0.9:
                selectedKey = "right"
                keyFrames += 1
                 #Bakışların bir tarafa 15 kareden fazla yoğunlaşması sonrası klavyeye gider
                if keyFrames == 15:
                    keyMenu = False
                    rightSound.play()
                     #Klavye seçildiğinde kare sayısını 0 olarak ayarla
                    frames = 0
                    keyFrames = 0
                if selectedKey != lastKeySelected:
                    lastKeySelected = selectedKey
                    keyFrames = 0
            else:
                selectedKey = "left"
                keyFrames += 1
                 #Bakışların bir tarafa 15 kareden fazla yoğunlaşması sonrası klavyeye gider.
                if keyFrames == 15:
                    keyMenu = False
                    leftSound.play()
                     #Klavye seçildiğinde çerçeve sayısını 0 alır.
                    frames = 0
                if selectedKey != lastKeySelected:
                    lastKeySelected = selectedKey
                    keyFrames = 0

        else:
             #Yanan tuşu seçmek için algılama
            if blink() > 5:
                # cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0), thickness=3)
                blinksFrame += 1
                frames -= 1

                 #Gözlerin kapalıyken yeşil olmasını gösterir.
                cv2.polylines( frame, [eyeLeft], True, (0, 255, 0), 2 )
                cv2.polylines( frame, [eyeRight], True, (0, 255, 0), 2 )

                 #Harfleri gösterir.
                if blinksFrame == frameBlink:
                    if activeLetter != "<" and activeLetter != "_":
                        text += activeLetter
                    if activeLetter == "_":
                        text += " "
                    sound.play()
                    keyMenu = True
                    # time.sleep(1)

            else:
                blinksFrame = 0

         #Klavyede harfleri gösterir
        if keyMenu is False:
            if frames == frameLetter:
                letterIndex += 1
                frames = 0
            if letterIndex == 15:
                letterIndex = 0
            for i in range( 15 ):
                if i == letterIndex:
                    light = True
                else:
                    light = False
                letter( i, keys_set[i], light )

             #ekran tahtamıza yazdığımız metni gösterir.
        cv2.putText( board, text, (80, 100), font, 9, 0, 3 )

         #Yanıp sönme
        percentageBlink = blinksFrame / frameBlink
        loadingX = int( cols * percentageBlink )
        cv2.rectangle( frame, (0, row - 50), (loadingX, row), (51, 51, 51), -1 )

        cv2.imshow( "Frame", frame )
        cv2.imshow( "Keyboard", keyboard )
        cv2.imshow( "Board", board )

        key = cv2.waitKey( 1 )
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()