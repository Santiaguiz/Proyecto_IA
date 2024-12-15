from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib import style
style.use("ggplot")

def createExamples():
    # Esta función genera ejemplos a partir de imágenes numeradas (1.jpg, 2.jpg, 3.jpg)
    # y convierte estas imágenes en matrices que serán usadas para la clasificación.
    numberArrayExamples = []
    numbersWeHave = range(1, 4)  # Limitar a los números 1, 2 y 3

    for eachNum in numbersWeHave:
        try:
            # Ruta personalizada para cada número (suponiendo imágenes como 1.jpg, 2.jpg, ..., 3.jpg)
            imgFilePath = f'C:/Users/blanc/OneDrive/Documentos/IA/P2/Proyecto/{eachNum}.jpg'.replace('\\', '/')
            ei = Image.open(imgFilePath).convert("RGBA")  # Asegurarse de que la imagen tenga 4 canales
            eiar = np.array(ei)
            eiarl = str(eiar.tolist())

            lineToWrite = str(eachNum) + '::' + eiarl
            numberArrayExamples.append(lineToWrite)  # Agregar al array en lugar de escribir en un archivo
        except Exception as e:
            print(f"Error al cargar la imagen para el número {eachNum}: {e}")

    return numberArrayExamples

def threshold(imageArray):
    # Esta función aplica un umbral a la imagen, convirtiéndola en blanco y negro
    # según el promedio de los valores RGB.
    balanceAr = []
    newAr = imageArray.copy()
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
    # Esta función clasifica la imagen de entrada comparándola con ejemplos predefinidos.
    matchedAr = []

    # Usar ejemplos generados en lugar de leer de un archivo
    loadExamps = createExamples()

    try:
        i = Image.open(filePath).convert("RGBA")  # Convertir a RGBA para consistencia
        iar = np.array(i)
        iarl = iar.tolist()
        inQuestion = str(iarl)

        for eachExample in loadExamps:
            try:
                splitEx = eachExample.split('::')
                currentNum = splitEx[0]
                currentAr = splitEx[1]
                if currentAr == inQuestion:  # Comparación directa de las matrices
                    matchedAr.append(int(currentNum))
            except Exception as e:
                print(f"Error en la comparación de ejemplos: {e}")

        # Contar las coincidencias y graficar
        x = Counter(matchedAr)
        print(f"Coincidencias: {x}")

        graphX = []
        graphY = []

        ylimi = 0
        for eachThing in x:
            graphX.append(eachThing)
            graphY.append(x[eachThing])
            ylimi = max(ylimi, x[eachThing])

        fig = plt.figure()
        ax1 = plt.subplot2grid((4, 4), (0, 0), rowspan=1, colspan=4)
        ax2 = plt.subplot2grid((4, 4), (1, 0), rowspan=3, colspan=4)

        ax1.imshow(iar)
        ax2.bar(graphX, graphY, align='center')
        plt.ylim(0, ylimi + 10)  # Ajuste dinámico de límite en el gráfico

        xloc = plt.MaxNLocator(12)
        ax2.xaxis.set_major_locator(xloc)

        plt.show()

    except Exception as e:
        print(f"Error al procesar la imagen de entrada: {e}")

# Llamar a la función con la ruta de la imagen de prueba
whatNumIsThis(r'C:/Users/blanc/OneDrive/Documentos/IA/P2/Proyecto/prueba.jpg'.replace('\\', '/'))