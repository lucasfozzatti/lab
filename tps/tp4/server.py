import asyncio 
import time
from argparse import ArgumentParser
import os


# Atiendo las conexiones al servidor:
async def handle_echo(reader, writer):

    dic={"txt":" text/plain","jpg":" image/jpeg","ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}
    data = await reader.read(200)
    message = data.decode()
    ip, puerto = writer.get_extra_info('peername')
    await asyncio.create_task(search(data, dic, writer))
    await asyncio.create_task(clients(ip, puerto))
 
async def search(data, dic, writer):
    lista = []
    for elem in data.split(b'\r\n'):

        lista.append(elem.decode('utf-8'))
        
    listGet = lista

    archvo = ''
    for p, elem in enumerate(listGet[0].split(' ')):
        if p == 1:
            archivo = elem
    
    
    if archivo.find('gallery.ico') != -1:
        writer.write(open(args.root + "gallery.ico", 'rb').read())
        
    else:
        
        try:
            if archivo == '/' or archivo == '/index':
                archivo = args.root + "index.html"
                extension = 'html'
            else:
                archivo = args.root + archivo.split("/")[1]  
                extension = archivo.split(".")[1]
                
            fd = os.open(archivo, os.O_RDONLY)
            body = os.read(fd, os.path.getsize(archivo))
            os.close(fd)
            header = bytearray("HTTP/1.1 200 OK\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')  
            writer.write(header)      
            with open(archivo, 'rb') as file:
                while True:
                    lec = file.read(args.size)
                    if not lec:

                        break

                    writer.write(lec)
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            

        except Exception as x:
            print("erorrrr", x)
            
            archivo = args.root + "404error.html"
            extension = 'html'
            fd = os.open(archivo, os.O_RDONLY)
            body = os.read(fd, os.path.getsize(archivo))
            os.close(fd)
            header = bytearray("HTTP/1.1 404 Not Found\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
            writer.write(header)
            writer.write(body)
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            
#Armo un log:
async def clients(ip, port):
    now = time.ctime()
    log = f'> client: {ip}:{port}; date:{now}\n'
    with open('clients.txt', 'a') as logs:
        logs.write(log)
 
async def main():
    server = await asyncio.start_server(
        handle_echo, args.ip, args.port)   
    
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    parser = ArgumentParser(
        description='Servidor asincronico de multimedias', usage='server.py -r [ruta de documentos] -p [puerto] -s [bloque de lectura] -i [direccion ip]')
   
    parser.add_argument('-r', '--root', type=str, help='Ruta', default='/home/lucas/comp2/lab/tps/tp4/')
    parser.add_argument('-p', '--port', type=int, nargs=1, help='Puerto', default=8080)
    parser.add_argument('-s', '--size', type=int, help='Bloque de lectura', default=1024)
    parser.add_argument('-i', '--ip', type=str, help='direccion ip', default=['localhost'], metavar='')
    args = parser.parse_args()

asyncio.run(main())    