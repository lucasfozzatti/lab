li = input("Ingrese los numeros separado por comas y un espacio\n")
num = ""
lista = []
for i in (li + " "):
    if i != "," and i != " ":
        num = num + i
    else:
        if num != "":
            lista.append(int(num))
        num = ""
def histograma(lis, cantidad = "-"):
    for i in lis:
        print(cantidad * i)

histograma(lista)

