#!/bin/bash

module load anaconda3

rm -rf POSCAR*

exec="python -m QE_to_POSCAR.run"

$exec 2> Guideline
$exec in relax.in > POSCAR_from_in
$exec scf scf.out > POSCAR_from_scf_out
$exec relax relax.out > POSCAR_from_relax_out
