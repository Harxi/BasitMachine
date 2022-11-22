# Copyright (c) 2022-2023 Harxi

from lark import Lark, Transformer, Token

class ToJson(Transformer):
	def string(self, s):
		(s,) = s
		return {'type': 'str', 'value': s[1:-1]}

	def integer(self, n):
		(n,) = n
		return {'type': 'int', 'value': int(n)}
	
	def function(self, f):
		return {'type': 'function', 'name': f[0].value, 'value': f[1:len(f)]}
		
	def register(self, r):
		(r,) = r
		return {'type': 'reg', 'value': r.value}
	
	def address(self, r):
		(r,) = r
		return {'type': 'adrs', 'value': r}
		
	def section(self, f):
		return {'type': 'section', 'name': f[0].value, 'value': f[1:len(f)]}

	def block(self, d):
		return d
	
	def point(self, f):
		return {'type': 'point', 'name': f[0].value, 'value': f[1]}
				
grammar = Lark(r"""
    start: instruction*
    ?instruction: function | point | section
    register: /[a-z]+/
    string: ESCAPED_STRING
    integer: SIGNED_NUMBER
    address: "#"(register | integer)
    section: /[a-zA-Z]+/ "=" (string | integer | register) ":" (string | integer | register)
    ?types: (string | integer | register | address)
    function: /[a-z]+/ (types ("," types)*)
    block: ( instruction* )
    point: /[a-z]+/ "{" block "}"
    COMMENT: ";" /[^\n]/*

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    
    %ignore COMMENT
    %ignore WS
""", start='start')

def analyse(text):
	return ToJson().transform(grammar.parse(text)).children
