#!/usr/bin/python3
import os
import header

path = "/home/lucas/tp2_p/"

ppm = os.open(path + "newdog.ppm", os.O_RDONLY)


def read(ppm):
    lines = os.read(ppm, 200).splitlines()
    comments = ""
    largo = 0
    for line in lines:
        if line == b"P6":
            largo += len(line) + 1
        elif line[0] == ord('#'):
            comments=line
            largo += len(line) + 1
            print(comments)
        elif len(line.split()) == 2:
            largo += len(line) + 1
        else:
            largo += len(line) + 1
            break    

    comment=comments.split(b" ")     
    print(comment)    
    offset=int(comment[1])
    interleave=int(comment[2])
    l_total=int(comment[3])

   
    os.lseek(ppm, largo, 0)
    
    pixels = []
    for i in range(l_total*8):
        reading = os.read(ppm, 3)

        pixels.append(reading)
        os.lseek(ppm, interleave*3-3, os.SEEK_CUR)

    c = 0
    byte = []
    for pixel in pixels:
        byte.append(pixel[c])
        c += 1
        if c == 3:
            c = 0

    code = "".join([str(i%2) for i in byte])

    def decode_binary_string(code):
        return ''.join(chr(int(code[i*8:i*8+8],2)) for i in range(len(code)//8))
    print(decode_binary_string(code))
    


if __name__ == "__main__":
    read(ppm)


    
    
          



'''
index =[]
n = 0
for pixel in range(0*3, L_file - largo, 1*3):
    index.append(pixel + n)
    n += 1
    if n == 3:
        n = 0
'''        