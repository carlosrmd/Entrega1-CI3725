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
# "inv_assign" Asignación inválida
# "inv_neg" Negación inválida
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
		print(st_stack)

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


	# Tipos AST de asignacion de variables y evaluacion de expresiones
	# Realiza la funcion correspondiente al tipo de nodo (AST.type)
	elif AST.type == "assign":
		var_list = getvar_list(AST)
		for var in var_list:
			name = var[0]
			lin_dec = var[1]
			col_dec = var[2]
			actual_num_scopes = len(st_stack.stack)
			declared = False
			no_errors = True
			while(actual_num_scopes > 0):
				if st_stack.stack[actual_num_scopes - 1].contains(name, actual_num_scopes):
					declared = True
				actual_num_scopes = actual_num_scopes - 1
			if not declared:
				no_errors = False
				error_st.append(("nodec", name, lin_dec, col_dec))
		if no_errors:
			varname = AST.children[0].children[0].val
			for i in range(num_scopes):
				if st_stack.stack[0].typeof(varname, i+1):
					to_assign_type = st_stack.stack[0].typeof(varname, i+1)
			print("Buey Almizclero " + to_assign_type)
			assign_value_type = gettype(AST.children[1].children[0])
			if assign_value_type != "error" and assign_value_type != to_assign_type:
				error_st.append(("inv_assign", "=" , AST.lineno, AST.colno, to_assign_type, assign_value_type))

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

def gettype(AST):

	if AST.val == "int" or AST.val == "set":
		print("Zarramagurdi " + AST.type)
		return AST.val
	if AST.val == "true" or AST.val == "false":
		return "bool"
	if AST.val == "constant":
		return gettype(AST.children[0])
	if AST.val == "variable":
		for i in range(num_scopes):
			if st_stack.stack[0].typeof(AST.children[0].val, i+1):
				to_assign_type = st_stack.stack[0].typeof(AST.children[0].val, i+1)
		return to_assign_type


	if AST.type == "expr_binopr":
		a = gettype(AST.children[0])
		b = gettype(AST.children[1])
		if a == b and a == "int":
			return a
		else:
			if a != "error" and b != "error": error_st.append(("inv_opr", AST.val[-1:] , AST.lineno, AST.colno, a, b))
			return "error"
	if AST.type == "expr_cmpopr":
		a = gettype(AST.children[0])
		b = gettype(AST.children[1])
		if a == b and a == "int":
			return "bool"
		else:
			opr = AST.val.split(" ")
			if a != "error" and b != "error": error_st.append(("inv_opr", opr[1] , AST.lineno, AST.colno, a, b))
			return "error"
	if AST.type == "expr_setcont":
		a = gettype(AST.children[0])
		b = gettype(AST.children[1])
		if a == "int" and b == "set":
			return "bool"
		else:
			if a != "error" and b != "error": error_st.append(("inv_opr", "@" , AST.lineno, AST.colno, a, b))
			return "error"

	if AST.type == "negate_stmt":
		a = gettype(AST.children[0])
		if a == "int": return "int"
		else:
			if a != "error": error_st.append(("inv_neg", "-" , AST.lineno, AST.colno, a))
			return "error"

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
			toreturn = toreturn + "+" + getvars(child)
		return toreturn
	else:
		print(AST.val)
		uno = getvars(AST.children[0])
		if len(AST.children) == 1:
			return uno
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


# PRUEBAS - QUITAR!
def tostring_symbol_table():
	#return str(st_stack)
	#return str(symbol_table_final.st)
	pass