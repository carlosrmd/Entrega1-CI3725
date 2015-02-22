# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Tercera entrega del proyecto.             #
#   TypeChecker para el lenguaje Setlan       #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

from sl_symtab import SymTab, ST_Stack

# Tipos de Errores detectados en esta etapa:

# "redec": Redeclaracion de variable en el mismo alcance
# "nodec": Uso de variable no declarada
# "inv_tex": Tipo de expresion invalido
# "inv_opr": Operacion o tipo de operandos invalidos
# "read_ol": Asignacion a una variable read_only (de un FOR)

error_st = []
num_scopes = 0
st_stack = ST_Stack()
symbol_table_final = SymTab()

def build_symbol_table(AST):
	global st_stack
	global num_scopes

	# Inicializacion de los parametros de la entrada a la tabla de simbolos
	name = ""
	def_scope = 0
	type = ""
	val = ""
	lin_dec = 0

	# Tipos AST de declaracion de variables, apertura y cierre de Scopes
	# Realiza la funcion correspondiente al tipo de nodo (AST.type)
	if AST.type == "block": 
		num_scopes += 1

	elif AST.type == "using":
		st = SymTab()
		st_stack.push(st)

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

		if not st_stack.top().insert(name, dec_scope, type, val, lin_dec):
			error_st.append(("redec", name))

	elif AST.type == "for_stmt":
		num_scopes += 1
		st = SymTab()
		st_stack.push(st)

		name = str(AST.children[0].children[0].val)
		dec_scope = num_scopes
		type = "int"
		val = "0"
		lin_dec = AST.lineno

		st_stack.top().insert(name, dec_scope, type, val, lin_dec)

	elif AST.type == "block_end":
		pop_stack_to_st()

	# Tipos AST de asignacion de variables y evaluacion de expresiones
	# Realiza la funcion correspondiente al tipo de nodo (AST.type)
	

	# Recorre los hijos del nodo actual
	if AST.children:
		for child in AST.children:
			build_symbol_table(child)

	# Si es un nodo FOR, cierra el Scope al salir
	if AST.type == "for_stmt":
		pop_stack_to_st()


def pop_stack_to_st():
	st = st_stack.pop()
	for key in st.var_list():
		value = st.lookup(key[0], key[1])
		symbol_table_final.insert(key[0], key[1], value[0], value[1], value[2])


def tostring_symbol_table():
	#return str(st_stack)
	return str(symbol_table_final.st)