import numpy as np
import cv2

cap = cv2.VideoCapture('beat_tafel.mp4')
# Live-Video
#cap = cv2.VideoCapture(0)

#ergbnis_fenster = cv2.namedWindow('Video_Ergebnis')

def regionErmitteln (index, countoursRange):
    minimumRange = min(countoursRange)
    maximumRange = max(countoursRange) + 1

    indexRange = list(range(minimumRange, maximumRange))
    dataIndex = list.remove(indexRange[index])

    return (dataIndex)


while cap.isOpened():

    # Einlesen der einzelnen Frames
    ret, frame = cap.read()
    
    # Konvertieren von BGR zu HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
       
    hueRange = cv2.inRange(h, 155, 175)
    satRange = cv2.inRange(s, 50, 255)

    maskeGruen = cv2.multiply(hueRange,satRange)

    #cv2.imshow('Video_Hue', hueRange)
    #cv2.imshow('Video_sat', satRange)

    #cv2.imshow('Video_maske', maskeGruen)


    # Median zur Entferung von unerwünschten Bereichen
    ksize = 21
    median = cv2.medianBlur(maskeGruen, ksize)

    contours,hierarchy=cv2.findContours(median,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    for index in range(len(contours)):
        
        #area = cv2.contourArea(contours[index])

        #if 
        dataIndex = regionErmitteln(index, range(len(contours)))
        print(dataIndex)

        cv2.drawContours(median,contours,2,(0,0,0),cv2.FILLED)
        cv2.drawContours(median,contours,1,(0,0,0),cv2.FILLED)
        #cv2.drawContours(frame,contours,(index),(0,255,0),cv2.FILLED)
        #cv2.drawContours(frame,contours,(index),(0,255,0),cv2.FILLED)

        M = cv2.moments(median)
    
        if  M["m00"] == 0:
            cXRegoin = 1
        else:
            cXRegion = int(M["m10"] / M["m00"])

        if  M["m00"] == 0:
            cYRegion = 1
        else:
            cYRegion = int(M["m01"] / M["m00"])
            cv2.circle(median, (cXRegion, cYRegion), 5, (255, 0, 255), -1)
        print("Y-Wert: " + str(cYRegion))
        print("X-Wert: " + str(cXRegion))


    #cv2.imshow('Video_median', median)




    
    


    # Schwerpunkt ermitteln
    M = cv2.moments(median)
    
    if  M["m00"] == 0:
        cX = 1
    else:
        cX = int(M["m10"] / M["m00"])

    if  M["m00"] == 0:
        cY = 1
    else:
        cY = int(M["m01"] / M["m00"])


    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)

    # Textausgabe
    cv2.putText(frame, "Y-Wert: " + str(cY), (cX - 0, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, "X-Wert: " + str(cX), (cX - 0, cY - 9),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    #print("Y-Wert: " + str(cY))
    #print("X-Wert: " + str(cX))






    # Rechteck zu den Feldes
    x, y, w, h = cv2.boundingRect(median)
    cv2.rectangle (median, (x, y), (x + w, y + h), (52,26,77), 2)





    median_color = cv2.cvtColor(median, cv2.COLOR_GRAY2BGR)
    maske = cv2.multiply(median_color,frame)
    cv2.imshow('Video_multi', maske)




    # Bildausgabe
    cv2.imshow('Video_Ergebnis', frame)

    if cv2.waitKey(25) != -1:
        break

cap.release()
cv2.destroyAllWindows()