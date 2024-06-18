import subprocess
import pandas as pd
import time
import os
import re
import sys

class Execute():
	def __init__(self, file, timeout=5):
		self.file = file
		self.timeout = timeout

	def run(self, entrada):
		try:
			p = subprocess.Popen([
				'python3', f"{self.file}"],
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True
			)

			self.stdout, self.stderror = p.communicate(
				f"{entrada}",
				timeout=self.timeout
			)
		except subprocess.TimeoutExpired:
			p.terminate()
			self.stdout, self.stderror = "", f"Tiempo de ejecución excedido ({t}s)"

def progressBar(count_value, total, prefix='', suffix='', bar_length = 100, mark = '%'):
	bar_len = bar_length
	filled_up_Length = int(round(bar_len* count_value / float(total)))
	percentage = round(100.0 * count_value/float(total),1)
	bar = mark * filled_up_Length + '-' * (bar_len - filled_up_Length)
	#sys.stdout.write('%s [%s] %s%s ...%s\r' %(prefix, bar, percentage, '%', suffix))
	sys.stdout.write(f'{prefix} [{bar}] {percentage}% ...{suffix}\r')
	sys.stdout.flush()

pattern_files = r'(?P<rut>\d*-([0-9]|k))_ej.*(?P<ejercicio>\d+)\.py'
pattern_input = r'entrada_ej.*(?P<ejercicio>\d+)\.in'
pattern_read = r'^###(?P<type>ENTRADA)###\n(?P<content>((.|\n)*?))\n?######'
path = "./RESPUESTAS"
dirlist = os.listdir(path)


def cargar_ejercicios(path=""):
	ENTRADA = dict()
	for file in os.listdir(path):
		match = re.search( pattern_input, f"{path}/{file}" )
		if match:
			ejercicio = match.group('ejercicio')
			file = open(f"{path}/{file}", "r")
			res = file.read()

			aux = re.findall(pattern_read, res, re.M)
			for i in aux:
				if ejercicio in ENTRADA:
					ENTRADA[ejercicio].append( i[1] )
				else:
					ENTRADA[ejercicio] = [i[1]]
	return ENTRADA

ENTRADA = cargar_ejercicios("./ENTRADA")
dict = {
	'estudiante' : [],
	'ejercicio' : [],
	'entrada' : [],
	'esperado' : [],
	'obtenido' : [],
	'error' : [],
	'resultado' : [],
}
df = pd.DataFrame(dict)
import getopt
t = 5



argumentList = sys.argv[1:] # Remover primer argumento
options = "vht:" # Opciones abreviadas
long_options = ["verbatim", "help", "timeout="] # Opciones largas
VERBATIM = False
TIMEOUT = 5
try:
	# Parsing argument
	arguments, values = getopt.getopt(argumentList, options, long_options)
	 
	# checking each argument
	for currentArgument, currentValue in arguments:
		if currentArgument in ("-v", "--verbatim"):
			VERBATIM = True
		elif currentArgument in ("-t", "--timeout"):
			print( ("Enabling special output mode (% s)") % (currentValue) )
			TIMEOUT = currentValue
		elif currentArgument in ("-h", "--help"):
			s = """OPCIONES DE USO
			-v [--verbatim] : Mostrar avance del proceso
			-t [--timeout]  : Establacer el tiempo máximo de espera por programa
			-h [--help]     : Mostrar ayuda
			"""
			print( re.sub(r'\t', '', s) )
			exit(0)
		#elif currentArgument in ("-o", "--Output"):
		#	print( ("Enabling special output mode (% s)") % (currentValue) )
except getopt.error as err:
	# output error, and return with an error code
	print( f"{err}")



"""
if len( sys.argv ) > 1 and sys.argv[1] in ["-verbatim", "-v", "--verbatim", "--v"]:
	VERBATIM = True
else:
	VERBATIM = False
"""

for estudiante in sorted(dirlist):
	match = re.search( pattern_files, estudiante )
	if match:
		rut = match.group('rut')
		ejercicio = match.group('ejercicio')
		solucion = Execute(f"SOLUCION/solucion_ej{ejercicio}.py")
		i = 1
		entrada = ENTRADA[ejercicio]
		s = f"ESTUDIANTE {rut} ejercicio {ejercicio}"

		for input in entrada:
			if VERBATIM:
				progressBar(i, len(entrada), prefix=s, bar_length=50, mark='>')
			solucion.run(input)
			a = Execute(f"{path}/{estudiante}") # , timeout=TIMEOUT
			a.run(input)
			i += 1

			df.loc[len(df.index)] = [rut, ejercicio, input, solucion.stdout, a.stdout, a.stderror, solucion.stdout == a.stdout]
			time.sleep(0.3)
		if VERBATIM:
			print()



def nota(p, p_maximo, e=0.6, n_maxima=7.0, n_aprobacion=4.0, n_minima=1.0):
	n = 1
	if p < e*p_maximo:
		n = (n_aprobacion - n_minima)*( (p)/(e*p_maximo) ) + n_minima
	else:
		n = (n_maxima - n_aprobacion)*( (p - e*p_maximo)/(p_maximo*(1 - e)) ) + n_aprobacion
	return round(n, 2)

print( df )
for rut, df in df.groupby(by=['estudiante']):
	rut = rut[0]
	print( rut, nota(df.resultado.sum(), df.shape[0]) )
