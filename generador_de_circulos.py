import matplotlib
import matplotlib.pyplot as plt
import random
import PySimpleGUI as sg
import os

num_circulos = 0
min_radio = 0.0
max_radio = 0.0
eje_x = 0.0
eje_y = 0.0
figura = None
values = None

sg.theme('Dark Green')

layout = [
	[sg.Text("hola genki", font=("Comic Sans MS", 25))],
	[sg.Text("numero de circulos: "), sg.Push(), sg.Input(key='-NUMCIRCULOS-', default_text='10')],
	[sg.Text("radio minimo: "), sg.Push(), sg.Input(key='-MINRADIO-', default_text='5.5')],
	[sg.Text("radio maximo: "), sg.Push(), sg.Input(key='-MAXRADIO-', default_text='12.5')],
	[sg.Text("limite del area en x: "), sg.Push(), sg.Input(key='-EJEX-', default_text='40.0')],
	[sg.Text("limite del area en y: "), sg.Push(), sg.Input(key='-EJEY-', default_text='40.0')],
	[sg.Button("generar", key="-GENERAR-")],
	[sg.HorizontalSeparator(color='black')],
	[
		sg.Text("folder: "),
		sg.Push(),
		sg.Input(key='-FOLDER-', default_text=os.getcwd()),
		sg.FolderBrowse("seleccionar", initial_folder=os.getcwd())
	],
	[
		sg.Text("nombre de archivo: "),
		sg.Push(),
		sg.Input(key='-NOMBRE-', default_text='circulos'),
		sg.Button("guardar", key="-GUARDAR-")
	]
]

def llenar_valores():
	global num_circulos, min_radio, max_radio, eje_x, eje_y

	if values == None:
		sg.popup("primero llena los valores we", font=("Comic Sans MS", 18))
	else:
		num_circulos = int(values["-NUMCIRCULOS-"])
		min_radio = float(values["-MINRADIO-"])
		max_radio = float(values["-MAXRADIO-"])
		eje_x = float(values["-EJEX-"])
		eje_y = float(values["-EJEY-"])
		verificar_parametros()

def verificar_parametros():
	if num_circulos <= 0 or num_circulos > 1000:
		sg.popup("no seas idiota dame un numero de circulos valido", font=("Comic Sans MS", 18))
	elif min_radio <= 0:
		sg.popup("no seas idiota dame un radio minimo positivo", font=("Comic Sans MS", 18))
	elif max_radio <= 0 or max_radio < min_radio:
		sg.popup("no seas idiota dame un radio maximo valido", font=("Comic Sans MS", 18))
	elif eje_x <= 0 or (eje_x / 2.0) < max_radio:
		sg.popup("no seas idiota dame una longitud de eje x valida", font=("Comic Sans MS", 18))
	elif eje_y <= 0 or (eje_y / 2.0) < max_radio:
		sg.popup("no seas idiota dame una longitud de eje y valida", font=("Comic Sans MS", 18))
	else:
		generar_circulos()

def generar_circulos():
	circulos = []

	primer_circulo = plt.Circle((0, 0), max_radio, color='black', lw=5, fill=False)
	circulos.append(primer_circulo)

	for i in range(num_circulos - 1):
		nuevo_centro = [0, 0]
		nuevo_radio = 0
		distancia_nuevo_centro = 0

		contador_centros = 0

		# generar centro aleatorio dentro del circulo
		while True:
			nuevo_centro = [
				random.uniform(-max_radio, max_radio),
				random.uniform(-max_radio, max_radio)
			]
			distancia_nuevo_centro = (nuevo_centro[0] ** 2 + nuevo_centro[1] ** 2) ** 0.5
			if distancia_nuevo_centro <= max_radio:
				break

		# generar radio aleatorio que salga del circulo
		while True:
			nuevo_radio = random.uniform(min_radio, max_radio)

			if (distancia_nuevo_centro + nuevo_radio) <= max_radio:
				continue
			if nuevo_centro[0] > 0:
				if nuevo_centro[0] + nuevo_radio > (eje_x / 2.0):
					continue
			else:
				if nuevo_centro[0] - nuevo_radio < (-eje_x / 2.0):
					continue
			if nuevo_centro[1] > 0:
				if nuevo_centro[1] + nuevo_radio > (eje_y / 2.0):
					continue
			else:
				if nuevo_centro[1] - nuevo_radio < (-eje_y / 2.0):
					continue
			break

		nuevo_circulo = plt.Circle(
			(nuevo_centro[0], nuevo_centro[1]), nuevo_radio, color='black', lw=5, fill=False)
		circulos.append(nuevo_circulo)

	dibujar_circulos(circulos)

def dibujar_circulos(circulos):
	matplotlib.rcParams['figure.figsize'] = [eje_x, eje_y]

	global figura

	figura, ejes = plt.subplots()
	ejes = plt.gca()
	ejes.cla()

	ejes.set_xlim((-1.0 * (eje_x / 2.0), (eje_x / 2.0)))
	ejes.set_ylim((-1.0 * (eje_y / 2.0), (eje_y / 2.0)))

	for i in range(num_circulos):
		ejes.add_patch(circulos[i])

	plt.axis('off')

def guardar_resultado():
	if figura == None:
		sg.popup("no has generado nada aun we", font=("Comic Sans MS", 18))
	elif values["-FOLDER-"] == "":
		sg.popup("no has seleccionado un folder we", font=("Comic Sans MS", 18))
	elif values["-NOMBRE-"] == "":
		sg.popup("no le has puesto nombre al archivo we", font=("Comic Sans MS", 18))
	else:
		direccion_transparente = values["-FOLDER-"] + '/' + values["-NOMBRE-"] + '.png'
		figura.savefig(direccion_transparente, bbox_inches='tight', transparent=True)
		direccion_fondo = values["-FOLDER-"] + '/' + values["-NOMBRE-"] + '_fondo.png'
		figura.savefig(direccion_fondo, bbox_inches='tight', transparent=False)

def event_loop():
	global values

	window = sg.Window("generador de circulos", layout, font=("Comic Sans MS", 18))

	while True:
		event, values = window.read()

		if event == "-GENERAR-":
			llenar_valores()
			sg.popup("circulos generados", font=("Comic Sans MS", 18))
		if event == "-GUARDAR-":
			guardar_resultado()
		if event == sg.WIN_CLOSED:
			break

	window.close()

if __name__=="__main__":
	event_loop()
