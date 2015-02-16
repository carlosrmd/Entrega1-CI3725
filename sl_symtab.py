# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Tercera entrega del proyecto.             #
#   Definicion de la Tabla de Simbolos        #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

class SymTab:
	
	def __init__(self):
		self.st = {}

	def insert(self, name, type, val, scope):
		if not self.contains(name, scope):
			self.st[(name, scope)] = (type, val)
			return True
		else:
			return False

	def delete(self, name, type, val, scope):
		if self.contains(name, scope) and self.st[(name, scope)] == (type, val):
			del self.st[(name, scope)]
			return True
		else:
			return False

	def update(self, name, type, val, scope):
		if self.contains(name, scope):
			self.st[(name, scope)] = (type, val)
			return True
		else:
			return False

	def contains(self, name, scope):
		return (name, scope) in self.st.keys()

	def lookup(self, name, scope):
		if self.contains(name, scope):
			return self.st[(name, scope)]
		else:
			return False

	def typeof(self, name, scope):
		if self.contains(name, scope):
			return self.st[(name, scope)][0]
		else:
			return False

	def valof(self, name, scope):
		if self.contains(name, scope):
			return self.st[(name, scope)][1]
		else:
			return False

	def var_str(self, name, scope):
		if self.contains(name, scope):
			type = self.typeof(name, scope)
			val = self.valof(name, scope)
			return "Variable: " + name + "\t| Type: " + type + "\t| Value: " + str(val)
		else:
			return False