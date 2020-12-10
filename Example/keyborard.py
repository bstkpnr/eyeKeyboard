import cv2
import numpy as np


keyboard=np.zeros((600,1000,3),np.uint8)

keysSet1={0:"Q",1:"W",2:"E",3:"R",4:"T",
            5:"A",6:"S",7:"D",8:"F",9:"G",
            10:"Z",11:"Z",12:"C",13:"V",14:"B"}
def letter(letterIndex,text,letterLight):
   
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
        x=300
        y=300
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
    if letterLight is True:
        cv2.rectangle( keyboard, (x + thickness, y + thickness), (x + width - thickness, y + height - thickness), (255, 255, 255), -1 )
    else:
        cv2.rectangle(keyboard,(x+thickness,y+thickness),(x+width-thickness,y+height-thickness),(255,0,0),thickness)
    
    fontLetter=cv2.FONT_HERSHEY_PLAIN

    fontScale=10
    fontThickness=4
    textSize=cv2.getTextSize(text,fontLetter,fontScale,fontThickness)[0]
    widthtext,heightText=textSize[0],textSize[1]
    text_x=int((width-widthtext)//2)+x
    text_y=int((height+heightText)//2)+y


    cv2.putText(keyboard,text,(text_x,text_y),fontLetter,fontScale,(255,0,0),fontThickness)
for i in range(15):
    if i == 5:
        light=True
    else:
        light=False
    letter( i,keysSet1[i],light )








cv2.imshow("Keyboard",keyboard)
cv2.waitKey(0)
cv2.destroyAllWindows()
