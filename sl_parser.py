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

error = []


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

def p_program(p):
	'''program : PROGRAM line
			   | PROGRAM LCURLY start R_CURLY'''
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = p[3]

def p_empty(p):
	'empty :'
	pass

def p_line(p):
	'line : print'
	p[0] = p[1]

def p_start(p):
	'''start : print start
			 | using block
			 | empty'''
	p[0] = p[1]

def p_block(p):
	'''block : assign block
			 | scan block
			 | condition block
			 | loop block
			 | print block
			 | empty'''
	p[0] = p[1]

def p_print(p):
	'''print : PRINT elements SEMICOLON
			 | PRINTLN elements SEMICOLON'''
	p[0] = p[2]

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

def p_error(p):
	print("Error de sintaxis: Token '" + str(p.value) + "' inesperado en línea " + str(p.lineno) + ", columna " + str(".")