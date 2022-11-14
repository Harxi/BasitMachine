# Copyright (c) 2022-2023 Harxi

class Ram:
	def __init__(self, size: int, bits):
		self.size = size
		self.bits = bits
		self.memory = {}
	
	def create(self) -> None:
		for address in range(self.size):
			self.memory[address] = {"size": self.bits, "value": 0} 
