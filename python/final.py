import numpy as np
import cv2
import serial
import time
# Capturing video through webcam
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
filetopaste="image/"
global detectL 
global detectR 
detectL =0
detectR =0
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()
def verde(frame):
    #convert the image frame in RGB to HSV color space
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #hue saturation value
    #set range for green color and define mask
    mask_1 = cv2.inRange(hsv_roi, np.array([25,189,118]), np.array([95, 255, 198])) #lower value and upper value....define spetre -> domeniul pentru verde
    #convert to LAB
    ycr_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB) #alt spectru
    # set range for green color and define mask
    mask_2 = cv2.inRange(ycr_roi, np.array((105,51,137)), np.array((185, 111, 217)))
    #overlap those 2 masks in a single one
    mask = mask_1 | mask_2   #puncte comune intre masti
    #for each color and bitwise_and operator between imageframe and mask determines to detect only that particular color
    kern_dilate = np.ones((8, 8), np.uint8)  # mici erori care pot aparea....noise, dirty stuf
    kern_erode = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kern_erode)  # Eroding
    mask = cv2.dilate(mask, kern_dilate)
    #cv2.imshow("mask", mask)
    return mask ,"Verde"

def rosu(frame):
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv_roi, np.array([160, 160, 10]), np.array([190, 255, 255]))
    ycr_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    mask_2 = cv2.inRange(ycr_roi, np.array((0., 165., 0.)), np.array((255., 255., 255.)))
    mask = mask_1 | mask_2
    kern_dilate = np.ones((8, 8), np.uint8)
    kern_erode = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kern_erode)  # Eroding
    mask = cv2.dilate(mask, kern_dilate)
   # cv2.imshow("mask",mask) #afiseaza masca
    return mask,"Rosu"

#n-am gasit pentru mask2 color range
def galben(frame):
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv_roi, np.array([20, 100, 100]), np.array([30, 255, 255]))
    ycr_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    mask_2 = cv2.inRange(ycr_roi, np.array((71.11, -12.08, 71.61)), np.array((97.79, -14.50, 79.46)))
#RGB  - lower_yellow = np.array([25, 146, 190]), upper_yellow = np.array([62, 174, 250])
    mask = mask_1 | mask_2
    kern_dilate = np.ones((8, 8), np.uint8)
    kern_erode = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kern_erode)  # Eroding
    mask = cv2.dilate(mask, kern_dilate)
   # cv2.imshow("mask",mask) #afiseaza masca
    return mask,"Galben"

def semafor(blob,culoare): #poate detecta contur
    global detectR
    global detectL
    largest_contour = 0
    cont_index = 0
    val1 = 0
    val2 = 0
    _,contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > largest_contour):
            largest_contour = area
            cont_index = idx
    #creating contour over the color
    if largest_contour>500:
        x, y, w, h = cv2.boundingRect(contours[cont_index])
        cv2.rectangle(frame, (x,y), (x + w, y + h), 255, 2)
        cv2.circle(frame, (320, 240), 1, (255, 0, 0), 2)
        val1 = x + int(w/2)
        val2 = y + int(h/2)

        if val1 < 250 :
            
            
            if val2 < 200:
                print("Stanga sus " + culoare)
                if detectL == 1:
                    ser.write(str("LEFT" + '\n').encode('utf-8'))
                    newfile = filetopaste + str(x)+str(y) +'.jpg'
                   
                    cv2.imwrite(newfile,frame)
                    print("incarcat poza la" + newfile)
                    print("Sent Left")
                    time.sleep(1)
            elif val2 > 280:
                print("Stanga jos " + culoare)
                if detectL == 1:
                    ser.write(str("LEFT" + '\n').encode('utf-8'))
                    print("Sent Left")
    
            detectL = 1
            detectR = 0
           
            
            time.sleep(0.5)
        elif val1 > 250:
            
            if val2 < 200:
                print("Dreapta sus " + culoare)
                if detectR==1:
                    ser.write(str("RIGHT" + '\n').encode('utf-8'))
                    print("Sent Right")
            elif val2 > 280:
                print("Dreapta jos " + culoare)
                if detectR==1:
                    ser.write(str("RIGHT" + '\n').encode('utf-8'))
                    print("Sent Right")
            
            detectL = 0
            
            detectR = 1
            time.sleep(0.5)
            
            
            
        #ser.write(str("GO" + '\n').encode('utf-8'))
	#ser.write(str("X="+str(val1) +" Y=" + str(val2) + '\n').encode('utf-8'))
        cv2.circle(frame, (val1, val2), radius=1, color=(0, 0, 255), thickness=1)
        cv2.putText(frame,culoare,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow("Camera",frame)
    return largest_contour

#3B+

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #frame = cv2.flip(frame,0)

        #mask, culoare = rosu(frame)
        #areaR = semafor(mask, culoare=culoare)
        mask, culoare = verde(frame)
        areaV = semafor(mask, culoare=culoare)
        #mask, culoare = galben(frame)
        #areaV = semafor(mask, culoare=culoare)
        # write the flipped frame
        #out.write(frame)
        
        cv2.imshow('Camera',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()

