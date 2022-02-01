#!/bin/bash

module load python-3.7.7

for BLAH in *job ; do
  sbatch $BLAH
done
