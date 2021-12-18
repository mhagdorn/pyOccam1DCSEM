cdef extern from "CallDipole1D.h":
   cpdef void c_initialiseDpl1D()
   cpdef int c_get_nTx()
   cpdef int c_get_nFreq()
   cpdef void c_CallDipole1D(int iTx, int iFreq)
   cpdef void c_close_outfile()
