from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import Counter
from matplotlib import style
style.use("ggplot")

def createExamples():
    # Lista de ejemplos en lugar de un archivo
    numberArrayExamples = []
    numbersWeHave = range(1, 10)
    
    for eachNum in numbersWeHave:
        for furtherNum in numbersWeHave:
            imgFilePath = r'C:\Users\blanc\OneDrive\Documentos\IA\P2\Proyecto\im1.jpg'
            ei = Image.open(imgFilePath)
            eiar = np.array(ei)
            eiarl = str(eiar.tolist())

            lineToWrite = str(eachNum) + '::' + eiarl
            numberArrayExamples.append(lineToWrite)  # Agregar al array en lugar de escribir en un archivo
    
    return numberArrayExamples

def threshold(imageArray):
    balanceAr = []
    newAr = imageArray
    for eachPart in imageArray:
        for theParts in eachPart:
            # Promedio de los primeros 3 valores (R, G, B)
            avgNum = sum(theParts[:3]) / len(theParts[:3])
            balanceAr.append(avgNum)
    
    balance = sum(balanceAr) / len(balanceAr)
    for eachRow in newAr:
        for eachPix in eachRow:
            if sum(eachPix[:3]) / len(eachPix[:3]) > balance:
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255
                eachPix[3] = 255
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                eachPix[3] = 255
    return newAr

def whatNumIsThis(filePath):
    matchedAr = []
    
    # Usar ejemplos generados en lugar de leer de un archivo
    loadExamps = createExamples()
    
    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()
    inQuestion = str(iarl)
    
    for eachExample in loadExamps:
        try:
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]
            eachPixEx = currentAr.split('],')
            eachPixInQ = inQuestion.split('],')
            x = 0
            while x < len(eachPixEx):
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedAr.append(int(currentNum))
                x += 1
        except Exception as e:
            print(str(e))
    
    # Contar las coincidencias y graficar
    x = Counter(matchedAr)
    print(x)
    
    graphX = []
    graphY = []

    ylimi = 0
    for eachThing in x:
        graphX.append(eachThing)
        graphY.append(x[eachThing])
        ylimi = x[eachThing]
    
    fig = plt.figure()
    ax1 = plt.subplot2grid((4, 4), (0, 0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4, 4), (1, 0), rowspan=3, colspan=4)
    
    ax1.imshow(iar)
    ax2.bar(graphX, graphY, align='center')
    plt.ylim(0, ylimi + 10)  # Ajuste dinámico de límite en el gráfico
    
    xloc = plt.MaxNLocator(12)
    ax2.xaxis.set_major_locator(xloc)
    
    plt.show()

# Llamar a la función con la ruta de la imagen
whatNumIsThis(r'C:\Users\blanc\OneDrive\Documentos\IA\P2\Proyecto\im1.jpg')
