import numpy as np
import cv2


import numpy as np
import cv2

def do_nothing():
    return

cap = cv2.VideoCapture('beat_tafel.mp4')
# Live-Video
#cap = cv2.VideoCapture(0)

#Erstellen der Trackbars
cv2.namedWindow('Video_Ergebnis')
cv2.createTrackbar("Hue", 'Video_Ergebnis', 177, 180, do_nothing)
cv2.createTrackbar("Sat", 'Video_Ergebnis', 140, 255, do_nothing)

while cap.isOpened():

    # Einlesen der einzelnen Frames
    ret, frame = cap.read()

    # Konvertieren von BGR zu HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    # Position der Trackbars auslesen
    schwellwert_h = cv2.getTrackbarPos("Hue", 'Video_Ergebnis')
    schwellwert_s = cv2.getTrackbarPos("Sat", 'Video_Ergebnis')

    # Ermitteln der Grenzen
    h_lowerb = schwellwert_h - 3
    h_upperb = schwellwert_h + 3

    s_lowerb = schwellwert_s - 15
    s_upperb = schwellwert_s + 15

    # inRange / Binärbild
    hue_range = cv2.inRange(h, h_lowerb, h_upperb)
    sat_range = cv2.inRange(s, s_lowerb, s_upperb)

    # Ausgabe der Binärbilder Hue und Saturation
    cv2.imshow('Video_Hue', hue_range)
    cv2.imshow('Video_Saturation', sat_range)

    # Multilizieren beider Binärbilder
    maske = cv2.multiply(hue_range,sat_range)

    # Schwerpunkt ermitteln
    M = cv2.moments(maske)
  
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)

    # Textausgabe
    cv2.putText(frame, "Y-Wert: " + str(cY), (cX - 0, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, "X-Wert: " + str(cX), (cX - 0, cY - 9),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    print("Y-Wert: " + str(cY))
    print("X-Wert: " + str(cX))

    
    ksize = 7
    median = cv2.medianBlur(maske, ksize)

    x, y, w, h = cv2.boundingRect(median)
    frame = cv2.rectangle (frame, (x, y), (x + w, y + h), (0,255,0), 2)

    # Bildausgabe
    cv2.imshow('Video_Ergebnis', frame)

    if cv2.waitKey(25) != -1:
        break

cap.release()
cv2.destroyAllWindows()