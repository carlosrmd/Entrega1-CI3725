# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Cuarta entrega del proyecto.              #
#   Interpretador para el lenguaje Setlan     #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

from sys import stdout, stdin
printf = stdout.write
read = stdin.readline

error_intr = []
SymTab = None
num_scopes = 0
indent_level = 0

def interpreter_traverser(AST):
	global error_intr
	global num_scopes
	global indent_level

	if AST.type == "block":
		num_scopes += 1
		indent_level += 1

	elif AST.type == "block_end":
		indent_level -= 1

	elif AST.type == "print":
		elements = AST.children[0].children
		string = ""
		for elem in elements:
			if elem.type == "str_stmt":
				act = elem.children[0].val[1:-1]
				# Identificar Regex
				act = act.split("\\n")
				for i in range(len(act)-1):
					string = string + act[i] + "\n"
				if act[-1] != "''":
					string = string + act[-1]
		printf(string)

	elif AST.type == "scan":
		variable = AST.children[0].children[0]
		varType = SymTab.typeof(variable.val, num_scopes)
		
		value = read()
		value = value.split("\n")[0]
		valueType = ""

		try:
			value = int(value)
		except ValueError:
			pass
		else:
			valueType = "int"

		if value == "true" or value == "false":
			valueType = "bool"
		elif valueType != "int":
			valueType = "error"
		
		if valueType != varType:
			# Agrega el error a la lista
			if valueType == "bool" or valueType == "int":
				error_intr.append(("inv_type_scan", variable.val, variable.lineno, variable.colno, varType, valueType))
				return False
			else:
				error_intr.append(("inv_norec_scan", variable.val, variable.lineno, variable.colno))
				return False
		else:
			SymTab.update(variable.val, num_scopes, varType, value, SymTab.lin_decof(variable.val, num_scopes))


	# Recorre los hijos del nodo actual
	if AST.children:
		for child in AST.children:
			ch = interpreter_traverser(child)
			if ch == False:
				return False


def execute(AST, ST):
	global SymTab
	SymTab = ST
	inter = interpreter_traverser(AST)

	if inter == None:
		return True
	else:
		return False


def evaluate(expr):
	pass


def get_errors():
	global error_intr
	return error_intr