bsub -n 12 -W 24:00 -J SU2_test 'python /cluster/home/janbae/SU2/SU2-feature_WallModelLES/SU2_PY/parallel_computation.py --file=wmles_chan_re5200_v7.cfg -n 12'
