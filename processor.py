# Copyright (c) 2022-2023 Harxi

from sys import stdout
import json
import zlib

import ram
import BFS
import config

bit = config.cfg["bits"]

# REGISTERS
class Flags:
	def __init__(self):
		self.eq  = 0
		self.lt = 0
		self.gt = 0

class Registers:
	def __init__(self):
		self.regs = [register for register in config.cfg["registers"]]
		self.chr = config.cfg["registers"]["chr"]
		self.ctr = config.cfg["registers"]["ctr"]
		self.ret = config.cfg["registers"]["ret"]
		self.p = config.cfg["registers"]["p"]
		self.sp = config.cfg["registers"]["sp"]
		self.oth = config.cfg["registers"]["oth"]
		self.flags = Flags()
		
	def check(self):
		for reg in self.regs:
			if eval(f"self.{reg}['value']") > 2**eval(f"self.{reg}['size']")-1:
				exec(f"self.{reg}['value'] = 2**self.{reg}['size']-1")
			elif eval(f"self.{reg}['value']") < (2**eval(f"self.{reg}['size']")-1)*-1:
				exec(f"self.{reg}['value'] = (2**self.{reg}['size']-1)*-1")
# REGITERS END

# STACK
class Stack:
	def __init__(self, registers: Registers):
		self.stack = []
		self.registers = registers
                 
	def push(self, element: int):
		if element > 2**bit-1: element = 2**bit-1
		if self.registers.sp["value"] > 2**self.registers.sp["size"]-1: self.registers.sp["value"] = 2**self.registers.sp["size"]-1
		self.registers.sp["value"] += 1
		if len(self.stack) > 2**bit-1:
			while len(self.stack) != 2**bit-1:
				self.stack.pop()
		self.stack.insert(self.registers.sp["value"], element)
                 
	def pop(self):
		if self.registers.sp["value"] == 0: return 0
		self.registers.sp["value"] -= 1
		return self.stack.pop()
# STACK END

# ITERRUPTS
class Interrupts:
	def __init__(self, bfs: BFS.BFSInitialize, ram: ram.Ram, registers: Registers, stack: Stack):
		self.bfs = bfs
		self.ram = ram
		self.registers = registers
		self.stack = stack
	
	def print(self):
		stdout.write(chr(self.registers.chr["value"]))
	
	def input(self):
		i = input()
		if i == "":
			self.stack.push(0)
		else:
			i = i[0:2**bit-1]
			for index in range(0, len(i)):
				if ord(i[index]) > 2**self.registers.chr["size"]-1: self.stack.push(2**self.registers.chr["size"]-1)
				else: self.stack.push(ord(i[index]))
	
	def invertStack(self):
		self.stack.stack = self.stack.stack[::-1]
	
	def BFSservices(self):
		function = self.stack.pop()
		if function == 1:
			self.bfs.chdisk(chr(self.stack.pop()))
				
		if function == 2:
			size = self.stack.pop()
			string = ""
			for char in range(0, size):
				string += chr(self.stack.pop())
			string = string[::-1]
			self.bfs.getfile(string)
			
		if function == 3:
			self.bfs.file.get()
			sizes = [self.stack.pop(), self.stack.pop()]
			for index in range(sizes[1], sizes[0]+1):
				if index == len(self.bfs.file.hex):
					break
				self.ram.memory[index]["value"] = self.bfs.file.hex[index]
		
		if function == 4:
			sizes = [self.stack.pop(), self.stack.pop()]
			self.bfs.file.hex = [self.ram.memory[value]["value"] for value in self.ram.memory][sizes[1]:sizes[0]]
			self.bfs.file.dump()
			
	
	
# INTERRUPTS END

# OTHER
points = {}
sections = {}
# OTHER END

# REPLACERS
def replaceRegister(interrupts, name: str):
	return {"type": "int", "value": eval(f'interrupts.registers.{name}')["value"]}

def replaceAddress(interrupts, name: str):
	return {"type": "int", "value": eval(f'interrupts.ram.memory[{name}]')}
# REPLACERS END

