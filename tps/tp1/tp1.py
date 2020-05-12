#!/usr/bin/python3
import os
import argparse
import array
import time
import multiprocessing
from queue import Empty

try:
    # Argumentos
    parser = argparse.ArgumentParser(description='TP nº1 - Procesar imagen en formato ppm')
    
    parser.add_argument('-r', '--red', type=float, default=0, help='intensidad para rojo')
    
    parser.add_argument('-g', '--green', type=float, default=0, help='intensidad para verde')
    
    parser.add_argument('-b', '--blue', type=float, default=0, help='intensidad para azul')
    
    parser.add_argument('-s', '--size', type=int, help='Bloque de lectura')
    
    parser.add_argument('-f', '--file', help='Archivo a procesar')

    args = parser.parse_args()
    
    while args.size % 3 != 0:
        args.size += 1

except:
    if args.size < 90:
            args.size = 90
    print("ERROR - Argumentos invalidos")
    

try:
    print("El padre", os.getpid(), "esta leyendo el archivo")
    time.sleep(2)

    #Leo la imagen
    imagen = open(args.file, "rb").read()

    #Fuera comentarios
    for num in range(imagen.count(b"\n# ")):
        coment1 = imagen.find(b"\n# ")
        coment2 = imagen.find(b"\n", coment1 + 1)
        imagen = imagen.replace(imagen[coment1:coment2], b"")

    finHeader = imagen.find(b"\n", imagen.find(b"\n", imagen.find(b"\n") + 1) + 1) + 1

    #Guardo el header y el body
    header = imagen[:finHeader].decode()
    body = imagen[finHeader:]

   

    print("La imagen fue leida correctamente")
except:
    print("ERROR - Error al leer la imagen, dirección invalida")
    


try:
    print("Llamando procesos hijos")

    def prosRojo(ROJO):
        rojo = []
        while True:
            try:
                imar = ROJO.get_nowait()
                for num in range(len(imar)):
                    if num % 3 == 0 or num == 0:
                        #incremento el color
                        r = int(imar[num] * args.red)
                        #Verifico que no supere los bytes posibles
                        if r > 255:
                            r = 255

                        rojo += [r] + [0] + [0]
            except Empty:
                break

        imagenRojo=[]        
        for i in rojo:
            imagenRojo.append(i)
        imrojo=array.array('B', imagenRojo)  
        x=open(args.file + " Rojo", "wb", os.O_CREAT) 
        x.write(bytearray(header, 'ascii'))
        imrojo.tofile(x)
        x.close()

    def prosVerde(VERDE):
        verde = []
        while True:
            try:
                ima = VERDE.get_nowait()
                for num in range(len(ima)):
                    if (num-1) % 3 == 0 or num == 1:
                        v = int(ima[num] * args.green)
                        if v > 255:
                            v = 255

                        verde += [0] + [v] + [0]
                  
            except Empty:
                break
         
        imagenVerde=[]        
        for i in verde:
            imagenVerde.append(i)
        imverde=array.array('B', imagenVerde)  
        
        x=open(args.file + " Verde", "wb", os.O_CREAT) 
        x.write(bytearray(header, 'ascii'))
        imverde.tofile(x)
        x.close()
        

    def prosAzul(AZUL):
        azul = []
        while True:
            try:
                imaa = AZUL.get_nowait()
                for num in range(len(imaa)):
                    if num % 3 == 0 or num == 0:
                        a = int(imaa[num] * args.blue)
                        
                        if a > 255:
                            a = 255

                        azul += [0] + [0] + [a]
            except Empty:#vacio
                break
        imagenAzul=[]        
        for i in azul:
            imagenAzul.append(i)
        imazul=array.array('B', imagenAzul)    
            
        
        x=open(args.file + " Azul", "wb", os.O_CREAT) 
        x.write(bytearray(header, 'ascii'))
        imazul.tofile(x)
        x.close()
        
    
    listaint=[]
    for i in body:
        listaint.append(i)
    cola = []
    
    j = 0
    k = []
    for i in range(len(listaint)):
        k.append(listaint[i])
        j += 1
        if j == args.size:
            cola.append(k)#cola del proceso
            k = []
            j = 0
    
    cr = multiprocessing.Queue()
    cv = multiprocessing.Queue()
    ca = multiprocessing.Queue()

    for i in cola:
        cr.put(i)
        cv.put(i)
        ca.put(i)

    fr = multiprocessing.Process(target=prosRojo, args=(cr,))
    fv = multiprocessing.Process(target=prosVerde, args=(cv,))
    fa = multiprocessing.Process(target=prosAzul, args=(ca,))

    fr.start()
    fv.start()
    fa.start()

   
    fr.join()
    fv.join()
    fa.join()

    print("Colores procesados correctamente")

except:
    
    print("ERROR - No se pudieron procesar los colores, intente nuevamente")
    exit
    
    

