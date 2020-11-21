import multiprocessing as mp
import array
import os


class Filter():

    def __init__(self, file, opt, inte, childs, size):
        if size % 3 != 0:
            self.size = size - size % 3
        else:
            self.size = size
        # Arguemntos de entrada
        self.file = file
        self.inten = inte
        self.childs = childs
        # Imagen nueva
        self.imagenF = open('temp.ppm', 'wb')
        # IPC
        self.cola = mp.Queue()
        self.chunk = array.array('B')
        # Determino que byte modificar:
        for pos, color in enumerate(['red', 'green', 'blue', 'b&w']):
            if opt == color:
                self.filtro = pos

    # filtro
    def filter(self, lock):
        print('En ejecucion: ', os.getpid())
        lock.acquire()
        newB = []
        while True:
            leido = self.cola.get()
            if leido == 'end':
                break
            lecList = [i for i in leido]
            if self.filtro != 3:
                for pos, by in enumerate(lecList):
                    if pos % 3 == self.filtro:
                        mod = int(by) * self.inten
                        if mod < 256:
                            newB.append(int(mod))
                        else:
                            newB.append(255)
                    else:
                        newB.append(0)
            else:
                # Valor para ajuste de filtro.
                lecList.append(0)
                # ---
                suma = 0
                for pos, by in enumerate(lecList):
                    if pos % 3 == 0 and pos > 0:
                        newValue = suma//3
                        mod = newValue * self.inten
                        for _ in range(3):
                            if mod < 256:
                                newB.append(int(mod))
                            else:
                                newB.append(255)
                        suma = 0
                    suma += int(by)
        lock.release()
        array.array('B', newB).tofile(self.imagenF)

    # Cabecera de imagen ppm
    def head(self):
        img = open(self.file, 'rb')
        lines = img.read(100).splitlines()
        comments = []
        header_end = 0
        for line in lines:
            if line == b"P6":
                header_end += len(line) + 1
            elif line[0] == ord("#"):
                comments.append(line)
                header_end += len(line) + 1
            elif len(line.split()) == 2:
                words = line.split()
                width = int(words[0])
                height = int(words[1])
                header_end += len(line) + 1
            else:
                max_c = int(line)
                header_end += len(line) + 1
                break
        header = f'P6\n{width} {height}\n{max_c}\n'
        return header_end, bytearray(header, 'utf-8')

    def main(self):
        sik, head = self.head()
        lock = mp.Lock()
        # Imagen nueva
        self.imagenF.write(head)
        # Defino hijos
        hijos = []
        for n in range(self.childs):
            hijos.append(mp.Process(target=self.filter, args=(lock,)))
            hijos[n].start()
        # ----
        with open(self.file, 'rb') as imagen:
            imagen.seek(sik)
            while True:
                lec = imagen.read(self.size)
                self.cola.put(lec)
                if not lec:
                    break
            for i in range(self.childs):
                self.cola.put("end")
            for i in range(self.childs):
                hijos[i].join()
        print('- Terminado - ')


if __name__ == "__main__":
    obj = Filter('dog.ppm', 'green', 0.5, 7, 250)
    obj.main()
