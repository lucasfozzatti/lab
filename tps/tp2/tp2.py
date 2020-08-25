#!/usr/bin/python3

import os
import argparse
import array
import concurrent.futures 
import threading
import header
from time import time
import string


global read_bytes
#barrier=threading.barrier(5)

def change_LSB(byte, bit):
    if byte % 2 != bit:
        if bit == 1:
            byte += 1
        else:
            byte -= 1

    return byte


def thread_work(color, total_bytes, change, mensaje):
    global read_bytes
    
    global barrier

    bits = [mensaje[i] for i in range(color, len(mensaje), 3)]
    wr = 0
    while wr < total_bytes:

        wr = len(read_bytes)

        # modifican bytes y guardan en lista
        while change != [] and change[0] < wr:

            index_to_change = change.pop(0)
            read_bytes[index_to_change] = change_LSB(read_bytes[index_to_change], int(bits.pop(0)))
            

        


def rot13(text):
    rot13trans =text.maketrans(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 
        b'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')
    return text.translate(rot13trans)
def trans(mensaje):
    mensaje=rot13(mensaje)
    print(mensaje)

    
    
    x = []
    for i in mensaje:
        bit = bin(i)[2:]
        while len(bit) < 8:
            bit = "0" + bit
        x.append(bit)

    mensaje= "".join(x)
   
    return mensaje


def main():
    inicio = time()
    global mensaje
    global read_bytes
    read_bytes = []
    try:
        # argumentos
        parser = argparse.ArgumentParser()

        parser.add_argument("-f", "--file", type=str, required=True, help="ppm file you want to open")
        parser.add_argument("-m", "--message", type=str, required=True, help="file")
        parser.add_argument("-o", "--output", type=str, required=True, help="file")
        parser.add_argument("-s", "--size", type=int, default=1024, help="size")
        parser.add_argument("-e", "--offset", type=int, required=True, help="interleave pixels")
        parser.add_argument("-i", "--interleave", type=int, required=True, help="interleave pixels")
        parser.add_argument("-c", "--cifrado", action= 'store_true', help="message in rot13") 

        args = parser.parse_args()
    except:
        print("Debe especificar todos los argumentos")
   
    path = "/home/lucas/tp2_p/"
    
    L_file = os.path.getsize(path + args.file)

    archivo= open(path + args.message, "rb")
    mensaje = archivo.read()
    L_TOTAL = len(mensaje)

    if args.cifrado:

        thread = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        hilo=thread.submit(trans, mensaje)   
        mensaje=hilo.result()
    else:
        
        x = []
        for i in mensaje:
            bit = bin(i)[2:]
            while len(bit) < 8:
                bit = "0" + bit
            x.append(bit)

        mensaje= "".join(x)
        print(mensaje)

    f = os.open(path + args.file, os.O_RDONLY)
    
    
    header_end, width, height, max_c, comments = header.readHeader(f)

   

    os.lseek(f, header_end, 0)

   
    comments = "#UMCOMPU2 " + str(args.offset) + " " + str(args.interleave) + " " + str(L_TOTAL)
    


    w = os.open(path + args.output, os.O_WRONLY | os.O_CREAT)
    N_header = header.createHeader(width, height, max_c, comments)
    L_header = len(N_header)
    os.close(w)

    
    index =[]
    n = 0
    for pixel in range(0*3, L_file - header_end, 1*3):
        index.append(pixel + n)
        n += 1
        if n == 3:
            n = 0
    
    red = []
    green = []
    blue = []
    index = index[:len(mensaje)]
    for i in range(0, len(index), 3):
        red.append(index[i])
    for i in range(1, len(index), 3):
        green.append(index[i])
    for i in range(2, len(index), 3):
        blue.append(index[i])
  
    indexes = (red, green, blue)

    thread = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    for i in range(len(indexes)):

        [thread.submit(thread_work, i, width * height * 3, indexes[i], mensaje)]

    if len(mensaje) * args.interleave + args.offset > width*height:

        raise exceptions.OverflowError("No existen suficientes bytes")
    
    out = open(path + args.output, "wb", os.O_CREAT)
    out.write(bytearray(N_header, 'ascii'))

    wr = 0
    while wr < (width * height * 3):
        read_bytes += [i for i in os.read(f, args.size)]
        wr = len(read_bytes)
    if read_bytes:
        image = array.array('B', read_bytes)
        image.tofile(out)
        
   # try:
        #barrier.wait(0.1)
    #except threading.BrokenBarrierError:
     #   pass

    out.close()
    print("header", L_header)
    print("Tiempo total:\n", str(time()-inicio)[:4], "segundos")


if __name__ == "__main__":
    main()
