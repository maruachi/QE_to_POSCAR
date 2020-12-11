###Written by Donggyu
###This program has a function to shake atomic position in QE input
###The length units is unified as angstrom

import re
import sys
import numpy as np

filename	=	sys.argv[1]

class atomic_structure:
	def __init__(self):
		self.num_atom	=	0
		self.atomic_positions	=	np.zeros(3)
		self.cell_parameters	=	np.zeros([3, 3])
		self.atomic_kinds		=	[]

		self.ordered_atomic_tag	=	[]
		self.ordered_counts		=	[]

	def count_atoms(self):
		atomic_kinds		=	self.atomic_kinds
		ordered_atomic_tag	=	[]
		ordered_counts		=	[]
		
		order_tag = 0
		count = 0
		ordered_atomic_tag.append(atomic_kinds[0])
		for atomic_kind in atomic_kinds:
			if ordered_atomic_tag[order_tag] == atomic_kind:
				count += 1
			if ordered_atomic_tag[order_tag] != atomic_kind:
				ordered_atomic_tag.append(atomic_kind)
				order_tag += 1
				ordered_counts.append(count)
				count = 1
		ordered_counts.append(count)
				
		self.ordered_atomic_tag	=	ordered_atomic_tag
		self.ordered_counts		=	ordered_counts

def read_atomic_structure(filename):
	num_atom		=	0
	num_line		=	0
	cell_dimension	=	0.
	match_item		=	[]
	cell_parameters	=	np.array([])
	atomic_positions=	np.array([])
	atomic_kinds	=	[]

	number_format			=	re.compile("[+-]?[0-9]+.[0-9]+")
	atom_species_format		=	re.compile("[A-Za-z]+")

	with open(filename, 'r') as f:
		for line in f:
			if "CELL_PARAMETERS" in line:
				num_line	=	3
				list_cell_parameters	=	[]

				for _ in range(num_line):
					sub_line	=	f.readline()
					match_item	=	number_format.findall(sub_line)
					match_item	=	[float(item) for item in match_item]
					list_cell_parameters.append(match_item)
				cell_parameters	=	np.array(list_cell_parameters)

			if "ATOMIC_POSITIONS" in line:
				list_atomic_positions	=	[]
				atomic_kind =	''

				while(True):
					sub_line	=	f.readline()
					if sub_line == '' :
						break
					num_atom += 1
					match_item	=	number_format.findall(sub_line)
					match_item	=	[float(item) for item in match_item]
					list_atomic_positions.append(match_item)
					match_item	=	atom_species_format.match(sub_line)
					atomic_kind =	match_item.group()
					atomic_kinds.append(atomic_kind)
				atomic_positions	=	np.array(list_atomic_positions)

	atomic_structure0					=	atomic_structure()
	atomic_structure0.num_atom			=	num_atom
	atomic_structure0.atomic_positions	=	atomic_positions
	atomic_structure0.cell_parameters	=	cell_parameters
	atomic_structure0.atomic_kinds		=	atomic_kinds
	
	return atomic_structure0

def write_POSCAR(atomic_structure0):
	cell_parameters		=	atomic_structure0.cell_parameters
	atomic_positions	=	atomic_structure0.atomic_positions
	ordered_atomic_tag	=	atomic_structure0.ordered_atomic_tag
	ordered_counts		=	atomic_structure0.ordered_counts

	print("POSCAR")
	print("1.0000000")
	for cell_parameter in cell_parameters:
		for component in cell_parameter:
			print("{:13.7f}".format(component), end = '')
		print()
	for atomic_tag in ordered_atomic_tag:
		print("{} ".format(atomic_tag), end = '')
	print()
	for count in ordered_counts:
		print("{:d} ".format(count), end = '')
	print()
	print("Direct")
	for atomic_position in atomic_positions:
		for component in atomic_position:
			print("{:13.7f}".format(component), end = '')
		print()

atomic_structure	=	read_atomic_structure(filename)
atomic_structure.count_atoms()
write_POSCAR(atomic_structure)
