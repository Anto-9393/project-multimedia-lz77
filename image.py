from PIL import Image
import numpy as np 
from cv2 import cv2


def lz77Compress (image,sw,lab):
    img = cv2.imread(image)
    flat = np.array(img).flatten()
    row = img.shape[0]
    col = img.shape[1]
    ch = img.shape[2]
    tot = img.size
    slidingWindows = sw
    lookAhead = lab 

    encodedTuple = np.array([], dtype=np.uint16) 
    encodedChar = np.array([], dtype=np.uint8)
    # Lunghezza del Search Buffer
    sbSize = slidingWindows - lookAhead
    # puntatore Search Buffer
    sbPointer = 0
    while sbSize + sbPointer < tot :
        max_match = 0
        max_match_go_back = 0        
        selChar = sbPointer + sbSize
     # corrispondenza del carattere in Sb da lookAd
        encodeCharacters = flat[selChar] 
    #sequenza vuota[]
        seqY = np.array([])
        for i in range(sbPointer,sbPointer + sbSize):
            if(flat[i] == encodeCharacters):
                seqY = np.append(seqY,i)
    #controllare se non vi è una corrispondenza
        if(seqY.size == 0 ):
            encodedTuple = np.append(encodedTuple,(0,0))
            encodedChar = np.append (encodedChar,encodeCharacters)
        else:
            for j in seqY:
            #lunghezza della corrispodenza
                matchLenght= 0
                returnBack = selChar -i
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
                   returnBack = max_match_go_back

           
            encodedTuple = np.append(encodedTuple,(max_match_go_back,max_match))
            encodedChar = np.append(encodedChar,flat[selChar + max_match - 1])
            
            

        sbPointer+= 1 +max_match
        

   

    print("Prova", encodedTuple, encodedChar)
    print("ArrayBin",encodedTuple.tolist(), encodedChar.tolist())
    np.save("encodedTuple", encodedTuple) 
    np.save("encodedChar", encodedChar)
    a = encodedTuple.tolist()
    b = encodedChar.tolist()
    c= (a,b)
    print("File compresso in : Copressed.txt")
    output = open("Compressed.txt","w+")
    output.write(str(c))
    imgSize = open('imgSize.txt', "w")
    imgSize.write(str(row) + '\n')  # write row dimension
    imgSize.write(str(col) + '\n')  # write col dimension
    imgSize.write(str(ch) + '\n')  # write col dimension
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# fase di decodifica
def lz77Decompressor():
    imsize = open("imgSize.txt", "r")
    row = int(imsize.readline())
    col = int(imsize.readline())
    ch = int(imsize.readline())
    tot = row * col * ch

    # carico Tuple e caratteri
    encodedTuples = np.load("encodedTuple.npy")
    encodedChars = np.load("encodedChar.npy")
    tupleI= 0
    charJ = 0
        #array di decodifica
    decodeArray = np.array([])
    while tupleI < encodedTuples.size:
        pBack =  encodedTuples[tupleI]
        charact = encodedChars[charJ]
        #int usato per risolvere error:numoy.int32
        lunghezza = int(encodedTuples[tupleI + 1])
        charJ+=1
        tupleI+=2
        # se non vi è nessun prefisso codificato
        if(pBack == 0):
            decodeArray = np.append(decodeArray,charact)
        else:
            longT = decodeArray.size
            for j in range(lunghezza):
                distance = int(longT - pBack + j)
            if(distance<decodeArray.size):
                decodeArray = np.append(decodeArray,decodeArray[distance])
                if decodeArray.size < tot:
                    decodeArray = np.append(decodeArray, distance)

  
    for i in range(decodeArray.size, tot):
        decodeArray = np.append(decodeArray, i)
    decodeArray = np.reshape(decodeArray,(row,col,ch))
    cv2.imshow("output", decodeArray)
    cv2.imwrite("output.png", decodeArray)
    print("FinalSize",decodeArray.size)
    cv2.waitKey(0)
    cv2.destroyAllWindows()