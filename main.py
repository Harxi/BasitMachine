import processor
import ram
import bmasm
import BFS
import config

code = """
mov oth, 1
""" # ТУТ ТВОЙ КОД ДЛЯ АССЕМБЛЕРА



bfs = BFS.BFSInitialize(config.cfg["bfs"])
ram = ram.Ram(config.cfg["ram"]["size"], config.cfg["ram"]["bits"])
registers = processor.Registers()
stack = processor.Stack(registers)
ram.create()
functions = processor.Interrupts(bfs, ram, registers, stack)

processor.bas1x(functions, bmasm.analyse(code))