"""
Python 3.12.3
Encoding: UTF-8
"""
# Windows: Before running the script, run "chcp 65001" in the console
# chcp 65001
# Set InputEncoding and OutputEncoding to UTF8
# https://learn.microsoft.com/en-us/answers/questions/213769/what-are-the-differences-between-chcp-65001-and-(c

import json, os, re, random, requests
#deepl   # Import Deepl or Google Translate but do not import both at the same time
from googletrans import Translator
#pip install googletrans==4.0.0rc1
from pathlib import Path
from itertools import chain

input_lang = "en"
output_lang = "es"
output_lang2 = "ES"

#Deepl:
#"auth_key = "insert Api Key..."  # Replace with your key. limit: 500.000 characters (free)
#translator = deepl.Translator(auth_key)
#translator.translate_text("Hello, world!", target_lang=output_lang)


#To translate groups instead of 1 by 1, 
#5k limit of letters?, googletrans
temp_dialog_text = {
	"1":[],
	"2":[],
	"3":[],
	"4":[],
	"5":[],
	"6":[],
	"7":[],
	"8":[],
	"9":[],
	"10":[],
	}

# https://proxyscrape.com/free-proxy-list
# To avoid bans for too many queries
list_of_proxies = {
	                "0":['http','138.68.60.8:8080'],
					"1":['http','4.157.219.21:80'],
					"2":['http','172.191.74.198:8080'],
					"3":['http','35.92.233.193:80'],
					"4":['http','198.49.68.80:80'],
					"5":['http','129.10.76.179:80'],
					"6":['http','23.237.145.36:31288'],
					"7":['http','138.68.60.8:3128'],
					"8":['http','172.191.74.198:8080'],
					"9":['http','172.212.97.167:80'],
					"10":['http','12.176.231.147:80'],
					"11":['http','132.145.134.243:31288'],
					"12":['http','162.223.90.130:80'],
					"13":['http','142.93.202.130:3128'],
					"14":['http','132.145.134.243:31288'],
					"15":['http','138.68.60.8:8080'],
					"16":['http','23.247.136.245:80'],
					"17":['http','63.143.57.116:80'],
					"18":['http','165.232.129.150:80'],
					"19":['http','162.223.90.130:80'],
					"20":['http','144.126.216.57:80'],
					"21":['http','12.176.231.147:80'],
					}
#googletrans
def recharge_construct():
	global translator
	num_random = random.randint(0, len(list_of_proxies)-1)
	translator = Translator(
				user_agent = "Mozilla/5.0 (Android; Android 5.1.1; SAMSUNG SM-G9350L Build/LMY47X) AppleWebKit/603.19 (KHTML, like Gecko)  Chrome/54.0.1522.302 Mobile Safari/601.0",
				proxies = {
					list_of_proxies[str(num_random)][0]:list_of_proxies[str(num_random)][1]
					}
			)
	print("\nProxy actual: ", translator.client.proxies)
	create_debug(translator.client.proxies)


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
		content=f"{open_file_path}    {other_content}\n{err}\n"
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


""" 
To improve validation: Before each dialog, 
generally, there is: a text that says "speak", 
there is a dialog, there is an emotion / expression 
(smile, etc.) (In events, I don't 
remember if it is the same in the others).
"""
def is_dialog(text):
    extensions = [".mp3", ".png", ".jpeg", ".ogg", ".jpg", ".wav"]
    return (
        " " in text
        and all(ext not in text for ext in extensions)
        and text.replace("\'", "") not in special_words
    )

def is_complex_text(text):
	return "|f|" in text

def alternative_translate_request(text, lang_src="auto", lang_out="es"):
	response = requests.post("https://trans.zillyhuhn.com/translate", 
                         headers={"Content-Type": "application/json"}, 
                         data=json.dumps({
                             "q": text,
                             "source": lang_src,
                             "target": lang_out,
                             "format": "text",
                             "alternatives": 1,
                             "api_key": ""
                         }))
	try:
		text = str(response.json()["translatedText"]) or text
		return text
	except:
		return None


def translate_complex_text(text, n_event, n_scene, arch):
	try:
		partes = text.split('|f|')
		resultado = []
		for parte in partes:
			if parte:
				resultado.append(parte.split('|n|'))
		for t in range(len(resultado)):
			text = resultado[t][1]
			#resultado[t][1] = translator.translate_text(text=str(text), target_lang=output_lang2).text or text     #deepl
			#resultado[t][1] = alternative_translate_request(text, lang_src=input_lang, lang_out=output_lang) or text
			resultado[t][1] = translator.translate(text, dest=output_lang, src=input_lang).text or text			#googletrans
		union  = ["|n|".join(x) for x in resultado]
		tradd ="|f|" +"|f|".join(union)
		return tradd
		
	except Exception as err:
		print("Error en la libreria de traduccion / Error in the translation library: \n", err)
		aditional_data_err = f"Event: {n_event} SceneNum: {n_scene}, Raiz: translate_complex_text()\nText: {text}"
		create_debug(arch, err, aditional_data_err)
		recharge_construct() #googletrans
		return None

def translate_simple_text(text, n_event, n_scene, arch):
	try:
		#tradd = translator.translate_text(text=str(text), target_lang=output_lang2).text or text #Deepl
		#tradd = alternative_translate_request(text, lang_src=input_lang, lang_out=output_lang) or text
		tradd = translator.translate(text, dest=output_lang, src=input_lang).text or text   #googletrans
		return tradd
	except Exception as err:
		print("Error al traducir / Error in the translation: \n", err)
		aditional_data_err = f"\nEvent: {n_event} SceneNum: {n_scene}, Raiz: translate_simple_text()\nText: {text}"
		create_debug(arch, err, aditional_data_err)
		recharge_construct()  #googletrans
		return None

