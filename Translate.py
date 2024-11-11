import json, os, time
from googletrans import Translator
from pathlib import Path
#pip install googletrans==4.0.0rc1

input_lang = "en"
output_lang =  "es"

translator = Translator()
errores = []

files_path = [archivo.as_posix() for archivo in Path('./x-Events').glob("**/*.json")]

special_words = ["null"] #Agregar

def open_file(input_file_name):
	with open(input_file_name, 'r') as f:
		return json.load(f)    

def translate_file(data):
	for a in range(len(data["EventText"])): #Lista de eventos
		print("Event", a) # dicc Evento individual
		textEvent = data["EventText"][a]["theScene"] # list Texto del evento
		for c in range(len(textEvent)):
			b = str(textEvent[c])
			if " " in b and not(".mp3" in b) and not(".png" in b) and not(".jpeg" in b) and not(".ogg" in b) and not(".jpg" in b) and not(".waw" in b) and not(b in special_words):
				
				if "|f|" in b:
					print("r1")
					partes = b.split('|f|')
					# Lista resultante
					resultado = []
					
					# Procesar cada segmento
					for parte in partes:
					    if parte:
					        resultado.append(parte.split('|n|'))
				
					for t in range(len(resultado)):
						text = resultado[t][1]
						resultado[t][1] = translator.translate(str(text), dest=output_lang).text or b
						
						union  = ["|n|".join(x) for x in resultado]
						traduccion ="|f|" +"|f|".join(union)
						print(traduccion,"\n")
						data["EventText"][a]["theScene"][c] = traduccion
				else:		
					print("r2")
					try:
						traduccion = translator.translate(str(b), dest=output_lang).text or b
						print(traduccion,"\n")
						data["EventText"][a]["theScene"][c] = traduccion
					except Exception as err:
						errores.append([open_file_path,err, f"Event: {a}", str(textEvent[c])])
						create_debug(save_file_path, errores)
						print(err)
			
def save_file(data, output_file_name):
	with open(output_file_name, 'w') as f:
  	  json.dump(data, f, ensure_ascii=False, indent=4)

def create_debug(save_file_path = "", errores = ""):
	with open('-Errores_debug.txt', 'w', encoding='utf-8') as f:
		f.write(save_file_path + str(errores))

print(files_path)


for file_path in files_path:
	open_file_path = f"./{file_path}"
	save_file_path = f"./ES/{file_path}"
	dirname_save_file = os.path.dirname(save_file_path)
	
	print("file",open_file_path)
	print("save path file,", save_file_path)
	print("save path",dirname_save_file)
	
	try:
		os.makedirs(dirname_save_file, exist_ok=True)
		if os.path.isfile(save_file_path):
			raise Exception("Archivo existente.")
		
		try:
			data = open_file(open_file_path)
			translate_file(data)
			save_file(data, save_file_path)
		    
		except Exception as e:
		    print(f'\n\nError en el archivo : {open_file_path} ...',e)
		    errores.append([open_file_path,e])
		    save_file(data, save_file_path)
		    create_debug(save_file_path, errores)

	except Exception as err:
		print("error: ",err)
	
	

	  	  
print('Done.\nErrores: \n', errores)