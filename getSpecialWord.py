import json, os, re
from pathlib import Path
from itertools import chain

list_word = []

files_path_skill = [archivo.as_posix() for archivo in Path('./x-Skills').glob("**/*.json")]

files_path_monster = [archivo.as_posix() for archivo in Path('./x-Monsters').glob("**/*.json")]


def open_file(input_file_name):
	try: 
		with open(input_file_name, 'r', encoding='utf-8') as f:
			return json.load(f)    
	except:
		with open(input_file_name, 'r') as f:
			return json.load(f)

#x-Skills
def get_special_wor_skill(data):
	list_wor = []
	val = ["skillTags","statType", "fetishTags", "requiresStance","startsStance", "skillType", "unusableIfStance", "unusableIfTarget", "removesStance", "requiresStatusEffect", "unusableIfStatusEffect", "statusEffect", "statusResistedBy", "name" ]
	
	try:
		if " " in data["name"]:
			list_wor.append(data["name"])
	except:
		pass
	
	for tag in val:
		try:
			for a in range(len(data[tag])):
				b = data[tag][a]
				if " " in b and len(b) >= 2:
					list_wor.append(b)
		except Exception as err:
			print(err)
	return list_wor
	
def get_special_wor_monster(data):
	list_wor = []
	val = ["name", "requires", "skillList", "perks", "Fetishes","ItemDropList", "lossScenes", "victoryScenes"]
	try:
		if " " in data["name"]:
			list_wor.append(data["name"])
	except:
		pass
	try:
		if " " in data["IDname"]:
			list_wor.append(data["IDname"])
	except:
		pass
		
	for tag in val:
		try:
			for a in range(len(data[tag])):
				b = data[tag][a]
				try:
					if " " in b["name"]:
						list_wor.append(b["name"])
				except:
					pass
				try:
					if " " in b["NameOfScene"]:
						list_wor.append(b["NameOfScene"])
				except:
					pass 
				if " " in b and len(b) >= 2:
					list_wor.append(b)
		except Exception as err:
			print(err)
	return list_wor
	

#x-Events
def get_special_wor(data):
	list_wor = []
	for a in range(len(data["EventText"])): #Lista de eventos
		if " " in a:
			list_wor.append(data["EventText"][a]["NameOfScene"]) # list Texto del evento
	print(list_wor)
	return list_wor


def save_file(data, output_file_name):
	with open(output_file_name, 'w') as f:
  	  f.write(str(data))
	
	
for file_path in files_path_skill:
	open_file_path = f"./{file_path}"
	
	print("file",open_file_path)

	data = open_file(open_file_path)
	list_word.append(get_special_wor_skill(data))

for file_path in files_path_monster:
	open_file_path = f"./{file_path}"
	
	print("file",open_file_path)

	data = open_file(open_file_path)
	list_word.append(get_special_wor_monster(data))



list_word = list(chain.from_iterable(list_word))

list_word = list(set(list_word))
print(list_word)

save_file(list_word, "SpecialWord.txt")