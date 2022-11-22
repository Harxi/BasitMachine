# Copyright (c) 2022-2023 Harxi

import os

class HexTable():
	def __init__(self, file):
		self.file = file
		self.hex = []

	def newline(self):
		for _ in range(16):
			self.hex.append(0)

	def newbyte(self):
		self.hex.append(0)
		
	def edit(self, x: int, value: int):
		self.hex[x] = value
		
	def insert(self, value: str, exist: bool = True):
		if not exist:
			for _ in range(len(value)):
				self.newbyte()
			
		for ind, char in enumerate(value):
			self.edit(ind, ord(char))
			
	def get(self):
		with open(self.file, "r") as f:
			self.insert(f.read(), False)
			
	def dump(self):
		hex = ""
		with open(self.file, "w") as f:
			for ind, digit in enumerate(self.hex):
				hex += f"{chr(digit)}"
			f.write(hex)

class BFSInitialize:
	def __init__(self, disks: dict):
		self.disks = disks
		if len(disks["mainDisk"][0]) > 1 or len(disks["basitDisk"][0]) > 1:
			print("Ерор размеров названия")
			exit(-1)
		if ".BFS" in os.listdir(): os.chdir(".BFS")
		else:
			os.mkdir(".BFS")
			os.chdir(".BFS")
		if disks["mainDisk"][0] not in os.listdir(): os.mkdir(disks["mainDisk"][0])
		if disks["basitDisk"][0] not in os.listdir(): os.mkdir(disks["basitDisk"][0])
		os.chdir(f'{disks["basitDisk"][0]}')
		if 'basib' not in os.listdir(): os.mkdir('basib')
		os.chdir("..")
		self.root = os.getcwd()
		self.curdir = self.root
		self.disk = "~"
		self.file = None
		self.sizeMain = os.stat(disks["mainDisk"][0]).st_size
		self.sizeBasit = os.stat(disks["basitDisk"][0]).st_size
		self.checkSize()
		
	def checkSize(self):
		lastdir = os.getcwd()
		os.chdir(self.root)
		for path in os.scandir(self.disks["mainDisk"][0]): self.sizeMain += os.stat(path).st_size
		for path in os.scandir(self.disks["basitDisk"][0]): self.sizeBasit += os.stat(path).st_size
		if self.sizeMain > self.disks["mainDisk"][1]:
			print("DiskOverflow")
			exit(-1)
		if self.sizeBasit > self.disks["basitDisk"][1]:
			print("DiskOverflow")
			exit(-1)
		self.sizeRoot = self.sizeBasit + self.sizeMain
		os.chdir(self.curdir)
		
	def mkdir(self, name):
		try:
			if os.getcwd() == self.root:
				self.disk = "~"
				print("Permission denied")
			else:
				os.mkdir(name)
		except: pass
		self.checkSize()
	
	def getfile(self, name):
		if os.getcwd() == self.root:
			self.disk = "~"
			print("Permission denied")
		else:
			# name.split("/")[len(name.split("/"))-1]
			self.file = HexTable(name)
		
	def mkfile(self, name):
		if os.getcwd() == self.root:
			self.disk = "~"
			print("Permission denied")
		else:
			if name in os.listdir():
				pass
			else:
				self.file.dump()
		self.checkSize()
	
	def cd(self, path):
		if os.getcwd() == self.root:
			self.disk = "~"
			print("Permission denied")
		else:
			for name in path.split("/"):
				os.chdir(name)
				self.curdir = os.getcwd()
				if os.getcwd() == self.root:
					self.disk = "~"
					print("Permission denied")
					break
	
	def chdisk(self, name: str):
		if name == "~":
			os.chdir(f"{self.root}")
		else:
			if name == "":
				os.chdir(f"{self.root}")
				self.disk = "~"
			elif name in (self.disks["mainDisk"][0], self.disks["basitDisk"][0]):
				os.chdir(f"{self.root}/{name}")
				self.disk = name
			else:
				print("DiskNotFound")
		self.curdir = os.getcwd()
