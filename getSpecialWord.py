import json, os, re
from pathlib import Path
from itertools import chain

list_word = []

def get_paths(folder):
	path = r"MonGirlDreams-Alpha-v26.6-pc/game/Json/"
	if os.path.exists(path): #PC
		return [archivo.as_posix() for archivo in Path(path+folder).glob("**/*.json")]
	elif os.path.exists(folder): #Android (extract .APK)
		return [archivo.as_posix() for archivo in Path(folder).glob("**/*.json")]
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


def open_file(input_file_name):
	try: 
		with open(input_file_name, 'r', encoding='utf-8') as f:
			return json.load(f)    
	except:
		with open(input_file_name, 'r') as f:
			return json.load(f)

def get_name_root(data, tag):
	try:
		if " " in data[tag] and len(data[tag]) >=2:
			return data[tag]
	except:
		return False

#x-Skills
def get_special_wor_skill(data):
	list_wor = []
	val = ["skillTags","statType", "fetishTags", "requiresStance","startsStance", "skillType", "unusableIfStance", "unusableIfTarget", "removesStance", "requiresStatusEffect", "unusableIfStatusEffect", "statusEffect", "statusResistedBy", "name" ]
	
	list_wor.append(data["name"]) if get_name_root(data, "name") else None
			
	for tag in val:
		try:
			for a in range(len(data[tag])):
				b = data[tag]
				list_wor.append(b[a]) if get_name_root(data, [a]) else None
		except Exception as err:
			pass
	return list_wor

#x-Monsters
def get_special_wor_monster(data):
	list_wor = []
	val = ["name", "requires", "skillList", "perks", "Fetishes","ItemDropList", "lossScenes", "victoryScenes"]
	
	list_wor.append(data["name"]) if get_name_root(data, "name") else None
	list_wor.append(f"Random {data['name']}") if get_name_root(data, "name") else None
	try:
		list_wor.append(f'Random {data["name"]}')
		list_wor.append(data["name"])
	except:
		pass
		
	try:
		list_wor.append(data["IDname"])
		list_wor.append(f"Random {data['IDname']}")
	except:
		pass

	
	for a in range(15):
		try:
			list_wor.append(f'{data["name"]} {a+1}')
		except:
			pass
	
	list_wor.append(data["IDname"]) if get_name_root(data, "IDname") else None
	list_wor.append(f"Random {data['IDname']}") if get_name_root(data, "IDname") else None
		
	for tag in val:
		try:
			for a in range(len(data[tag])):
				b = data[tag][a]
				
				list_wor.append(b["name"]) if get_name_root(b, "name") else None
				list_wor.append(f"Random {b['name']}") if get_name_root(b, "name") else None
				
				list_wor.append(b["NameOfScene"]) if get_name_root(b, "NameOfScene") else None
				
				if " " in b and len(b) >= 2:
					list_wor.append(b)
		except Exception as err:
			pass
	return list_wor
	

#x-Events
def get_special_wor_events(data):
	list_wor = []
	
	list_wor.append(data["name"]) if get_name_root(data, "name") else None
	
	for a in range(len(data["EventText"])): #Lista de eventos
		b = data["EventText"][a]
	
		list_wor.append(b["NameOfScene"]) if get_name_root(b, "NameOfScene") else None # list Texto del evento
	return list_wor


def get_special_wor_adventures(data):
	list_wor = []
	val = ["requires", "Deck", "RandomMonsters", "RandomEvents", ]
	list_wor.append(data["name"]) if get_name_root(data, "name") else None
	
	for tag in val:
		try:
			for a in range(len(data[tag])):
				b = data[tag]
				list_wor.append(b[a]) if get_name_root(b, [a]) else None
				list_wor.append(f"Random {b[a]}") if get_name_root(b, [a]) else None
		except:
			pass
	return list_wor

def get_special_wor_fetish(data):
	list_wor = []
	try:
		for a in range(len(data["FetishList"])):
			b = data["FetishList"][a]
			list_wor.append(b["Name"]) if get_name_root(b, ["Name"]) else None
	except:
		pass
	return list_wor

def get_special_wor_items(data):
	list_wor = []
	val = ["requires","perks","skills"]
	
	list_wor.append(data["name"]) if get_name_root(data, "name") else None
	
	for tag in val:
		try:
			for a in range(len(data[tag])):
				b = data[tag]
				list_wor.append(b[a]) if get_name_root(b, [a]) else None
		except:
			pass
	return list_wor
	
def get_special_wor_location(data):
	list_wor = []
	val = ["requires","FullyUnlockedBy","Monsters", "Events", "Quests", "Adventures"]
	
	list_wor.append(data["name"]) if get_name_root(data, "name") else None
	list_wor.append(data["exploreTitle"]) if get_name_root(data, "exploreTitle") else None
	
	for tag in val:
		try:
			for a in range(len(data[tag])):
				b = data[tag]
				list_wor.append(b[a]) if get_name_root(b, [a]) else None
		except:
			pass
	return list_wor


def get_special_wor_perks(data):
	list_wor = []
	val = ["PerkReq","StatReq","PerkType"]
	
	list_wor.append(data["name"]) if get_name_root(data, "name") else None
	
	for tag in val:
		try:
			for a in range(len(data[tag])):
				b = data[tag]
				list_wor.append(b[a]) if get_name_root(b, [a]) else None
		except:
			pass
	return list_wor


def save_file(data, output_file_name):
	with open(output_file_name, 'w', encoding="UTF-8") as f:
  	  f.write(repr(data))


def init_get_word(files_paths, func):
	for file_path in files_paths:
		open_file_path = f"./{file_path}"
			
		data = open_file(open_file_path)
		list_word.append(func(data))
	print(files_paths[0], "Len:  ", len(list_word))
	


def init():
	global list_word
	init_get_word(files_path_skill, get_special_wor_skill)
	
	init_get_word(files_path_monster, get_special_wor_monster)
	
	init_get_word(files_path_events, get_special_wor_events)
	
	init_get_word(files_path_adventures, get_special_wor_adventures)
	
	init_get_word(files_path_fetishes, get_special_wor_fetish)
	
	init_get_word(files_path_items, get_special_wor_items)
	
	init_get_word(files_path_locations, 
	get_special_wor_location)
	
	init_get_word(files_path_perks, get_special_wor_perks)
	
	
	list_word = list(chain.from_iterable(list_word))
	
	list_word = [str(elemento) for elemento in list_word if not (len(elemento) <= 1 and (elemento == "" or elemento == " "))]
	
	print("Total len(Before): ", len(list_word))
	
	list_word = list(set(list_word))

	print("Total len(After): ", len(list_word))
	
	save_file(list_word, "SpecialWord.txt")
	
init()
"""		
def open_file():
	with open("./SpecialWord.txt", "r") as f:
		return f.read()
		
arch = repr(open_file().replace("\"", "").replace("\'", "").replace("[",""). replace("]","")).split(",")

print(type(arch))
print(len(arch),"\n")

arch = list(set(arch))

print("\n",type(arch))
print(len(arch))

print(arch)
"""