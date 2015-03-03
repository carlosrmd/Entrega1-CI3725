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
scopes_stack = []

def interpreter_traverser(AST):
	global error_intr
	global num_scopes
	global indent_level
	global scopes_stack
	if AST.type == "block":
		num_scopes += 1
		indent_level += 1
		scopes_stack.append(num_scopes)

	elif AST.type == "for_stmt":
		num_scopes += 1
		scopes_stack.append(num_scopes)

	elif AST.type == "block_end":
		indent_level -= 1
		scopes_stack.pop()

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
			else:
				act_value = evaluate(elem)
				act_string = str(act_value)
				if act_string[:3] == "set":
					act_string = "{"
					for elem in act_value:
						act_string += str(elem) + ","
					if act_string == "{":
						act_string = "{}"
					else:
						act_string = act_string[:-1] + "}"
				string += act_string
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


	elif AST.type == "assign":
		assign_var = AST.children[0].children[0].val
		assign_var_type = SymTab.typeof(assign_var, num_scopes)
		expr = AST.children[1].children[0]
		expr_val = evaluate(expr)
		for scope in scopes_stack:
			if SymTab.contains(assign_var, scope):
				act_scope = scope
		if assign_var_type == "int":
			SymTab.update(assign_var, act_scope, assign_var_type, expr_val, SymTab.lin_decof(assign_var, num_scopes))
		elif assign_var_type == "bool":
			if expr_val:
				SymTab.update(assign_var, act_scope, assign_var_type, "true", SymTab.lin_decof(assign_var, num_scopes))
			else:
				SymTab.update(assign_var, act_scope, assign_var_type, "false", SymTab.lin_decof(assign_var, num_scopes))
		elif assign_var_type == "set":
			strto_assign = "{"
			for elem in expr_val:
				strto_assign += str(elem) + ","
			if strto_assign == "{":
				SymTab.update(assign_var, act_scope, assign_var_type, "{}", SymTab.lin_decof(assign_var, num_scopes))
			else:
				SymTab.update(assign_var, act_scope, assign_var_type, strto_assign[:-1]+"}", SymTab.lin_decof(assign_var, num_scopes))

	elif AST.type == "if_stmt":
		if_expr = AST.children[0].children[0]
		if evaluate(if_expr):
			interpreter_traverser(AST.children[1])
		return

	elif AST.type == "while_stmt":
		pass


	# Recorre los hijos del nodo actual
	if AST.children:
		for child in AST.children:
			ch = interpreter_traverser(child)
			if ch == False:
				return False

	if AST.type == "for_stmt":
		scopes_stack.pop()


def execute(AST, ST):
	global SymTab
	SymTab = ST
	inter = interpreter_traverser(AST)

	if inter == None:
		return True
	else:
		return False


def evaluate(expr):
	# Casos base
	if expr.type == "int_stmt" or expr.type == "set_stmt":
		if expr.type == "set_stmt":
			actual_set = []
			for child in expr.children:
				actual_set.append(int(evaluate(child)))
			return set(actual_set)
		else:
			return expr.children[0].val
	if expr.type == "const_stmt":
		return expr.children[0].val == "true"
	if expr.type == "var_stmt":
		for scope in scopes_stack:
			if SymTab.contains(expr.children[0].val, scope):
				act_scope = scope
		vartype = SymTab.typeof(expr.children[0].val, act_scope)
		if vartype == "int":
			return SymTab.valof(expr.children[0].val, act_scope)
		elif vartype == "bool":
			return SymTab.valof(expr.children[0].val, act_scope) == "true"
		elif vartype == "set":
			actual_set = SymTab.valof(expr.children[0].val, act_scope)
			if actual_set == "{}":
				return set([])
			else:
				actual_set = actual_set[1:-1].split(",")
				for i in range(len(actual_set)):
					actual_set[i] = int(actual_set[i])
				return set(actual_set)

	# Operadores de enteros
	if expr.type == "expr_binopr":
		opr_a = int(evaluate(expr.children[0]))
		opr_b = int(evaluate(expr.children[1]))
		if expr.val.split()[1] == "+": return opr_a + opr_b
		if expr.val.split()[1] == "-": return opr_a - opr_b
		if expr.val.split()[1] == "*": return opr_a * opr_b
		if expr.val.split()[1] == "/":
			if opr_b == 0:
				error_intr.append(("div_by_zero", 0, expr.lineno, expr.colno))
			else:
				return opr_a / opr_b

	if expr.type == "expr_cmpopr":
		opr_a = int(evaluate(expr.children[0]))
		opr_b = int(evaluate(expr.children[1]))
		if expr.val.split()[1] == ">": return opr_a > opr_b
		if expr.val.split()[1] == "<": return opr_a < opr_b
		if expr.val.split()[1] == ">=": return opr_a >= opr_b
		if expr.val.split()[1] == "<=": return opr_a <= opr_b

	if expr.type == "negate_stmt":
		opr_a = int(evaluate(expr.children[0]))
		return -opr_a

	# Operadores de booleanos

	if expr.type == "bool_binopr":
		opr_a = evaluate(expr.children[0])
		opr_b = evaluate(expr.children[1])
		if expr.val.split()[1] == "or": return opr_a or opr_b
		if expr.val.split()[1] == "and": return opr_a and opr_b

	if expr.type == "not_stmt":
		opr_a = evaluate(expr.children[0])
		return not opr_a

	# Operadores de conjuntos

	if expr.type == "expr_setcont":
		opr_a = int(evaluate(expr.children[0]))
		opr_b = evaluate(expr.children[1])
		return opr_a in opr_b

	if expr.type == "set_binopr":
		opr_a = evaluate(expr.children[0])
		opr_b = evaluate(expr.children[1])
		if expr.val.split()[1] == "++":
			for elem in opr_b:
				opr_a.add(elem)
			return opr_a
		elif expr.val.split()[1] == "><":
			new_set = set([])
			for elem in opr_a:
				if elem in opr_b:
					new_set.add(elem)
			return new_set
		elif expr.val.split()[1] == "\\":
			new_set = set([])
			for elem in opr_a:
				if not elem in opr_b:
					new_set.add(elem)
			return new_set

	if expr.type == "set_mapopr":
		opr_a = int(evaluate(expr.children[0]))
		opr_b = evaluate(expr.children[1])
		if expr.val.split()[1] == "<+>":
			new_set = set([])
			for elem in opr_b:
				new_set.add(opr_a + elem)
			return new_set
		elif expr.val.split()[1] == "<->":
			new_set = set([])
			for elem in opr_b:
				new_set.add(opr_a - elem)
			return new_set
		elif expr.val.split()[1] == "<*>":
			new_set = set([])
			for elem in opr_b:
				new_set.add(opr_a * elem)
			return new_set
		elif expr.val.split()[1] == "</>":
			new_set = set([])
			for elem in opr_b:
				new_set.add(opr_a / elem)
			return new_set
		elif expr.val.split()[1] == "<%>":
			new_set = set([])
			for elem in opr_b:
				new_set.add(opr_a % elem)
			return new_set

	if expr.type == "set_unropr":
		opr_a = evaluate(expr.children[0])
		if expr.val.split()[1] == ">?" and len(opr_a) > 0: return max(opr_a)
		if expr.val.split()[1] == "<?" and len(opr_a) > 0: return min(opr_a)
		if expr.val.split()[1] == "$?" and len(opr_a) > 0: return len(opr_a)
		error_intr.append(("inv_empty_set", expr.val.split()[1], expr.lineno, expr.colno))



def get_errors():
	global error_intr
	return error_intr