import numpy as np
import cv2
import time
import rtmidi
import mido

# Hilfsvariable
frameAuslesen = True
colorListeIndex = 0
taktCode = []
feldNummerListe = []
ausgabeListe = ["","","","","","","","","","","","","","","",""]

# MIDI-Output suchen
print("Midi output ports: ", mido.get_output_names())
midiOutput = mido.open_output("LoopBe Internal MIDI 2")


# Liste mit allen Farben (Farbton, Sättigung, Hellwert)
colorListe = [165,52,12, 0,75,39, 70,78,27, 104,74,23, 23,78,39]

# Einbindung des Videosignals
cap = cv2.VideoCapture('beat_tafel.mp4')

# Live-Video
#cap = cv2.VideoCapture(0)

# Senden der Infomationen über MIDI
def sendControlChange(x):
    x = int(x)
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


# Einsotiernen der Farbfelder in die richtige Position
def trackCode (Liste):
    for i in Liste:
        for feldCode in i:
            taktCode = []    
            feldData = feldCode.split(".")

            if feldData[0] == "0":
                #[1,0,0,0]
                taktCode = 8
        
            elif feldData[0] == "23":
                #[0,1,0,0]
                taktCode = 4
            
            elif feldData[0] == "70":
                #[0,0,1,0]
                taktCode = 2
            
            elif feldData[0] == "104":
                #[0,0,0,1]
                taktCode = 1
            else: 
                None

            '''
            #elif feldData[0] == "165":
            #    taktCode = [1,0,1,0]

            #elif feldData[0] == "230":
            #    taktCode = [1,1,1,1]
            '''

            colorDataY = int(feldData[1])
            colorDataX = int(feldData[2])
        
            # Track 1

            if colorDataY < 350:
                if colorDataX < 600:
                    ausgabeListe[0] = taktCode
            
                elif colorDataX < 900:
                    ausgabeListe[1] = taktCode
            
                elif colorDataX < 1200:
                    ausgabeListe[2] = taktCode
                
                elif colorDataX < 1500:
                    ausgabeListe[3] = taktCode
            
                '''
                elif colorDataX < 1250:
                    ausgabeListe[4] = colorCode
                
                elif colorDataX < 1500:
                    ausgabeListe[5] = colorCode
                
                elif colorDataX < 1750:
                    ausgabeListe[6] = colorCode
            
                elif colorDataX < 2000:
                    ausgabeListe[7] = colorCode
                '''        

                # Track 2
            elif colorDataY < 500:
                if colorDataX < 600:
                    ausgabeListe[4] = taktCode
            
                elif colorDataX < 900:
                    ausgabeListe[5] = taktCode

                elif colorDataX < 1200:
                    ausgabeListe[6] = taktCode
                
                elif colorDataX < 1500:
                    ausgabeListe[7] = taktCode

                '''
                elif colorDataX < 1250:
                    ausgabeListe[4] = colorCode

                elif colorDataX < 1500:
                    ausgabeListe[5] = colorCode

                elif colorDataX < 1750:
                    ausgabeListe[6] = colorCode
            
                elif colorDataX < 2000:
                    ausgabeListe[7] = colorCode
                '''        

                # Track 3
            elif colorDataY < 650:
                if colorDataX < 600:
                    ausgabeListe[8] = taktCode

                elif colorDataX < 900:
                    ausgabeListe[9] = taktCode
            
                elif colorDataX < 1200:
                    ausgabeListe[10] = taktCode
                
                elif colorDataX < 1500:
                    ausgabeListe[11] = taktCode
            
                '''
                elif colorDataX < 1250:
                    ausgabeListe[4] = colorCode

                elif colorDataX < 1500:
                    ausgabeListe[5] = colorCode
                
                elif colorDataX < 1750:
                    ausgabeListe[6] = colorCode
            
                elif colorDataX < 2000:
                    ausgabeListe[7] = colorCode
                '''    
        
                # Track 4
            elif colorDataY < 800:
                if colorDataX < 600:
                    ausgabeListe[12] = taktCode

                elif colorDataX < 900:
                    ausgabeListe[13] = taktCode
            
                elif colorDataX < 1200:
                    ausgabeListe[14] = taktCode
                
                elif colorDataX < 1500:
                    ausgabeListe[15] = taktCode
            
                '''
                elif colorDataX < 1250:
                    ausgabeListe[4] = colorCode

                elif colorDataX < 1500:
                    ausgabeListe[5] = colorCode

                elif colorDataX < 1750:
                    ausgabeListe[6] = colorCode
            
                elif colorDataX < 2000:
                    ausgabeListe[7] = colorCode
                '''    

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
    for i in ausgabeListe:
        print(i)
        sendControlChange(i)         
            

    print(ausgabeListe)



# Hauptskript
while cap.isOpened() and frameAuslesen == True:

    # Einlesen der einzelnen Frames
    ret, frame = cap.read()
    
    # Konvertieren von BGR zu HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    # Länge der Liste 
    colorElemente = len(colorListe)

    # Nach jeder einzelenen Farbe suchen
    while colorListeIndex < colorElemente:
        
        # Liste in 3er Schritten abrufen
        colorNumb = colorListe[colorListeIndex]

        # Nach Farbe suchen
        hueRange = cv2.inRange(h, colorListe[colorListeIndex] - 10, colorListe[colorListeIndex] + 10)
        satRange = cv2.inRange(s, 50, 255)

        # Masken multiplizieren
        maskeFarbe = cv2.multiply(hueRange,satRange)

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

        if cv2.waitKey(25) != -1:
            break
        time.sleep(1)


    if frameAuslesen == True:
        
        print(feldNummerListe) 
    
    trackCode(feldNummerListe)
  
    # Auslesen des Frames nicht erneut durchführen
    frameAuslesen = False
  

cap.release()
cv2.destroyAllWindows()