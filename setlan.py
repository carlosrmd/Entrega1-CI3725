#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	TRADUCTORES E INTERPRETADORES CI3725
#	Primera entrega del proyecto
#	Autores: Carlos Martínez 	- 11-10584
#			 Christian Teixeira - 11-10584


import ply.lex as lex

tokens = (
		'PROGRAM',
		'OPENCURLY',
		'CLOSECURLY',
		'OPENPAREN',
		'CLOSEPAREN',
		'PRINT',
		'PRINTLN',
		'USING',
		'INT',
		'BOOL',
		'STRING'
		'IN',
		'SCAN',
		'ID',
		'COMMA',
		'SEMICOLON',
		'COLON',
		'EQUAL',
		'STRING',
		'PLUS',
		'MINUS',
		'IF',
		'ELSE',
		'TRUE',
		'OR',
		'AND',
		'NOT',
		'FALSE',
		'FOR',
		'REPEAT',
		'WHILE',
		'DO',
		'SET',
		'LESSTHAN',
		'GREATERTHAN',
		'LESSTHANOREQUAL',
		'GREATERTHANOREQUAL',
		'EQUALS',
		'NOTEQUALS',
		'ASTERISK',
		'DEF',
		'RETURN',
		'ARROW',
		'SLASH',
		'PERCENT',
		'ARROBA',
		'UNION',
		'INTERSECTION',
		'COMPLEMENT',
		'SETSUM',
		'SETREST',
		'SETSUBSTRACT',
		'SETMULT',
		'SETDIV',
		'SETMOD',
		'SETMAX',
		'SETMIN',
		'SETLENGTH',
		'NUMBER',
	)

reserved = {
	'program' : 'PROGRAM',
	'print' : 'PRINT',
	'println' : 'PRINTLN',
	'using' : 'USING',
	'int' : 'INT',
	'bool' : 'BOOL',
	'string' : 'STRING',
	'in' : 'IN',
	'scan' : 'SCAN',
	'if' : 'IF',
	'else' : 'ELSE',
	'true' : 'TRUE',
	'false' : 'FALSE',
	'or' : 'OR',
	'and' : 'AND',
	'not' : 'NOT',
	'for' : 'FOR',
	'repeat' : 'REPEAT',
	'while' : 'WHILE',
	'do' : 'DO',
	'set' : 'SET',
	'def' : 'DEF',
	'return' : 'RETURN',
}

t_OPENCURLY = r'\{'
t_CLOSECURLY = r'\}'
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
t_PLUS    = r'\+'
t_ignore  = ' \t'
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
def t_error(t):
	print("Illegal character '%s'" & t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()
lexer.input("1+1")
while True:
	tok = lexer.token()
	if not tok: break
	print(tok)