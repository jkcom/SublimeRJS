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
		print "REQUIRE MAIN", context.getBaseDir() + context.settings["require_main"]
		f = open(context.getBaseDir() + context.settings["require_main"], "r")
		data = f.read()
		f.close();
		if data.find("require.config") != -1:
			configString = data[data.find("(", data.find("require.config")) + 1:data.find(")", data.find("require.config("))].replace("'", '"')
		else:
			configString = "{\n}"
		
		# find paths
		if configString.find("paths") is not -1:
			pathsString = configString[configString.find("{", configString.find("paths")) + 1:configString.find("}", configString.find("paths"))].replace(" ", "").strip().replace('\n', "")
			pathsString = pathsString.replace("	", "")
			pathElements = pathsString.split(",")
			aliasMap = {}
			for alias in pathElements:
				value = alias.split(":")[0]
				key = alias.split(":")[1].replace("'", "").replace('"', "")
				if value != context.settings["texts_name"] or len(context.settings["text_folder"]) == 0:
					aliasMap[key] = value

		else:
			aliasMap = {}

		# add template alias map
		if len(context.settings["text_folder"]) > 0:

			# find texts folder
			stepsToBaseDir = len(context.settings["require_main"].split("/")) - 1
			textsPath = ""
			for x in range(0, stepsToBaseDir):
				textsPath += "../" + context.settings["text_folder"]

			aliasMap[textsPath] = context.settings["texts_name"]

			# remove current paths:
			if configString.find("paths") is not -1:
				pathsString = configString[configString.find("paths"):configString.find("}", configString.find("paths")) + 1]
				configString = configString.replace(pathsString, "{paths-location}")
				pass

			# render new paths block
			pathsString = "paths: {\n"
			for key in aliasMap:
				pathsString += "		" + aliasMap[key] + ": " + "'" + key + "',\n"
			pathsString = pathsString[0:pathsString.rfind(",")] + "\n"
			pathsString += "	}"

			# insert
			if configString.find("{paths-location}") != -1:
				configString = configString.replace("{paths-location}", pathsString)
			else:
				afterPaths = ""
				if configString.find(":") != -1:
					afterPaths = ","
				configString = "{" + "\n	" + pathsString + afterPaths + configString[configString.find("{") + 1:]

			# write in main data
			
			
			if data.find("require.config") != -1:
				newData = data.replace(data[data.find("(", data.find("require.config")) + 1:data.find(")", data.find("require.config("))], configString)
			else:
				newData = "require.config(" + configString + ");\n\n" + data

			f = open(context.getBaseDir() + context.settings["require_main"], "w+")
			f.write(newData)
			f.close()


		# assign to context
		context.setModuleAliasMap(aliasMap)

