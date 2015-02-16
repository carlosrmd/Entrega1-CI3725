# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Tercera entrega del proyecto.             #
#   TypeChecker para el lenguaje Setlan       #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

from sl_symtab import SymTab

# Tipos de Errores detectados en esta etapa:

# "redec": Redeclaracion de variable en el mismo alcance
# "nodec": Uso de variable no declarada
# "inv_tex": Tipo de expresion invalido
# "inv_opr": Operacion o tipo de operandos invalidos

error_st = []
symbol_table = SymTab()
num_scopes = 0

def build_symbol_table(AST):
	global symbol_table
	global num_scopes

	if AST.type == "block": num_scopes += 1
	elif AST.type == "vardec":
		vardec = str(AST.val)
		type = vardec.split()[0]
		var = vardec.split()[1]

		name = str(var)
		dec_scope = num_scopes
		if type == "int": val = "0"
		elif type == "set": val = "{}"
		elif type == "bool": val = "false"
		vis_scope = [num_scopes]

		if not symbol_table.insert(name, dec_scope, type, val, vis_scope):
			error_st.append(("redec", name))

	if AST.children:
		for child in AST.children:
			build_symbol_table(child)

def tostring_symbol_table():
	return str(symbol_table.st)