# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Tercera entrega del proyecto.             #
#   TypeChecker para el lenguaje Setlan       #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

from sl_symtab import SymTab, ST_Stack

# Tipos de errores detectados en esta etapa:

# "redec": Redeclaracion de variable en el mismo alcance
# "nodec": Uso de variable no declarada
# "inv_tex": Tipo de expresion invalido
# "inv_opr": Operacion o tipo de operandos invalidos
# "read_ol": Asignacion a una variable read_only (de un FOR)

error_st = []
strrep_st = ""
num_scopes = 0
indent_level = 0
st_stack = ST_Stack()
symbol_table_final = SymTab()


def build_symbol_table_REC(AST):
	global st_stack
	global strrep_st
	global num_scopes
	global indent_level

	# Inicializacion de los parametros de la entrada a la tabla de simbolos
	name = ""
	def_scope = 0
	type = ""
	val = ""
	lin_dec = 0
	col_dec = 0
	#print(st_stack)
	#print(len(st_stack.stack))
	# Tipos AST de declaracion de variables, apertura y cierre de Scopes
	# Realiza la funcion correspondiente al tipo de nodo (AST.type)
	if AST.type == "block": 
		num_scopes += 1
		st = SymTab()
		st_stack.push(st)

		strrep_st = strrep_st + "\t"*indent_level + "SCOPE" + "\n"
		indent_level += 1

	elif AST.type == "vardec":
		vardec = str(AST.val)
		type = vardec.split()[0]
		var = vardec.split()[1]

		name = str(var)
		dec_scope = num_scopes
		if type == "int": val = "0"
		elif type == "set": val = "{}"
		elif type == "bool": val = "false"
		lin_dec = AST.lineno
		col_dec = AST.colno

		actual_num_scopes = len(st_stack.stack)
		aux = False
		while(actual_num_scopes > 0):
			if st_stack.stack[actual_num_scopes - 1].contains(name, actual_num_scopes):
				aux = True
			actual_num_scopes = actual_num_scopes - 1
		if aux:
			error_st.append(("redec", name, lin_dec, col_dec))
		st_stack.top().insert(name, dec_scope, type, val, lin_dec)
		print(st_stack.stack[0].typeof("n", 1))

		strrep_st = strrep_st + "\t"*indent_level + str(st_stack.top().var_str(name, dec_scope)) + "\n"

	elif AST.type == "for_stmt":
		num_scopes += 1
		st = SymTab()
		st_stack.push(st)

		strrep_st = strrep_st + "\t"*indent_level + "SCOPE" + "\n"
		indent_level += 1

		name = str(AST.children[0].children[0].val)
		dec_scope = num_scopes
		type = "int"
		val = "0"
		lin_dec = AST.lineno
		read_only = 1

		st_stack.top().insert(name, dec_scope, type, val, lin_dec, read_only)

		strrep_st = strrep_st + "\t"*indent_level + str(st_stack.top().var_str(name, dec_scope)) + "\n"

	elif AST.type == "block_end":
		pop_stack_to_st()

	elif AST.type == "assign":
		var_list = getvar_list(AST)
		for var in var_list:
			name = var[0]
			lin_dec = var[1]
			col_dec = var[2]
			actual_num_scopes = len(st_stack.stack)
			declared = False
			while(actual_num_scopes > 0):
				if st_stack.stack[actual_num_scopes - 1].contains(name, actual_num_scopes):
					declared = True
				actual_num_scopes = actual_num_scopes - 1
			if not declared:
				error_st.append(("nodec", name, lin_dec, col_dec))

	# Tipos AST de asignacion de variables y evaluacion de expresiones
	# Realiza la funcion correspondiente al tipo de nodo (AST.type)

	# Recorre los hijos del nodo actual
	if AST.children:
		for child in AST.children:
			build_symbol_table(child)

	# Si es un nodo FOR, cierra el Scope al salir
	if AST.type == "for_stmt":
		pop_stack_to_st()


def build_symbol_table(AST):
	build_symbol_table_REC(AST)
	if len(error_st) == 0: return strrep_st
	else: return None

def getvar_list(AST):
	var_string = getvars(AST)
	var_aux = var_string.split("+")
	var_list = []
	for elem in var_aux:
		toappend = elem.split(",")
		if len(toappend) == 3:
			toappend[1] = int(toappend[1])
			toappend[2] = int(toappend[2])
			var_list.append(toappend)
	return var_list

def getvars(AST):
	if AST.val == "variable":
		return AST.children[0].val + "," + str(AST.children[0].lineno) + "," + str(AST.children[0].colno)
	elif AST.val == "int" or AST.val == "constant":
		return ""
	elif AST.val == "value":
		return getvars(AST.children[0])
	elif AST.val == "set":
		toreturn = ""
		for child in AST.children:
			print("Si no te gusta como pienso mamame el guevo " + child.val)
			toreturn = toreturn + "+" + getvars(child)
		return toreturn
	else:
		uno = getvars(AST.children[0])
		dos = getvars(AST.children[1])
		if dos == "":
			return uno
		else:
			return getvars(AST.children[0]) + "+" + getvars(AST.children[1])

def pop_stack_to_st():
	global strrep_st
	global indent_level
	st = st_stack.pop()
	for key in st.var_list():
		value = st.lookup(key[0], key[1])
		symbol_table_final.insert(key[0], key[1], value[0], value[1], value[2])
	if indent_level >= 1: indent_level -= 1
	strrep_st = strrep_st + "\t"*indent_level + "END_SCOPE" + "\n"


def get_errors():
	global error_st
	return error_st


def tostring_symbol_table():
	#return str(st_stack)
	#return str(symbol_table_final.st)
	pass