# BAS1X INSTRUCTIONS
class Bas1xInstructions:
	@staticmethod
	def move(interrupts, value):
		if len(value) < 2 or len(value) > 2:
			print("OperandError: many or few operands")
			exit(-1)
		else:
			if value[1]["type"] == "reg":
				if value[1]["value"] in interrupts.registers.regs: value[1] = replaceRegister(interrupts, value[1]["value"])
				else:
					print(f"RegisterError: Register '{value[1]['value']}' not found")
					exit(-1)
			elif value[1]["type"] == "adrs":
				temp1 = value[1]["value"]
				if value[1]["value"]["type"] == "reg":
					if value[1]["value"]["value"] in interrupts.registers.regs: temp1 = replaceRegister(interrupts, value[1]["value"]["value"])
					else:
						print(f"RegisterError: Register '{value[1]['value']['value']}' not found")
						exit(-1)
				if temp1["value"] < interrupts.ram.size: value[1] = replaceAddress(interrupts, temp1["value"])["value"]
				else:
					print(f"RegisterError: Register '{value[ind]['value']}' not found")
					exit(-1)
				#print(value)
			temp1 = value[1]
			
			if value[0]["type"] == "reg":
				if value[0]["value"] not in interrupts.registers.regs:
					print(f"RegisterError: Register '{value[0]['value']}' not found")
					exit(-1)
				exec('%s = %d'%(f'interrupts.registers.{value[0]["value"]}["value"]',value[1]["value"]))

			elif value[0]["type"] == "adrs":
				temp = value[0]["value"]
				if value[0]["value"]["type"] == "reg":
					if value[0]["value"]["value"] in interrupts.registers.regs:
						temp = replaceRegister(interrupts, value[0]["value"]["value"])
					else:
						print(f"RegisterError: Register '{value[0]['value']['value']}' not found")
						exit(-1)

				if temp["value"] < interrupts.ram.size:
					interrupts.ram.memory[temp["value"]] = {"size": interrupts.ram.memory[temp["value"]]["size"], "value": temp1["value"]}
				else:
					print(f"RegisterError: Register '{value[ind]['value']}' not found")
					exit(-1)
	
	@staticmethod
	def push(interrupts, value):
		for ind in range(len(value)):
			if value[ind]["type"] == "reg":
				if value[ind]["value"] in interrupts.registers.regs: value[ind] = replaceRegister(interrupts, value[ind]["value"])
				else:
					print(f"RegisterError: Register '{value[ind]['value']}' not found")
					exit(-1)
		for number in value:
			interrupts.stack.push(number["value"])
	@staticmethod
	def pop(interrupts, value):
		if len(value) > 1 or len(value) < 1:
			print("operandError: many operands")
			exit(-1)
		else:
			if value[0]["value"] == "void": interrupts.stack.pop()
			elif value[0]["value"] in interrupts.registers.regs: exec('%s = %d'%(f'interrupts.registers.{value[0]["value"]}["value"]',interrupts.stack.pop()))
			else:
				print(f"RegisterError: Register '{value[0]['value']}' not found")
				exit(-1)
	@staticmethod
	def goto(interrupts, value, tokens):
		if len(value) < 2 or len(value) > 2:
			print("OperandError: many or few operands")
			exit(-1)
		else:
			for ind in range(len(value)):
				if value[ind]["type"] == "reg":
					if value[ind]["value"] in interrupts.registers.regs: value[ind] = replaceRegister(interrupts, value[ind]["value"])
					else:
						print(f"RegisterError: Register '{value[ind]['value']}' not found")
						exit(-1)
			if tokens[value[0]["value"]]["name"] == "goto":
				print("GotoError: cannot call goto from goto")
				exit(-1)
			else:
				if value[1]["value"] < 0:
					while True:
						bas1x(interrupts, [tokens[value[0]["value"]]])
				else:
					bas1x(interrupts, [tokens[value[0]["value"]]]*value[1]["value"])
	@staticmethod
	def ret(interrupts, value):
		if len(value) > 1 or len(value) < 1:
			print("OperandError: many operands")
			exit(-1)
		else:
			if value[0]["type"] == "reg":
				if value[0]["value"] in interrupts.registers.regs: value[0] = replaceRegister(interrupts, value[0]["value"])
				else:
					print(f"RegisterError: Register '{value[0]['value']}' not found")
					exit(-1)
			interrupts.registers.ret["value"] = value[0]["value"]
	@staticmethod
	def cmp(interrupts, value):
		if len(value) > 2 or len(value) < 2:
			print("OperandError: many or few operands")
			exit(-1)
		else:
			for ind in range(len(value)):
				if value[ind]["type"] == "reg":
					if value[ind]["value"] in interrupts.registers.regs: value[ind] = replaceRegister(interrupts, value[ind]["value"])
					else:
						print(f"RegisterError: Register '{value[ind]['value']}' not found")
						exit(-1)
			if value[0]["value"] == value[1]["value"]:
				interrupts.registers.flags.eq = 1
				interrupts.registers.flags.gt = 0
				interrupts.registers.flags.lt = 0
			if value[0]["value"] != value[1]["value"]:
				interrupts.registers.flags.eq = 0
				interrupts.registers.flags.gt = 0
				interrupts.registers.flags.lt = 0
			if value[0]["value"] > value[1]["value"]:
				interrupts.registers.flags.eq = 0
				interrupts.registers.flags.gt = 1
				interrupts.registers.flags.lt = 0
			if value[0]["value"] < value[1]["value"]:
				interrupts.registers.flags.eq = 0
				interrupts.registers.flags.gt = 0
				interrupts.registers.flags.lt = 1
				
	@staticmethod
	def add(interrupts, value):
		if len(value) > 2 or len(value) < 2:
			print("OperandError: many or few operands")
			exit(-1)
		else:
			if value[1]["type"] == "reg":
				if value[1]["value"] in interrupts.registers.regs: value[1] = replaceRegister(interrupts, value[1]["value"])
				else:
					print(f"RegisterError: Register '{value[1]['value']}' not found")
					exit(-1)
			if value[0]["value"] in interrupts.registers.regs: exec('%s += %d'%(f'interrupts.registers.{value[0]["value"]}["value"]',value[1]["value"]))
			else:
				print(f"RegisterError: Register '{value[0]['value']}' not found")
				exit(-1)
				
	@staticmethod
	def jmp(interrupts, value):
		if len(value) > 1 or len(value) < 1:
			print("operandError: many operands")
			exit(-1)
		else:
			if value[0]["type"] == "reg":
				if value[0]["value"] in points:
					bas1x(interrupts, points[value[0]["value"]])
				else:
					print(f"PointError: Point '{value[0]['value']}' not found")
					exit(-1)
			else:
				print("OperandError: incorrect operand")
				exit(-1)
	@staticmethod
	def set(interrupts, value):
		if len(value) > 2 or len(value) < 2:
			print("OperandError: many or few operands")
			exit(-1)
		else:
			if value[1]["type"] == "reg":
				register = value[1]["value"]
				if value[1]["value"] in interrupts.registers.regs: value[1] = replaceRegister(interrupts, value[1]["value"])
				else:
					print(f"RegisterError: Register '{value[1]['value']}' not found")
					exit(-1)

			if value[0]["value"] not in ["eq","gt","lt"]:
				print(f"RegisterError: Flag '{value[0]['value']}' not found")
				exit(-1)
			if value[1]["value"] not in [0,1]:
				print("SizeError: Allowed only 1 and 0")
				exit(-1)
			exec('%s = %d'%(f'interrupts.registers.flags.{value[0]["value"]}',value[1]["value"]))
	@staticmethod
	def ext(interrupts, value):
		if len(value) > 1 or len(value) < 1:
			print("OperandError: many operands")
			exit(-1)
		else:
			if value[0]["type"] == "reg":
				if value[0]["value"] in sections:
					for value in sections[value[0]["value"]]:
						if value["type"] == "reg":
							if value["value"] in interrupts.registers.regs: value = replaceRegister(interrupts, value["value"])
							else:
								print(f"RegisterError: Register '{value['value']}' not found")
								exit(-1)
						interrupts.stack.push(value["value"])
				else:
					print(f"SectionError: Section '{value[0]['value']}' not found")
					exit(-1)
			else:
				print("OperandError: incorrect operand")
				exit(-1)
	@staticmethod
	def inc(interrupts, value):
		if len(value) > 1 or len(value) < 1:
			print("OperandError: many operands")
			exit(-1)
		else:
			if value[0]["type"] == "str":
				cdisk = interrupts.bfs.disk
				interrupts.bfs.chdisk(interrupts.bfs.disks["basitDisk"][0])
				interrupts.bfs.cd("basib")
				with open(value[0]["value"], "rb") as f:
					bas1x(interrupts, json.loads(zlib.decompress(f.read()).decode()))
			else:
				print("OperandError: incorrect operand")
				exit(-1)
	@staticmethod
	def interrupt(interrupts, value):
		if len(value) > 1 or len(value) < 1:
			print("OperandError: many operands")
			exit(-1)
		else:
			if value[0]["type"] == "reg":
				if value[0]["value"] in interrupts.registers.regs: value[0] = replaceRegister(interrupts, value[0]["value"])["value"]
				else:
					print(f"RegisterError: Register '{value[0]['value']}' not found")
					exit(-1)
			else: value[0] = value[0]["value"]
			if value[0] == 1:
				interrupts.print()
				
			if value[0] == 2:
				interrupts.input()
				
			if value[0] == 3:
				interrupts.invertStack()
			
			if value[0] == 4:
				interrupts.BFSservices()
				
