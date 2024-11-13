"""
Python 3.12.3
Encoding: UTF-8
"""
# Windows: Before running the script, run "chcp 65001" in the console
# chcp 65001
# Set InputEncoding and OutputEncoding to UTF8
# https://learn.microsoft.com/en-us/answers/questions/213769/what-are-the-differences-between-chcp-65001-and-(c

import json, os, re
from googletrans import Translator
from pathlib import Path
#pip install googletrans==4.0.0rc1
from itertools import chain

input_lang = "en"
output_lang = "es"

#https://proxyscrape.com/free-proxy-list
# To avoid bans for too many queries
translator = Translator(
	user_agent="Mozilla/5.0 (U; Linux i581 x86_64) Gecko/20100101 Firefox/52.6",
    proxies = {
		'http':'154.85.58.149:80',
		'http':'63.143.57.116:80',
		'http':'165.232.129.150:80',
		'http':'162.223.90.130:80',
		'http':'144.126.216.57:80',
		'http':'12.176.231.147:80',
		}
)

def get_paths(folder):
	path = r"MonGirlDreams-Alpha-v26.6-pc/game/Json/"
	if os.path.exists(path): #PC
		return [archivo.as_posix() for archivo in Path(path+folder).glob("**/*.json")]
	elif os.path.exists(f"./x-{folder}"): #Android (extract .APK)
		return [archivo.as_posix() for archivo in Path(f"./x-{folder}").glob("**/*.json")]
	else:
		raise Exception("Problems defining the route")
	

files_path_events = get_paths('Events') #OK
files_path_skill = get_paths('Skills') #
files_path_monster = get_paths('Monsters')#
files_path_adventures = get_paths('Adventures') # 
files_path_fetishes = get_paths('Fetishes') #
files_path_items = get_paths('Items') #
files_path_locations = get_paths('Locations') #
files_path_perks = get_paths('Perks')


def get_file_words():
	if os.path.isfile("./SpecialWord.txt"):
		with open("./SpecialWord.txt", "r", encoding="UTF-8") as f:
			return f.read()
	else:
		raise Exception('"SpecialWords.txt" is not found, it is necessary for correct execution.')
		

special_words = repr(get_file_words().replace("\"", "").replace("\'", "").replace("[",""). replace("]","")).split(", ")
special_words = list(set(special_words))


def open_json_file(input_file_name):
	try: 
		with open(input_file_name, 'r', encoding='utf-8') as f:
			return json.load(f)    
	except:
		with open(input_file_name, 'r') as f:
			return json.load(f)

def save_json_file(data, output_file_name):
	with open(output_file_name, 'w', encoding="UTF-8") as f:
  	  json.dump(data, f, ensure_ascii=False, indent=4)

def create_debug(open_file_path = "", err = "", other_content=None):
	with open('-Errores_debug.txt', 'a', encoding='utf-8') as f:
		content=f"\n{open_file_path}    {other_content}\n{err}\n\n\n"
		f.write(content)

def check_brackets(text):
    # Check if it has [ ]
    return True if re.search(r'[\[\]]', text) else False
    
def correct_brackets(text1, text2):
	#Ensure that the content in brackets is the same as the original
	content1_list = re.findall(r'\[(.*?)\]', text1)
	content2_list = re.findall(r'\[(.*?)\]', text2)
	
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

def translate_complex_text(text, n_event, n_scene, arch):
	try:
		partes = text.split('|f|')
		resultado = []
		for parte in partes:
			if parte:
				resultado.append(parte.split('|n|'))
		for t in range(len(resultado)):
			text = resultado[t][1]
			resultado[t][1] = translator.translate(fr"{text}", dest=output_lang, src=input_lang).text or text			
		union  = ["|n|".join(x) for x in resultado]
		tradd ="|f|" +"|f|".join(union)
		return tradd
		
	except Exception as err:
		print("Error en la libreria de traduccion / Error in the translation library: \n", err)
		aditional_data_err = f"Event: {n_event} SceneNum: {n_scene}"
		create_debug(arch, err, aditional_data_err)
		return None

def translate_simple_text(text, n_event, n_scene, arch):
	try:
		tradd = translator.translate(fr"{text}", dest=output_lang, src=input_lang).text or text
		return tradd
	except Exception as err:
		print("Error en la libreria de traduccion / Error in the translation library: \n", err)
		aditional_data_err = f"Event: {n_event} SceneNum: {n_scene}"
		create_debug(arch, err, aditional_data_err)
		return None

def manager_translation(data="", text="", n_event="", n_scene="", path="", list_of_paths=[]):
	try:
		if is_complex_text(text):
			translated_text = translate_complex_text(text, n_event, n_scene, path) or text
		else:
			translated_text = translate_simple_text(text, n_event, n_scene, path) or text
			
		if check_brackets(text):
			translated_text = correct_brackets(translated_text, text)
		
		data["EventText"][n_event]["theScene"][n_scene] = translated_text
	except Exception as err:
		aditional_data = f"Error en el evento {n_event}, escena {n_scene}: {text}"
		print(aditional_data)
		create_debug(path, err, aditional_data)
			
	print(
		f"Name File: {path} \n",
		f"Num File: {list_of_paths.index(path)} / {len(list_of_paths)} \n",
		f"Event: {n_event} / {len(data['EventText'])} \n", 
		f"SceneNum: {n_scene} / {len(data["EventText"][n_event]["theScene"])}\n", 
		translated_text,"\n"
		)


def get_text_events(data, path, list_of_paths):
	for a in range(len(data["EventText"])): 
		textEvent = data["EventText"][a]["theScene"]
		for b in range(len(textEvent)):
			text = str(textEvent[b])
			if is_dialog(text):
				manager_translation(data=data, text=text, n_event=a, n_scene=b, path=path, list_of_paths=list_of_paths)

def get_text_skill(data, path, list_of_paths):
	pass

def get_text_monster(data, path, list_of_paths):
	pass

def get_text_adventures(data, path, list_of_paths):
	pass

def get_text_fetishes(data, path, list_of_paths):
	pass

def get_text_items(data, path, list_of_paths):
	pass

def get_text_locations(data, path, list_of_paths):
	pass

def get_text_perks(data, path, list_of_paths):
	pass
	
def init_translation(files_paths, func):
	for file_path in files_paths:
		open_file_path = f"./{file_path}"
		save_file_path = f"./ES/{file_path}"
		dirname_save_file = os.path.dirname(save_file_path)
		
		if not(os.path.isfile(save_file_path)):		
			os.makedirs(dirname_save_file, exist_ok=True)		
				
			try:
				data = open_json_file(open_file_path)
				func(data, file_path, files_paths)
				save_json_file(data, save_file_path)
			except Exception as e:
				print(f'\n\nError en el archivo : {open_file_path} ...',e)
				#save_file(data, save_file_path)
				create_debug(open_file_path, e)
		else:
			print("Archivo existente")

def init():
	init_translation(files_path_events, get_text_events)
	"""
	init_translation(files_path_skill, get_text_skill)
	init_translation(files_path_monster, get_text_monster)
	init_translation(files_path_adventures, get_text_adventures)
	init_translation(files_path_fetishes, get_text_fetishes)
	init_translation(files_path_items, get_text_items)
	init_translation(files_path_locations, get_text_locations)
	init_translation(files_path_perks, get_text_perks)
	"""

init()
	  	  
print('Done.\n')