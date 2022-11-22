import re


def inputRex(label:str = "", error:str = "Entered string musst match the pattern!", pattern:str = ".*"):
	while True:
		line = input(label)
		if re.match(pattern, line) == None:
			print(error)
		else:
			return line


def inputInt(label:str = "", error:str = "Please enter a number!") -> int:
	while True:
		line = input(label)
		if not line.isnumeric():
			print(error)
		else:
			return int(line)


def inputBool(label:str = "", valTrue:str = "true", valFalse:str = "false", error:str = "DEFAULT") -> bool:
	if error == "DEFAULT":
		error = "Please enter eigther '%s' or '%s'!" % (valTrue, valFalse)
	while True:
		line = input(label)
		if not line.lower() in [valTrue.lower(), valFalse.lower()]:
			print(error)
		else:
			return line.lower() == valTrue.lower()


def inputChoice(title:str, options:dict, error:str = "Please enter one of the listed options via its number!", bottom:str="", label:str=": ") -> any:
	while True:
		print(title)
		i = 1
		l = len(str(len(options)))
		for key in options:
			print("  (" + ((" " * l + str(i))[-l:]) + ") %s" % key)
			i += 1
		if len(bottom) > 0:
			print(bottom)
		i = inputInt(label, error)
		if i > len(options) or i <= 0:
			print(error)
		else:
			return options[list(options.keys())[i - 1]]


if __name__ == "__main__":
	def main():
		strIn = input("String: ")
		intIn = inputInt("Integer: ")
		boolIn = inputBool("Bool: ")
		choiceIn = inputChoice(
			"Options:",
			{
				"Opt1": 1,
				"Opt2": 2,
				"Opt3": 3,
				"Opt4": 4,
				"Opt5": 5,
				"Opt6": 6,
				"Opt7": 7,
				"Opt8": 8,
				"Opt9": 9,
				"Opt10": 10,
				"Opt11": 11,
			})
		print("strIn:    %s" % strIn)
		print("intIn:    %s" % intIn)
		print("boolIn:   %s" % boolIn)
		print("choiceIn: %s" % choiceIn)
	main()