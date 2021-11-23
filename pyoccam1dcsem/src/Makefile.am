if X86_64
	AM_FCFLAGS = -m64
	AM_CXXFLAGS = -m64
endif
# Linker flags
AM_LDFLAGS = -framework Accelerate

lib_LTLIBRARIES = liboccam1dcsem.la
liboccam1dcsem_la_SOURCES = FilterModules.f90 Dipole1D.f90 CallDipole1D.f90
liboccam1dcsem_la_LDFLAGS = -version-info 0:1:0 -shared -rpath ${exec_prefix}/lib
