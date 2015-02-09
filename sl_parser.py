# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Primera entrega del proyecto.             #
#   Lexer para el lenguaje Setlan             #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

import ply.yacc as yacc
from sl_lexer import tokens

# Variable global error_par

error_par = []

# Definicion de la clase Nodo utilizada para la construccion del AST

class Node:
	def __init__(self, type, children=None, val=None):
		self.type = type
		if children: 
			self.children = children
		else:
			self.children = []
		self.val = val

	def __str__(self):
		return str(self.val)

# PARSER

# Precedencia entre operadores, de menor a mayor

precedence = (
	# Operadores sobre bool
	('left', 'OR'),
	('left', 'AND'),
	('right', 'NOT'),

	# Operadores comparativos
	('nonassoc', 'LESSTHAN', 'GREATERTHAN', 'LTOREQUAL', 'GTOREQUAL'),
	('nonassoc', 'EQUAL', 'NOTEQUAL'),

	# Operadores aritmeticos
	('left', 'PLUS', 'MINUS'),
	('left', 'ASTERISK', 'INTDIV', 'PERCENT'),
	('right', 'UMINUS'),

	# Operadores sobre conjuntos
	('left', 'UNION', 'COMPLEMENT'),
	('left', 'INTERSERCTION'),

	# Operadores entre conjuntos-aritmeticas
	('nonassoc', 'SETSUM', 'SETSUBSTRACT'),
	('nonassoc', 'SETMULT', 'SETDIV', 'SETMOD'),
	('nonassoc', 'ARROBA'),

	# Operadores unarios sobre conjuntos
	('nonassoc', 'SETMAX', 'SETMIN', 'SETLENGTH'),
)

# Reglas de la gramatica

def p_program(p):
	'''program : PROGRAM one_line
			   | PROGRAM LCURLY start R_CURLY'''
	if len(p) == 3:
		p[0] = Node("program", [p[2]], "PROGRAM")
	else:
		p[0] = Node("program", [p[3], Node("block_end", None, "BLOCK_END")], "PROGRAM")

def p_empty(p):
	'empty :'
	pass

def p_one_line(p):
	'one_line : print'
	p[0] = p[1]

def p_start(p):
	'''start : using block
			 | empty'''
	if len(p) == 3:
		p[0] = Node("block", [p[1], Node("in", None, "IN")] + p[2], "BLOCK")

def p_block(p):
	'''block : assign block
			 | scan block
			 | condition block
			 | loop block
			 | print block
			 | empty'''
	if len(p) == 3:
		p[0] = [p[1]]+p[2]

def p_using(p):
	'''using : USING vardec IN'''
	p[0] = Node("using", p[2], "USING")

def p_vardec(p):
	'''vardec : type var_list SEMICOLON
			  | vardec type var_list SEMICOLON'''
	p[0] = []
	for var in p[2]:
		p[0] = p[0] + [Node("vardec", None, str(p[1]) + " " + str(var))]
	if len(p) == 5:
		p[0] = p[1] + p[0]

def p_type(p):
	'''type : INT
			| BOOL
			| SET'''
	p[0] = p[1]

def p_var_list(p):
	'''var_list : IDENTIFIER
				| var_list COMMA IDENTIFIER'''
	p[0] = [p[1]]
	if len(p) == 4:
		p[0] = p[1] + p[0]

def p_print(p):
	'''print : PRINT elements SEMICOLON
			 | PRINTLN elements SEMICOLON'''
	p[0] = Node("print", [p[2]], "PRINT")

def p_elements(p):
	'''elements : expr
				| setexpr
				| boolexpr
				| STRING
				| elements COMMA elements'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = [p[1]] + [p[3]]

def p_expr_simple(p):
	'''expr : INTEGER
			| IDENTIFIER
			| LPAREN expr RPAREN
			| MINUS expr %prec UMINUS'''
	if len(p) == 2: p[0] = p[1]
	elif p[1] == '-': p[0] = -p[2]
	else: p[0] = p[2]

def p_expr_binopr(p):
	'''expr : expr PLUS expr
			| expr MINUS expr
			| expr ASTERISK expr
			| expr INTDIV expr
			| expr PERCENT expr'''
	if p[2] == '+': p[0] = p[1] + p[3]
	elif p[2] == '-': p[0] = p[1] - p[3]
	elif p[2] == '*': p[0] = p[1] * p[3]
	elif p[2] == '/': p[0] = p[1] / p[3]
	elif p[2] == '%': p[0] = p[1] % p[3]

def p_set(p):
	'''set : LCURLY setelem RCURLY
		   | IDENTIFIER'''
	if len(p) == 2: p[0] = p[1]
	else: p[0] = p[2]

def p_setelem(p):
	'''setelem : expr
			   | setelem COMMA expr'''
	if len(p) == 2: p[0] = p[1]
	else: 
		if p[3] not in [1]: p[0] = p[1], p[3]
		else: p[0] = p[1]

def p_setexpr_binopr(p):
	'''setexpr : set
			   | setexpr UNION set
			   | setexpr INTERSECTION set
			   | setexpr COMPLEMENT set'''
	if len(p) == 2: p[0] = p[1]
	#elif p[2] == '++': p

def p_error(p):
	print("Error de sintaxis: Token '" + str(p.value) + "' inesperado en línea " + str(p.lineno) + ", columna " + str("."))

def build_parser():
	parser = yacc.yacc()
	return parser