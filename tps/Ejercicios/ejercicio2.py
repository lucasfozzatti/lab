def Series(n, m): 
    
    num = str(n) 
    sumas = n 
    sum_str = str(n) 
  
    for i in range(1, m): 
         
        sum_str = sum_str + num
        sumas = sumas + int(sum_str) 
        
    return sumas 
print("ingrese un numero")
n=int(input(">>"))
print("ingrese cantidad de sumas")
m=int(input(">>"))
total = Series(n, m) 
print(total) 