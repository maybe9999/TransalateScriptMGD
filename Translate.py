import json, os, re
from googletrans import Translator
from pathlib import Path
#pip install googletrans==4.0.0rc1
from itertools import chain

input_lang = "en"
output_lang =  "es"

translator = Translator()

def get_paths(folder):
	return [archivo.as_posix() for archivo in Path(folder).glob("**/*.json")]

files_path_skill = get_paths('./x-Skills')#

files_path_monster = get_paths('./x-Monsters')#

files_path_adventures = get_paths('./x-Adventures') # 

files_path_fetishes = get_paths('./x-Fetishes') #

files_path_items = get_paths('./x-Items') #

files_path_locations = get_paths('./x-Locations') #

files_path_events = get_paths('./x-Events') #

files_path_perks = get_paths('./x-Perks')

def open_file():
	with open("./SpecialWord.txt", "r") as f:
		return f.read()
		
special_words = repr(open_file().replace("\"", "").replace("\'", "").replace("[",""). replace("]","")).split(", ")

special_words = list(set(special_words))


def open_file(input_file_name):
	try: 
		with open(input_file_name, 'r', encoding='utf-8') as f:
			return json.load(f)    
	except:
		with open(input_file_name, 'r') as f:
			return json.load(f)

def check_brackets(text):
    # Verificar si el texto contiene corchetes [] o llaves {}
    return True if re.search(r'[\[\]]', text) else False
    
def correct_brackets(text1, text2):
	# Encontrar todas las coincidencias entre corchetes en ambos textos
	content1_list = re.findall(r'\[(.*?)\]', text1)
	content2_list = re.findall(r'\[(.*?)\]', text2)
	
	# Reemplazar cada elemento de text1 con el correspondiente de text2
	for content1, content2 in zip(content1_list, content2_list):
		text1 = text1.replace(f'[{content1}]', f'[{content2}]')
		return text1

def is_dialog(text):
    extensions = [".mp3", ".png", ".jpeg", ".ogg", ".jpg", ".wav"]
    return (
        " " in text
        and all(ext not in text for ext in extensions)
        and text.replace("\'", "") not in special_words
    )

def is_complex_text(text):
	return "|f|" in text

def translate_complex_text(text, e, a, arch):
	try:
		partes = text.split('|f|')
		resultado = []
		for parte in partes:
			if parte:
				resultado.append(parte.split('|n|'))
		for t in range(len(resultado)):
			text = resultado[t][1]
			resultado[t][1] = translator.translate(fr"{text}", dest=output_lang).text or text			
		union  = ["|n|".join(x) for x in resultado]
		tradd ="|f|" +"|f|".join(union)
		return tradd
		
	except Exception as err:
		aditional_data_err = f"Event: {e} SceneNum: {a}"
		create_debug(arch, err, aditional_data_err)
		return None

def translate_simple_text(text, e, a, arch):
	try:
		tradd = translator.translate(fr"{text}", dest=output_lang).text or text
		return tradd
	except Exception as err:
		aditional_data_err = f"Event: {e} SceneNum: {a}"
		create_debug(arch, err, aditional_data_err)
		return None

def get_text_events(data, path, list_of_paths):
	for a in range(len(data["EventText"])): 
		textEvent = data["EventText"][a]["theScene"]
		for b in range(len(textEvent)):
			text = str(textEvent[b])
			if is_dialog(text):
				
				if is_complex_text(text):
					translated_text = translate_complex_text(text, a, b, path) or text
				else:		
					translated_text = translate_simple_text(text, a, b, path) or text
					
				if check_brackets(text):
					translated_text = correct_brackets(translated_text, text)
				
				
				data["EventText"][a]["theScene"][b] = translated_text
						
				print(f"Name File: {path} \n Num File: {list_of_paths.index(path)} / {len(list_of_paths)} \n Event: {a} / {len(data['EventText'])} \n SceneNum: {b} / {len(textEvent)}\n", translated_text,"\n")


def save_file(data, output_file_name):
	with open(output_file_name, 'w') as f:
  	  json.dump(data, f, ensure_ascii=False, indent=4)

def create_debug(open_file_path = "", errores = "", other_content=None):
	with open('-Errores_debug.txt', 'a', encoding='utf-8') as f:
		content=f"\n{open_file_path}    {other_content}\n{errores}\n\n\n"
		f.write(content)
	
def init_translation(files_paths, func):
	for file_path in files_paths:
		open_file_path = f"./{file_path}"
		save_file_path = f"./ES/{file_path}"
		dirname_save_file = os.path.dirname(save_file_path)
		
		if not(os.path.isfile(save_file_path)):		
			os.makedirs(dirname_save_file, exist_ok=True)		
				
			
			data = open_file(open_file_path)
			func(data, file_path, files_paths)
			save_file(data, save_file_path)
			"""
			except Exception as e:
			    print(f'\n\nError en el archivo : {open_file_path} ...',e)
			    #save_file(data, save_file_path)
			    create_debug(open_file_path, e)
			"""
		else:
			print("Archivo existente")

def init():
	init_translation(files_path_events, get_text_events)

init()
	  	  
print('Done.\n')