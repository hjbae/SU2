#!/usr/bin/env python

# \file run_SU2.py
# \brief Python script to run WMLES cases using SU2 native flow solvers
# \author Jane Bae 
# \version 7.0.3 "Blackbird"
#
# SU2 Project Website: https://su2code.github.io
#
# The SU2 Project is maintained by the SU2 Foundation 
# (http://su2foundation.org)
#
# Copyright 2012-2020, SU2 Contributors (cf. AUTHORS.md)
#
# SU2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# SU2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SU2. If not, see <http://www.gnu.org/licenses/>.

import sys
import shutil
import pysu2 as pysu2          # imports the SU2 adjoint-wrapped module
from mpi4py import MPI

def main(comm):

  # Define the input file names
  flow_filename = "wmles_chan_re5200_v7.cfg"
  
  # Import communicators to run with parallel version of SU2
  #comm = MPI.COMM_WORLD
  rank = comm.Get_rank()

  # Initialize the flow driver of SU2, this includes solver preprocessing
  FlowDriver = pysu2.CSinglezoneDriver(flow_filename, 1, comm);
  FlowMarkerID = None
  FlowMarkerName = 'lower'                                            # wall marker
  FlowMarkerList = FlowDriver.GetAllBoundaryMarkersTag()              # Get all the flow boundary tags
  FlowMarkerIDs = FlowDriver.GetAllBoundaryMarkers()                  # Get all the associated indices to the flow markers
  if FlowMarkerName in FlowMarkerList and FlowMarkerName in FlowMarkerIDs.keys():
    FlowMarkerID = FlowMarkerIDs[FlowMarkerName]                      # Check if the flow FSI marker exists
  nVertex_Marker_Flow = FlowDriver.GetNumberVertices(FlowMarkerID)    # Get the number of vertices of the flow FSI marker

    
  print("\n------------------------------ Begin Solver -----------------------------\n")
  sys.stdout.flush()
  comm.Barrier()

  Flow_Time  = FlowDriver.GetTime_Iter()
  Flow_nTime = FlowDriver.GetnTimeIter()
    
  for i in range(Flow_nTime):
  
    # Time iteration preprocessing
    FlowDriver.Preprocess(Flow_Time+i)
    FlowDriver.Run()
    FlowDriver.Postprocess() 
    FlowDriver.Update()
    FlowDriver.Output(Flow_Time+i)
    stopCalc = FlowDriver.Monitor(Flow_Time+i)
    if stopCalc:
        break

    # Get relevant flow information at each vertex
    for j in range(nVertex_Marker_Flow):
       u  = FlowDriver.GetVelOffWall(FlowMarkerID,j,0)
       du = FlowDriver.GetVelGradOffWall(FlowMarkerID,j,0)
       y  = FlowDriver.GetVertexCoordY(FlowMarkerID,j)
       tauw = FlowDriver.GetTauWall_WMLES(FlowMarkerID,j)
    

# -------------------------------------------------------------------
#  Run Main Program
# -------------------------------------------------------------------

# this is only accessed if running from command prompt
if __name__ == '__main__':

    comm = MPI.COMM_WORLD
    main(comm)  
