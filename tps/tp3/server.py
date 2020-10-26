#!/usr/bin/python3
from socketserver import ForkingTCPServer
import socketserver
import os
from os import remove
import argparse
from filtro import *

import time


parser = argparse.ArgumentParser(description='Tp3 - Servidor', usage='./server.py -r [ruta de documentos] -p [puerto] -s [bloque de lectura]')
parser.add_argument('-r', '--root', type=str, help='Ruta', default='/root')
parser.add_argument('-p', '--port', type=int, nargs=1, help='Puerto', default=8084)
parser.add_argument('-s', '--size', type=int, help='Bloque de lectura', default=40000)
parser.add_argument('-c', '--child', type=int, help='Cantidad de hijos', default=6)
args = parser.parse_args()

class Handler(socketserver.BaseRequestHandler):
    def handle(self):

        dic={"txt":" text/plain","jpg":" image/jpeg","ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}
        
        self.data = self.request.recv(1024)
        encabezado = self.data.decode().splitlines()[0]
        archivo = "." + encabezado.split()[1]
        

        if archivo.find('./favicon.ico') != -1:
            self.request.sendall(open('/home/lucas/compu2/lab/tps/tp3/favicon.ico', 'rb').read())
           
        else:
            
            try:
                if archivo == './':
                    archivo = '/home/lucas/compu2/lab/tps/tp3/index.html'
                    extension = 'html'
                    
                else:
                    
                    extension = archivo.split('.')[2]

                    if archivo.find('ppm') != -1:
                        extension = "ppm"
                        color = archivo.split("?")[1].split("=")[0]
                        intensidad = archivo.split("?")[1].split("=")[1]
                        archivo = archivo.split("?")[0]
                        archivo = '/home/lucas/compu2/lab/tps/tp3/' + archivo.split("/")[1]
                        print("este", archivo)
                        print(intensidad)
                        imagen = Filtro(archivo, color, int(intensidad), args.size, args.child)
                        img = imagen.main()
                        image = open("/home/lucas/compu2/lab/tps/tp3/temp.ppm", "wb")
                        image.write(img)
                        image.close

                        archivo = '/home/lucas/compu2/lab/tps/tp3/temp.ppm'
                    else:
                        archivo = '/home/lucas/compu2/lab/tps/tp3/' + archivo.split("/")[1]
                        

                fd = os.open(archivo, os.O_RDONLY)
                body = os.read(fd, os.path.getsize(archivo))
                

                if archivo.find("ppm") != -1:
                    remove('/home/lucas/compu2/lab/tps/tp3/temp.ppm')

                header = bytearray("HTTP/1.1 200 OK\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
                self.request.sendall(header)
                self.request.sendall(body)
                
                #if archivo.find("ppm") != -1:  
                 #   archivo = '/home/lucas/compu2/lab/tps/tp3/aviso.html'
                  #  extension = 'html'
                
                #    fd = os.open(archivo, os.O_RDONLY)
                 #   body = os.read(fd, os.path.getsize(archivo))
                  #  os.close(fd)
                   # header = bytearray("HTTP/1.1 404 Not Found\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
                    #self.request.sendall(header)
                    #self.request.sendall(body)
        
            except Exception as x:
                print(x)
                

                
                archivo = '/home/lucas/compu2/lab/tps/tp3/404error.html'
                extension = 'html'
                    
                fd = os.open(archivo, os.O_RDONLY)
                body = os.read(fd, os.path.getsize(archivo))
                os.close(fd)
                header = bytearray("HTTP/1.1 404 Not Found\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
                self.request.sendall(header)
                self.request.sendall(body)
                

socketserver.ForkingTCPServer.allow_reuse_address = True
server =  socketserver.TCPServer(("0.0.0.0", args.port), Handler)
server.serve_forever()


with ForkingTCPServer(('0.0.0.0', args.port), Handler) as server:
    server.allow_reuse_address = True
    server.serve_forever()