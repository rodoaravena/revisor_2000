import time

num = int( input( "Ingrese un número entre el 1 y el 12 entero: " ) )
while num < 1 or num > 12:
	print( "El numero ingresado no es valido. Intente nuevamente" )
	num = int( input( "Ingrese un numero entre el 1 y el 12 entero: " ) )
i = 1
while i <= 12:
	producto = i * num
	print (i," x ", num, " = ", producto )
	i += 1
	time.sleep(0.1*i)