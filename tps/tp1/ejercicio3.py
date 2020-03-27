
print('escriba una lista de numero separados: ', end='')
numeros = list(map(int, input().split()))

j=0
for i in numeros:
   print(numeros[j] * '*')
   j+=1
      
      
  