import sys
from src.io_base import read_input_QE, read_relax_out_QE, print_POSCAR

file_format = sys.argv[1]
filename = sys.argv[2]

if file_format == 'in' :
	cell = read_input_QE(filename).get_cell()
elif file_format == 'out' :
	cell = read_relax_out_QE(filename).get_cell()
else:
	print("Invalid format input")
	exit()

print_POSCAR(cell)
