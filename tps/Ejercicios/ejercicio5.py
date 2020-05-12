def fibo(n,a=0,b=1):

   while n!=0:
      return fibo(n-1,b,a+b)

   return a

for i in range(0,10):
   print(fibo(i))



'''
 Es la serie Fibonachi seguido de una funcion recursiva.
 En la funcion fibo se pasa dentro de n el numero tope de la serie, cuando el numero es 0 solo retorna
 ese mismo valor, si no procede a la sucesion, a la cual se le asigna a cada termino la suma de los 
 dos numeros anteriores
 Dentro del for se imprimen indivudualmente la serie correspondiende de los numeros del 0 al 10.
 
'''