# BAS1X INSTRUCTIONS END

# BAS1X EXECUTER
def bas1x(interrupts: Interrupts, tokens: list):
	for token in tokens:
		
		type = token["type"]
		name = token["name"]
		value = [v for v in token["value"]]
		length = 0
		for ind in range(len(value)):
			# PREPROCESSOR
			if name != "inc":
				if value[ind+length]["type"] == "str":
					text = value[ind+length]["value"]
					del value[ind+length]
					for char in text:
						if char == "":
							value.insert(ind+length, {"type": "int", "value": 0})
						else:
							if ord(char) > 2**interrupts.registers.chr["size"]-1:
								value.insert(ind+length, {"type": "int", "value": 2**interrupts.registers.chr["size"]-1})
							else:
								value.insert(ind+length, {"type": "int", "value": ord(char)})
					length += len(text)-1
			# PREPROCESSOR
		
		# CHECKERS
		if type == "function":
			if name == "inc":
				Bas1xInstructions.inc(interrupts, value)
			if name == "mov":
				Bas1xInstructions.move(interrupts, value)
			if name == "push":
				Bas1xInstructions.push(interrupts, value)
					
			if name == "pop":
				Bas1xInstructions.pop(interrupts, value)
			if name == "goto":
				Bas1xInstructions.goto(interrupts, value, tokens)
			if name == "ret":
				Bas1xInstructions.ret(interrupts, value)
			if name == "cmp":
				Bas1xInstructions.cmp(interrupts, value)
			if name == "add":
				Bas1xInstructions.add(interrupts, value)
			if name == "jmp":
				Bas1xInstructions.jmp(interrupts, value)
			if name == "jeq":
				if interrupts.registers.flags.eq:
					Bas1xInstructions.jmp(interrupts, value)

			if name == "jneq":
				if not interrupts.registers.flags.eq:
					Bas1xInstructions.jmp(interrupts, value)
			if name == "jgt":
				if interrupts.registers.flags.gt:
					Bas1xInstructions.jmp(interrupts, value)
			if name == "jlt":
				if interrupts.registers.flags.lt:
					Bas1xInstructions.jmp(interrupts, value)
			if name == "set":
				Bas1xInstructions.set(interrupts, value)
			if name == "ext":
				Bas1xInstructions.ext(interrupts, value)
			if name == "int":
				Bas1xInstructions.interrupt(interrupts, value)
			interrupts.registers.check()
		if type == "point":
			points[name] = value
		
		if type == "section":
			sections[name] = value
		
		# CHECKERS
# BAS1X EXECUTER END
