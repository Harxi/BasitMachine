import os

class BFSInitialize:
	def __init__(self, disks: dict):
		self.disks = disks
		if len(disks["mainDisk"][0]) > 1 or len(disks["basitDisk"][0]) > 1:
			print("Ерор размеров названия")
			exit(-1)
		try:
			os.mkdir(".BFS")
			os.chdir(".BFS")
		except:
			os.chdir(".BFS")
		try:
			os.mkdir(disks["mainDisk"][0])
			os.mkdir(disks["basitDisk"][0])
		except:
			pass
		self.root = os.getcwd()
		self.curdir = self.root
		self.disk = "~"
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
	
	def write(self, path, text):
		with open(path, "w") as f: f.write(text)
		self.checkSize()	
	
	def mkfile(self, name):
		if os.getcwd() == self.root:
			self.disk = "~"
			print("Permission denied")
		else:
			if name in os.listdir():
				pass
			else:
				open(name, "w").close()
		self.checkSize()
	
	def getFile(self, name):
		if os.getcwd() == self.root:
			self.disk = "~"
			print("Permission denied")
		else:
			with open(name, "r") as f:
				return f.read()
	
	def cd(self, index: int):
		if os.getcwd() == self.root:
			self.disk = "~"
			print("Permission denied")
		else:
			if index == -1:
				os.chdir("..")
			else:
				os.chdir(sorted(os.listdir())[index])
		self.curdir = os.getcwd()
	
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