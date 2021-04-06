from PIL import Image
import numpy as np 
from cv2 import cv2


def lz77Compress (image,sw,lab):
    img = cv2.imread(image)
    flat = np.array(img).flatten()
    row = img.shape[0]
    col = img.shape[1]
    ch = img.shape[2]
    tot = row * col * ch
    slidingWindows = sw
    lookAhead = lab 
    print("fase 1")
    encodedTuple = []
    encodedChar = []
    # Lunghezza del Search Buffer
    sbSize = slidingWindows - lookAhead
    for it in range(sbSize):
        encodedTuple.append(0)
        encodedChar.append (flat[it])
    # puntatore Search Buffer
    sbPointer = 0
    print("fase 2")
    while sbPointer < tot :
        max_match = 0
        max_match_go_back = 0        
        selChar = sbPointer + sbSize
     # corrispondenza del carattere in Sb da lookAd
        encodeCharacters = flat[selChar] 
    #sequenza vuota[]
       
        seqY = []
        for i in range(sbPointer,sbPointer + sbSize):
            if(flat[i] == encodeCharacters):
                seqY.append(i)
        
    #controllare se non vi è una corrispondenza
        if(len(seqY) == 0 ):
            encodedTuple.append(0)
            encodedChar.append (encodeCharacters)
        else:
            for j in seqY:
            #lunghezza della corrispodenza
                matchLenght= 0
                returnBack= selChar - j
                it = 0 
                while selChar + it < tot :
                    if flat[it + j] == flat[selChar + it]:
                        matchLenght +=1
                        it +=1
                  # se non trova corrispondenze
                    else: 
                        break
                if matchLenght>max_match:
                   max_match = matchLenght
                   returnBack= max_match_go_back

           
            encodedTuple.append((max_match_go_back,max_match))
            encodedChar.append(encodedChar,flat[selChar + max_match - 1])
            
            

        sbPointer= sbPointer+ 1 +max_match
    
        

   

    print("Prova", encodedTuple, encodedChar)   
    np.save("encodedTuple", encodedTuple) 
    np.save("encodedChar", encodedChar)  
    print("File compresso in : Copressed.txt")
    output = open("Compressed.txt","w+")
    imgSize = open('imgSize.txt', "w")
    imgSize.write(str(row) + '\n')  # write row dimension
    imgSize.write(str(col) + '\n')  # write col dimension
    imgSize.write(str(ch) + '\n')  # write col dimension
    output.close()
    imgSize.close()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# fase di decodifica
# fase di decodifica
def lz77Decompressor():
    imsize = open("imgSize.txt", "r")
    row = int(imsize.readline())
    col = int(imsize.readline())
    ch = int (imsize.readline())
    tot = row * col * ch

    # carico Tuple e caratteri
    encodedTuples = np.load("encodedTuple.npy")
    encodedChars = np.load("encodedChar.npy")
    tupleI= 0
    charJ = 0
        #array di decodifica
    decodeArray = []
    while tupleI < encodedTuples.size:
        pBack =  encodedTuples[tupleI]
        charact = encodedChars[charJ]
        #int usato per risolvere error:numoy.int32
        lunghezza = int(encodedTuples[tupleI + 1])
        charJ+=1
        tupleI+=2
        # se non vi è nessun prefisso codificato
        if(pBack == 0):
            decodeArray.append(charact)
        else:
            longT = len(decodeArray)
            for j in range(lunghezza):
                distance = int(longT - pBack + j)
            if(distance<len(decodeArray)):
                decodeArray.append(distance)
                if len(decodeArray) < tot:
                    decodeArray.append( distance)

  
    for i in range(len(decodeArray), tot):
        decodeArray.append( i)
    decodeArray = np.reshape(decodeArray,(row,col,ch))
    imageArray = np.asarray(decodeArray)
    
    cv2.imwrite("output.png", imageArray)
    print("FinalSize",len(imageArray))
    cv2.waitKey(0)
    cv2.destroyAllWindows()