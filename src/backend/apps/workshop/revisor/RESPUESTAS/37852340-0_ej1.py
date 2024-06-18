import time

print("Bienvenido")
limite = int( input( "Ingrese un entero positivo para mostrar los impares: " ) )
numero = 1
while numero <= limite:
	if numero%2 != 0:
		print( 'El', numero ,'es impar' )
	numero += 1
