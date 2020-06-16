#!/usr/bin/python3
import os
import argparse
import array
import time
import threading
from converter import a_bits, de_bits
from mensaje_code import mess

#0-------------argumentos----------------------0

# Argumentos
parser = argparse.ArgumentParser(description='Tp2 - procesa ppm')
parser.add_argument('-s', '--size', type=int, help='Bloque de lectura')
parser.add_argument('-f', '--file', help='Archivo a procesar')
parser.add_argument('-m', '--message', help='Mensaje Esteganográfico')
parser.add_argument('-p', '--pixels', type=int, help='offset en pixels del inicio del raster')
parser.add_argument('-i', '--interleave', type=int, help='interleave de modificacion en pixel')
parser.add_argument('-o', '--output', help='estego-mensaje')

args = parser.parse_args()

    


#0-----------------------------------0
#pixels = 2  message = "mensa" interleave = 0 output = "salida.ppm"
class est():
    def _init_(self):
        self.a = 0
        self.cont = 0
        self.mens = ""
        self.sis = 0
        self.offs = 0
        self.header = ""
        self.body = ""
        self.imageInt = []

    def again(self):
        self.cont = 0

    #0---------------mensaje--------------------0
    def mensaje(self):
       
        self.mens = mess(args.message)[0]
        self.sis = mess(args.message)[1]
        self.offs = args.pixels * 3

    #0-----------------------------------0

    #0------------primeros pasos imagen-----------------------0
    def modificar_imagen(self):
    
        print("Se esta leyendo el archivo")

        #Abro la imagen y la leo
        imagen = open(args.file, "rb").read()

        #Fuera comentarios
        for num in range(imagen.count(b"\n# ")):
            com1 = imagen.find(b"\n# ")
            com2 = imagen.find(b"\n", com1 + 1)
            imagen = imagen.replace(imagen[com1:com2], b"")

        finHeader = imagen.find(b"\n", imagen.find(b"\n", imagen.find(b"\n") + 1) + 1) + 1

        #Guardo el header y el body
        self.header = ""
        for i in imagen[:finHeader].decode():
            if i == "6":
                if len(str(self.sis)) >= 3:
                    self.header += "6\n#UMCOMPU2" + " " + str(self.offs) + " " + "2" + " " + str(self.sis)
                else:
                    self.header += "6\n#UMCOMPU2" + " " + str(self.offs) + " " + "2" + " " + str(self.sis) + " "
            else:
                self.header += i
        self.body = imagen[finHeader:]

        #Pixeles a int
        self.imageInt = [i for i in self.body]

    #0-------------modificar bits----------------------0
    def modificar_bits(self):
    
        for i in range(len(self.mens)):
            if i == 0:
                bit = a_bits(str(self.imageInt[self.offs]), self.mens[i])
                bitas = de_bits(bit)
                self.imageInt[self.offs] = int(bitas)
            else:
                if self.cont == 2:
                    bit = a_bits(str(self.imageInt[self.offs]), self.mens[i])
                    bitas = de_bits(bit)
                    self.imageInt[self.offs + self.a] = int(bitas)
                    self.again()
                else:
                    self.a += 3 * (args.interleave + 1)
                    self.cont += 1
                    bit = a_bits(str(self.imageInt[self.offs]), self.mens[i])
                    bitas = de_bits(bit)
                    self.imageInt[self.offs + self.a] = int(bitas)
            self.offs += 1
       

    #0--------------guardo la imagen---------------------0
    def create(self):
    
        imagenMensaje = array.array('B', [i for i in self.imageInt])

        with open(args.output, "wb", os.O_CREAT) as x:
                x.write(bytearray(self.header, 'ascii'))
                imagenMensaje.tofile(x)
                x.close()
        

    #0-----------------------------------0

    def main(self):
        
        ha = threading.Thread(target=self.mensaje())
        hb = threading.Thread(target=self.modificar_imagen())
        hc = threading.Thread(target=self.create())

        ha.start()
        hb.start()
        hc.start()
        

        ha.join()
        hb.join()
        hc.join()        
       
        print("Archivo leido correctamente")    



ob = est()
ob.main()