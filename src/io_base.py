import re
import numpy as np
from .atom import atom, cell, species_tag

bohr_to_angstrom = 0.529177

class read_relax_out_QE:
	def __init__(self, filename):
		self.filename = filename
		self.natm = 0
		self.lat_vecs = []
		self.atoms = []

		self.natm = self.read_system()
		self.lat_vecs = self.read_cell_parameters()
		self.atoms = self.read_atomic_positions()
		self.cell = cell(self.lat_vecs, self.atoms)
	
	def read_system(self):
		with open(self.filename, 'r') as f:
			for line in f:
				if "number of atoms/cell" in line:
					natm = re.search('[0-9]+', line).group()
					natm = int(natm)
		return natm
	
	def read_cell_parameters(self):
		with open(self.filename, 'r') as f:	
			for line in f:
				if "lattice parameter (alat)  =" in line:
					lat_par = re.search('[0-9]+\.[0-9]+', line).group()
					lat_par = float(lat_par)
				if "crystal axes" in line:
					lat_vecs = []
					for _ in range(3):
						tmp_line = f.readline()
						lat_vec = re.findall('[0-9]+\.[0-9]+', tmp_line)
						lat_vec = [float(item) for item in lat_vec]
						lat_vecs.append(lat_vec)
		lat_vecs = lat_par * np.array(lat_vecs) * bohr_to_angstrom
		return lat_vecs
	
	def read_atomic_positions(self):
		with open(self.filename, 'r') as f:	
			for line in f:
				if "Begin final coordinates" in line:
					f.readline()
					f.readline()
					atoms = []
					for _ in range(self.natm):
						tmp_line = f.readline()
						tmp_pos = re.findall('[0-9+\.[0-9]+', tmp_line)
						tmp_pos = [float(item) for item in tmp_pos]
						tmp_spe = re.match('[a-zA-Z]+', tmp_line).group()
						tmp_atom = atom(tmp_spe, tmp_pos, 0)
						atoms.append(tmp_atom)
		return atoms
	
	def get_cell(self):
		return self.cell

class read_input_QE:
	def __init__(self, filename):
		self.filename = filename
		self.num_format = re.compile('[+-]?[0-9]+\.[0-9]+')
		self.lat_vecs = []
		self.atoms = []

		self.get_lat_vecs()
		self.get_atoms()
		self.cell = cell(self.lat_vecs, self.atoms)

	def get_lat_vecs(self):
		with open(self.filename, 'r') as f:
			for line in f:
				if "CELL_PARAMETERS" in line:
					for i in range(3):
						temp_line = f.readline()
						temp = self.num_format.findall(temp_line)
						temp = [float(item) for item in temp]
						self.lat_vecs.append(temp)
	
	def get_atoms(self):
		with open(self.filename, 'r') as f:
			for line in f:
				if "ATOMIC_POSITIONS" in line:
					i = 1
					atoms = []
					for temp_line in f:
						temp_atm_pos = self.num_format.findall(temp_line)
						temp_atm_pos = [float(item) for item in temp_atm_pos]
						temp_spe = re.match('[a-zA-Z]+', temp_line).group()
						temp_atom = atom(temp_spe, temp_atm_pos, i)
						self.atoms.append(temp_atom)
						i += 1

	def get_cell(self):
		return self.cell
		

class print_POSCAR:
	def __init__(self, cell):
		self.atoms = cell.atoms
		self.lat_vecs = cell.lat_vecs

		self.species_tags = self.get_species_tags()
		self.print_all()
	
	def get_species_tags(self):
		species_tags = []

		top = 0 
		species_tags.append(species_tag(self.atoms[0].spe, 0))
		for atom in self.atoms:
			if atom.spe == species_tags[top].spe:
				species_tags[top].num += 1
			else :
				top += 1
				species_tags.append(species_tag(atom.spe, 1))

		return species_tags
	
	def print_all(self):
		print("POSCAR")
		print("1.0000000")

		for lat_vec in self.lat_vecs:
			for coordinate in lat_vec:
				print("%14.7f"%(coordinate), end = "")
			print("")

		for species_tag in self.species_tags:
			print("%-s "%(species_tag.spe), end = '')
		print("")
		for species_tag in self.species_tags:
			print("%-d "%(species_tag.num), end = '')
		print("")

		print("Direct")
		for atom in self.atoms:
			for coordinate in atom.pos:
				print("%14.7f"%(coordinate), end = "")
			print("")
