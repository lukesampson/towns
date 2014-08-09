import lex

class Parser:
	def __init__(self):
		self.input = []
		self.pos = 0
		self.items = []

	def next(self):
		if self.pos >= len(self.input):
			return None

		n = self.input[self.pos]
		self.pos += 1
		return n

	def backup(self):
		self.pos -= 1

	def peek(self):
		n = self.next()
		self.backup()
		return n

def parse_token(t, p):
	type = t[0]
	if type == 'text':
		p.items.append(parse_text(t))
	elif type == 'left_tmpl':
		p.items.append(parse_tmpl(p))

def parse_text(t):
	return t

def parse_tmpl(p):
	name = ''
	params = []

	tok = p.next()
	while tok:
		if tok[0] == 'param':
			if not name:
				name = tok[1].strip() # first param is name
			else:
				params.append(tok[1]) # subsequent params (don't strip yet)
		elif tok[0] == 'param_delim':
			pass
		elif tok[0] == 'right_tmpl':
			break
		elif tok[0] == 'left_tmpl':
			p.backup()
			if len(params) == 0:
				params.append('') # ensure at least one param
			params[-1] += serialize_tmpl(p) # add to last param
		else:
			raise Exception("unexpected token type {} at position {}: {}".format(tok[0], p.pos, tok[1]))

		tok = p.next()

	return ('template', name, param_data(params))

def param_data(params):
	data = {}
	for param in params:
		clean = param.strip()
		if clean == '': continue
		eq = clean.find('=')
		if eq > -1:
			name = clean[:eq].strip()
			val = clean[eq+1:].strip()
			data[name] = val
		else:
			data[clean] = None

	return data

# for nested templates, just serialize them back to text
def serialize_tmpl(p):
	tok = p.next()
	nest_level = 1
	str = ''
	while tok:
		str += tok[1]
		if tok[0] == 'left_tmpl':
			nest_level += 1
		elif tok[0] == 'right_tmpl':
			nest_level -= 1
			if nest_level == 1: break

		tok = p.next()

	return str


def parse(input):
	parser = Parser()
	parser.input = lex.lex(input)

	tok = parser.next()
	while tok:
		parse_token(tok, parser)
		tok = parser.next()

	return parser.items