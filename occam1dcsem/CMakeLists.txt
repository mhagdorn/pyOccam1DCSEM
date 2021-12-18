include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/../src)

add_cython_target(_dipole)
add_library(_dipole MODULE ${_dipole})
python_extension_module(_dipole)
target_link_libraries(_dipole $<TARGET_OBJECTS:occam1dcsem>
  ${CMAKE_Fortran_IMPLICIT_LINK_LIBRARIES})

install(TARGETS _dipole LIBRARY DESTINATION occam1dcsem)
