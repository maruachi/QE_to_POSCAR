class atom:
	def __init__(self, spe, pos, index):
		self.spe = spe
		self.pos = pos
		self.index = index
	
	def show(self):
		print("%-4d"%(self.index), end = "")
		print("%2s"%(self.spe), end = "")
		for coordinate in self.pos:
			print("%16.9f"%(coordinate), end = "")
		print("")
	
	def print_POSCAR(self):
		for coordinate in self.pos:
			print("%16.9f"%(coordinate), end = "")
		print("")
	
class cell:
	def __init__(self, lat_vecs, atoms):
		self.lat_vecs = lat_vecs
		self.atoms = atoms
	
	def show(self):
		print("CELL_PARAMETERS angstrom")
		for lat_vec in self.lat_vecs:
			for coordinate in lat_vec:
				print("%16.9f"%(coordinate), end = "")
			print("")

		print("ATOMIC_POSITIONS (crystal)")
		for atom in self.atoms:
			atom.show()

class species_tag:
	def __init__(self, spe, num):
		self.spe = spe
		self.num = num
	
	def show(self):
		print("%s %d"%(self.spe, self.num))
