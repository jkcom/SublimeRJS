import json
from pprint import pprint

def initializeContext(context):
	# load settings
	json_data = open(context.settingsPath)
	data = json.load(json_data)
	json_data.close()
	context.setSettings(data)
	# load require main
	if data["require_main"] is not "":
		loadRequireMain(context)
	else:
		context.setModuleAliasMap({})


def loadRequireMain(context):	
		print context.getBaseDir() + context.settings["require_main"]
		f = open(context.getBaseDir() + context.settings["require_main"], "r")
		data = f.read()
		configString = data[data.find("(", data.find("require.config")) + 1:data.find(")", data.find("require.config("))].replace("'", '"')
		f.close()
		# find paths
		if configString.find("paths") is not -1:
			pathsString = configString[configString.find("{", configString.find("paths")) + 1:configString.find("}", configString.find("paths"))].replace(" ", "").strip().replace('\n', "")
			pathElements = pathsString.split(",")
			aliasMap = {}
			for alias in pathElements:
				value = alias.split(":")[0]
				key = alias.split(":")[1].replace("'", "").replace('"', "")
				aliasMap[key] = value
			context.setModuleAliasMap(aliasMap)


