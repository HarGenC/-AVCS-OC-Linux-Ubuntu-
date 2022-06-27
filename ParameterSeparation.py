from fuzzywuzzy import fuzz

def parameterSeparation(voiceResponse: str, command):
	if command == None:
		return None
	list = voiceResponse.split()
	list2 = []
	if voiceResponse != "":
		for i in range(1, len(list) + 1):
			string = ""
			for j in range(i):
				string = string + " " + list[j]
			list2.append(string[1:])
	max = 0
	resultResponse = ""
	for item in list2:
		for response in command.voiceResponse:
			resultСomparison = fuzz.WRatio(item, response)
			if resultСomparison > max:
				max = resultСomparison
				resultResponse = item

	if voiceResponse == resultResponse or len(voiceResponse) == len(resultResponse):
		return None
	else:
		return voiceResponse[len(resultResponse) + 1:]