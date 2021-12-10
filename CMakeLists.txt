cmake_minimum_required (VERSION 2.6)
project(occam1dcsem)
set (PROJECT_VERSION_MAJOR 7)
set (PROJECT_VERSION_MINOR 3)
set (PROJECT_VERSION_PATCH 0)
set (PROJECT_BUGREPORT "isloux@yahoo.co.uk")
set (PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")

enable_language (Fortran)

# make sure that the default is a RELEASE
if (NOT CMAKE_BUILD_TYPE)
  set (CMAKE_BUILD_TYPE RELEASE CACHE STRING
      "Choose the type of build, options are: None Debug Release."
      FORCE)
endif (NOT CMAKE_BUILD_TYPE)

# make sure all the built Fortran modules end up end the same place to ease
# installing them later
set (CMAKE_Fortran_MODULE_DIRECTORY ${CMAKE_BINARY_DIR}/mod_files)

set (INCLUDE_INSTALL_DIR include CACHE PATH
  "Location where include files will be installed relative to prefix")
set (BIN_INSTALL_DIR bin CACHE PATH
  "Location where executables will be installed relative to prefix")
set (LIB_INSTALL_DIR lib CACHE PATH
  "Location where library files will be installed relative to prefix")
set (MOD_INSTALL_DIR ${INCLUDE_INSTALL_DIR}/${PROJECT_NAME} CACHE PATH
  "Location where fortran mod files will be installed relative to prefix")


add_subdirectory (src)
