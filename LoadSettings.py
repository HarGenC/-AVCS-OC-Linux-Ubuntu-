import json

class LoadSettings():
	def LoadSettings(self):
		data = ""
		with open("./Settings.json", "r",  encoding='utf-8') as file:
			data = json.load(file)
		return data

	def SaveSettings(self, data):
		with open("./Settings.json", "w",  encoding='utf-8') as writeFile:
			json.dump(data, writeFile, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))