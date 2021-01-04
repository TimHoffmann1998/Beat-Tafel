import numpy as np
import cv2
import time
#import rtmidi
#import mido

# Hilfsvariable
frameAuslesen = True
colorListeIndex = 0
#frameKalibierung = True
taktCode = []
feldNummerListe = []
ausgabeListe = ["","","","","","","","","","","","","","","",""]


# Liste mit allen Farben (Farbton, Sättigung, Hellwert)
colorListe = [165,52,12, 0,75,39, 70,78,27, 104,74,23, 23,78,39]

# Einbindung des Videosignals
cap = cv2.VideoCapture('beat_tafel.mp4')

# Live-Video
#cap = cv2.VideoCapture(0)



# Bestimmen der verschiedenen Regionen einer Farbe
def regionErmitteln (index, countoursRange):
    minimumRange = min(countoursRange)
    maximumRange = max(countoursRange) + 1

    indexRange = list(range(minimumRange, maximumRange))
    #print(str(indexRange[index]) + " index")
    del indexRange[index]

    #print(indexRange)
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
        #print("Y-Wert: " + str(cYRegion))
        #print("X-Wert: " + str(cXRegion))

        colorStr = str(colorNumb) + "." + str(cYRegion) + "." + str(cXRegion)
        #print(colorStr)
        colorStrListe.append(colorStr)

    return(colorStrListe)



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

    listeCount = 0
    for i in ausgabeListe:
        
        if i != "":
            i = i
            listeCount += 1
        else:
            #[0,0,0,0]
            ausgabeListe[listeCount] = 0
            listeCount += 1
             
            

    print(ausgabeListe)





# Hauptskript
while cap.isOpened() and frameAuslesen == True:

    # Einlesen der einzelnen Frames
    ret, frame = cap.read()
    
    # Konvertieren von BGR zu HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    colorElemente = len(colorListe)
    #print(colorElemente)

    while colorListeIndex < colorElemente:

        colorNumb = colorListe[colorListeIndex]
        #print(colorListeIndex)
        hueRange = cv2.inRange(h, colorListe[colorListeIndex] - 10, colorListe[colorListeIndex] + 10)
        satRange = cv2.inRange(s, 50, 255)

        maskeFarbe = cv2.multiply(hueRange,satRange)

        ksize = 11
        median = cv2.medianBlur(maskeFarbe, ksize)
        cv2.imshow('Video_Masken', median)
        

        contours,hierarchy=cv2.findContours(median,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        feldNummerListeFarbe = feldNummer(colorNumb, contours)
        
        #print(feldNummerListeFarbe)

        feldNummerListe.append(feldNummerListeFarbe)

        colorListeIndex += 3 

        if cv2.waitKey(25) != -1:
            break
        time.sleep(1)

    if frameAuslesen == True:
        #sendControlChange(feldNummerListe)
        print(feldNummerListe) 
    
    trackCode(feldNummerListe)


    #print("Midi output ports: ", mido.get_output_names())
    #midiOutput = mido.open_output("LoopBe Internal MIDI 2")

    #def sendControlChange(control, value):
        #message = mido.Message.from_bytes()
       # midiOutput.send(message)



    '''
    def sendControlChange(control, value):
        message = mido.Message('control_change', control=3, value=value)
        midiOutput.send(message)'''
    


    frameAuslesen = False


        
        







       
    #hueRange = cv2.inRange(h, 155, 175)
    #satRange = cv2.inRange(s, 50, 255)
    #colorNumb = 100

    #maskeFarbe = cv2.multiply(hueRange,satRange)

        
    #cv2.imshow('Video_maske', maskeGruen)


    # Median zur Entferung von unerwünschten Bereichen
    #ksize = 21
    #median = cv2.medianBlur(maskeFarbe, ksize)


    #contours,hierarchy=cv2.findContours(median,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)



    # Ausgabe des Strings
    #feldNummer(colorNumb, contours)
    

    

    




       

    #cv2.imshow('Video_median', median)
    #frameAuslesen = False
    
    # Textausgabe
    #cv2.putText(frame, "Y-Wert: " + str(cY), (cX - 0, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    #cv2.putText(frame, "X-Wert: " + str(cX), (cX - 0, cY - 9),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    #print("Y-Wert: " + str(cY))
    #print("X-Wert: " + str(cX))


    # Rechteck zu den Feldes
    #x, y, w, h = cv2.boundingRect(median)
    #cv2.rectangle (median, (x, y), (x + w, y + h), (52,26,77), 2)



    #median_color = cv2.cvtColor(median, cv2.COLOR_GRAY2BGR)
    #maske = cv2.multiply(median_color,frame)
    #cv2.imshow('Video_multi', maske)




    # Bildausgabe
    #cv2.imshow('Video_Ergebnis', frame)

   

cap.release()
cv2.destroyAllWindows()