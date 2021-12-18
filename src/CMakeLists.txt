# source code
set ( occam1dcsem_SOURCES FilterModules.f90
  Dipole1D.f90 CallDipole1D.f90)

# targets
add_library (occam1dcsem OBJECT ${occam1dcsem_SOURCES})

# install
install (TARGETS occam1dcsem
         RUNTIME DESTINATION ${BIN_INSTALL_DIR}
         LIBRARY DESTINATION ${LIB_INSTALL_DIR}
         PUBLIC_HEADER DESTINATION ${INCLUDE_INSTALL_DIR})

# install the mod files
#install (DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY}/
#  DESTINATION ${MOD_INSTALL_DIR})
# install the header
#install (FILES CallDipole1D.h DESTINATION ${INCLUDE_INSTALL_DIR})