def manager_translation(data="", text="", n_event="", n_scene="", path="", list_of_paths=[]):
	try:
		if is_complex_text(text):
			translated_text = translate_complex_text(text, n_event, n_scene, path) or text
		else:
			translated_text = translate_simple_text(text, n_event, n_scene, path) or text
			
		if check_brackets(text):
			translated_text = correct_brackets(translated_text, text)
		
		print(
		f"Name File: {path} \n",
		f"Num File: {list_of_paths.index(path)} / {len(list_of_paths)} \n",
		f"Event: {n_event} / {len(data['EventText'])} \n", 
		f"SceneNum: {n_scene} / {len(data["EventText"][n_event]["theScene"])}\n", 
		translated_text,"\n"
		)

		return translated_text
	except Exception as err:
		aditional_data = f"Error en el evento {n_event}, escena {n_scene}: {text}, Raiz: manager_translation()\nText: {text}"
		print(aditional_data)
		create_debug(path, err, aditional_data)
		return text



def get_text_events(data, path, list_of_paths):
	for a in range(len(data["EventText"])): 
		textEvent = data["EventText"][a]["theScene"]
		for b in range(len(textEvent)):
			text = str(textEvent[b])
			if is_dialog(text):
				translated_text = manager_translation(data=data, text=text, n_event=a, n_scene=b, path=path, list_of_paths=list_of_paths)
				data["EventText"][a]["theScene"][b] = translated_text

def get_text_skill(data, path, list_of_paths):
	val = ["descrip", "outcome", "miss", "statusOutcome", "statusText"]
	for tag in val:
		try:
			text = str(data[tag])
		except:
			text = "no"
		if is_dialog(text):
			translated_text = manager_translation(data=data, text=text, n_event=tag, n_scene="nothing...", path=path, list_of_paths=list_of_paths)
			data[tag] = translated_text

def get_text_monster(data, path, list_of_paths):
	val = ["description", "combatDialogue", "encyclopedia"] #"victoryScenes"
	for tag in val:
		if not (tag == "description"):
			try:
				if data[tag]:
					for a in range(len(data[tag])): 
						textEvent = data[tag][a]["theText"]
						for b in range(len(textEvent)):
							text = str(textEvent[b])
							if is_dialog(text):
								translated_text = manager_translation(data=data, text=text, n_event=a, n_scene=b, path=path, list_of_paths=list_of_paths)
								data[tag][a]["theText"][b] = translated_text
			except:
				pass
		else:
			text = str(data[tag])
			if is_dialog(text):
				translated_text = manager_translation(data=data, text=text, n_event=tag, n_scene="nothing...", path=path, list_of_paths=list_of_paths)
				data[tag] = translated_text


def get_text_adventures(data, path, list_of_paths):
	try:
		text = str(data["description"])
		if is_dialog(text):
			translated_text = manager_translation(data=data, text=text, n_event="description", n_scene="nothing...", path=path, list_of_paths=list_of_paths)
			data["description"] = translated_text
	except:
		pass
	

def get_text_fetishes(data, path, list_of_paths):
	for a in range(len(data["FetishList"])): 
		text = data["FetishList"][a]["CreationOn"]
		text1 = data["FetishList"][a]["CreationOff"]
		if is_dialog(text):
			translated_text = manager_translation(data=data, text=text, n_event=a, n_scene="nothing...", path=path, list_of_paths=list_of_paths)
			data["FetishList"][a]["CreationOn"] = translated_text
		if is_dialog(text1):
			translated_text = manager_translation(data=data, text=text1, n_event=a, n_scene="nothing...", path=path, list_of_paths=list_of_paths)
			data["FetishList"][a]["CreationOff"] = translated_text


def get_text_items(data, path, list_of_paths):
	val = ["descrip", "useOutcome", "useMiss"]
	for tag in val:
		try:
			text = str(data[tag])
		except:
			text = "no"
		if is_dialog(text):
			translated_text = manager_translation(data=data, text=text, n_event=tag, n_scene="nothing...", path=path, list_of_paths=list_of_paths)
			data[tag] = translated_text

def get_text_locations(data, path, list_of_paths):
	pass

def get_text_perks(data, path, list_of_paths):
	tag = "description"
	try:
		text = str(data[tag])
	except:
		text = "no"
	if is_dialog(text):
		translated_text = manager_translation(data=data, text=text, n_event=tag, n_scene="nothing...", path=path, list_of_paths=list_of_paths)
		data[tag] = translated_text
	
def init_translation(files_paths, func):
	for file_path in files_paths:
		open_file_path = f"./{file_path}"
		save_file_path = f"./ES/{file_path}"
		dirname_save_file = os.path.dirname(save_file_path)
		
		if not(os.path.isfile(save_file_path)):		
			os.makedirs(dirname_save_file, exist_ok=True)
			recharge_construct()
				
			try:
				data = open_json_file(open_file_path)
				func(data, file_path, files_paths)
				save_json_file(data, save_file_path)
			except Exception as e:
				print(f'\n\nError en el archivo : {open_file_path} ...',e)
				aditional_data = "Raiz: init_translation()"
				create_debug(open_file_path, e, aditional_data)
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
	#init_translation(files_path_locations, get_text_locations)
	init_translation(files_path_perks, get_text_perks)
	"""

init()
	  	  
print('Done.\n')