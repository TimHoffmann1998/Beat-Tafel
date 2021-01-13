import numpy as np
import cv2
import time
import rtmidi
import mido

# Hilfsvariable
frameAuslesen = False
colorListeIndex = 0
#taktCode = []
#feldNummerListe = []
#ausgabeListe = ["","","","","","","","","","","","","","","",""]
midiMax = True
count = 0

# MIDI-Output suchen
print("Midi output ports: ", mido.get_output_names())
midiOutput = mido.open_output("LoopBe Internal MIDI 1")


# Liste mit allen Farben (Farbton, Sättigung, Hellwert)
colorListe = [107,90,90, 170,90,90, 95,90,90, 20,90,90, 62,90,90]#, 104,90,90, 130,90,90]

# Einbindung des Videosignals
#cap = cv2.VideoCapture('beat_tafel_testvideo.mp4')

# Live-Video
cap = cv2.VideoCapture(0)
#cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Senden der Infomationen über MIDI
def sendControlChange(x):
    x = int(x)
    print(x)
    message = mido.Message('control_change', control=3, value=x)
    midiOutput.send(message)


# Bestimmen der verschiedenen Regionen einer Farbe
def regionErmitteln (index, countoursRange):
    minimumRange = min(countoursRange)
    maximumRange = max(countoursRange) + 1

    indexRange = list(range(minimumRange, maximumRange))
    del indexRange[index]

    return (indexRange)


# Jedem Feld eine eindeutige Bezeichung zuordnen
def feldNummer(maskeFarbe, contours):
    colorStrListe = []
    for index in range(len(contours)):
        indexRange = regionErmitteln(index, range(len(contours)))
        cv2.drawContours(median,contours,index,(255,255,255),cv2.FILLED)
        
        for region in indexRange:
            cv2.drawContours(median,contours,region,(0,0,0),cv2.FILLED)
            
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

        colorStr = str(colorNumb) + "." + str(cYRegion) + "." + str(cXRegion)
        colorStrListe.append(colorStr)

    return(colorStrListe)

def sortierung (taktCode, xWerteDifferenz, colorDataX, track):
    if colorDataX < xWerteDifferenz + xWerte[0]:
        ausgabeListe[(track * 4) + 0] = taktCode
                    
    elif colorDataX < xWerteDifferenz*2 + xWerte[0]:
        ausgabeListe[(track * 4) + 1] = taktCode
                    
    elif colorDataX < xWerteDifferenz*3 + xWerte[0]:
        ausgabeListe[(track * 4) + 2] = taktCode
                        
    elif colorDataX < xWerteDifferenz*4 + xWerte[0]:
        ausgabeListe[(track * 4) + 3] = taktCode

# Einsotiernen der Farbfelder in die richtige Position
def trackCode (Liste):
    for i in Liste:
        for feldCode in i:
            taktCode = []    
            feldData = feldCode.split(".")

            if feldData[0] != "107":

                if feldData[0] == "170":
                    #[1,0,0,0]
                    taktCode = 8
            
                elif feldData[0] == "95":
                    #[1,0,1,0]
                    taktCode = 10
                
                elif feldData[0] == "20":
                    #[0,1,0,0]
                    taktCode = 4
                
                elif feldData[0] == "62":
                    #[0,0,0,1]
                    taktCode = 1
                '''
                elif feldData[0] == "130":
                    #[1,1,1,1]
                    taktCode = 15'''
                                    

                colorDataY = int(feldData[1])
                colorDataX = int(feldData[2])
            
                    # Track 1
                if colorDataY < yWerteDifferenz + yWerte[0]:
                    sortierung(taktCode, xWerteDifferenz, colorDataX, 0)  
              
                    # Track 2
                elif colorDataY < yWerteDifferenz*2 + yWerte[0]:
                    sortierung(taktCode, xWerteDifferenz, colorDataX, 1)
                        
                    # Track 3
                elif colorDataY < yWerteDifferenz*3 + yWerte[0]:
                    sortierung(taktCode, xWerteDifferenz, colorDataX, 2)
                
                    # Track 4
                elif colorDataY < yWerteDifferenz*4 + yWerte[0]:
                    sortierung(taktCode, xWerteDifferenz, colorDataX, 3)
            
            elif feldData[0] == "107":
                
                yWerte.append(int(feldData[1]))
                xWerte.append(int(feldData[2]))

                yWerte.sort()
                xWerte.sort()

                yWerteDifferenz = ((max(yWerte) - min(yWerte)) / 4)
                xWerteDifferenz = ((max(xWerte) - min(xWerte)) / 4)
                yWerteVerschiebung = yWerte[0]
                xWerteVerschiebung = xWerte[0]


    # leere Elemente mit 0en auffüllen
    listeCount = 0
    for i in ausgabeListe:
        
        if i != "":
            i = i
            listeCount += 1
        else:
            #[0,0,0,0]
            ausgabeListe[listeCount] = 0
            listeCount += 1

    # Jedes Elemente der sortierten Liste in 
    counter = 0
    for index in ausgabeListe:
        if counter < 16 and midiMax == True:
            #print(i)
            #print(counter)
            sendControlChange(index)
            counter += 1
        else:
            None

    print(ausgabeListe)


'''def kalibrierung(Liste):
    for feldCode in Liste:
        feldData = feldCode.split(".")'''



# Hauptskript
while cap.isOpened():
    ret, frame = cap.read()

    if frameAuslesen == True:
        print("test")
        colorListeIndex = 0
        taktCode = []
        feldNummerListe = []
        ausgabeListe = ["","","","","","","","","","","","","","","",""]
        yWerte = []
        xWerte = []

        # Einlesen der einzelnen Frames
        #ret, frame = cap.read()
        
        # Konvertieren von BGR zu HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)

        # Länge der Liste 
        colorElemente = len(colorListe)

        # Nach jeder einzelenen Farbe suchen
        while colorListeIndex < colorElemente:
            
            # Liste in 3er Schritten abrufen
            colorNumb = (colorListe[colorListeIndex])

            # Nach Farbe suchen
            hueRange = cv2.inRange(h, colorListe[colorListeIndex] - 10, colorListe[colorListeIndex] + 10)
            satRange = cv2.inRange(s, 40, 255)
            valRange = cv2.inRange(v, 25, 255)
            


            # Masken multiplizieren
            #maskeFarbe = cv2.multiply(hueRange,satRange)
            maskeFarbe = hueRange*satRange*valRange
            #cv2.imshow('Video', maskeFarbe)

            # Median bilden
            ksize = 11

            median = cv2.medianBlur(maskeFarbe, ksize)
            cv2.imshow('Video_Masken', median)
            
            # Regionen finden
            contours,hierarchy=cv2.findContours(median,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            feldNummerListeFarbe = feldNummer(colorNumb, contours)
            feldNummerListe.append(feldNummerListeFarbe)

            # nachste Farbe bearbeiten
            colorListeIndex += 3 

            #cv2.imshow('Video', frame)

            if cv2.waitKey(30) != -1:
                break
            
            #time.sleep(1)

        print(feldNummerListe) 

        trackCode(feldNummerListe)
        frameAuslesen = False

    else:
        None

    if frameAuslesen == False:
        if count < cap.get(cv2.CAP_PROP_FPS):
            count += 1
            frameAuslesen = False
        else: 
            frameAuslesen = True
            count = 0   
    #frameAuslesen = False
    #break

cap.release()
cv2.destroyAllWindows()