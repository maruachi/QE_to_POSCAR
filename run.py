import sys
from .src.io_base import read_input_QE, read_relax_out_QE, print_POSCAR

sys.path.append('/home/maruachi/home-make_code/pyworks/QE_to_POSCAR/')

if len(sys.argv) != 3:
	print("python -m QE_to_POSCAR.run [option] [filename]", file = sys.stderr)
	print("This program is used to convert QE input or output files into POSCAR",
		 file = sys.stderr)
	print("QE pw.x input file option is \"in\"", file = sys.stderr)
	print("QE pw.x output file option is \"out\"", file = sys.stderr)
	exit()


file_format = sys.argv[1]
filename = sys.argv[2]

if file_format == 'in' :
	cell = read_input_QE(filename).get_cell()
elif file_format == 'out' :
	cell = read_relax_out_QE(filename).get_cell()
else:
	print("Invalid format input")
	exit()
print("There is no such filename: ", filename, sys.stderr)

print_POSCAR(cell)
