
import json, os, re
from googletrans import Translator
from pathlib import Path
#pip install googletrans==4.0.0rc1
from itertools import chain

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
			
			
def is_dialog(text):
    extensions = [".mp3", ".png", ".jpeg", ".ogg", ".jpg", ".wav"]
    return (
        " " in text
        and all(ext not in text for ext in extensions)
        and text.replace("\'", "") not in special_words
    )

def is_complex_text(text):
	return "|f|" in text

def create_debug(open_file_path = "", errores = "", other_content=None):
	with open('-needTranslated.txt', 'a', encoding='utf-8') as f:
		content=f"\n{open_file_path}    {other_content}\n{errores or ""}\n\n\n"
		f.write(content)

def get_text_events(data,  path, list_of_paths, data_translated=None):
	dialog_total = 0
	iguales=0
	xy = ""
	
	for a in range(len(data["EventText"])): 
		textEvent = data["EventText"][a]["theScene"]
		for b in range(len(textEvent)):
			text = str(textEvent[b])
			if is_dialog(text):
				dialog_total += 1
				if data["EventText"][a]["theScene"][b] == data_translated["EventText"][a]["theScene"][b]:
					iguales+=1
					xy += f"Event: {a}, Scene: {b} Text: {data_translated["EventText"][a]["theScene"][b]}\n"
						
				print(f"Name File: {path} \n Num File: {list_of_paths.index(path)} / {len(list_of_paths)} \n Event: {a} / {len(data['EventText'])} \n SceneNum: {b} / {len(textEvent)}\n")
	create_debug(path,  other_content=f"\nNeed Translation:  {iguales} / {dialog_total}", errores=xy)
				
				
def init_translation(files_paths, func):
	for file_path in files_paths:
		open_file_path = f"./{file_path}"
		open_translated_file_path = f"./ES/{file_path}"
		dirname_save_file = os.path.dirname(open_translated_file_path)
		
		if os.path.isfile(open_translated_file_path):

			try:
				data = open_file(open_file_path)
				data_translated = open_file(open_translated_file_path)
				func(data, file_path, files_paths, data_translated=data_translated)
				
				#save_file(data, save_file_path)
				
			except Exception as e:
				print(f'\n\nError en el archivo : {open_file_path} ...',e)
			    #save_file(data, save_file_path)
				create_debug(open_file_path, e)
		else:
			print("Archivo inexistente")

def init():
	init_translation(files_path_events, get_text_events)

init()
	  	  