#!/bin/bash

module load anaconda3

python ../run.py in relax.in > POSCAR_from_in
python ../run.py out relax.out > POSCAR_from_out
