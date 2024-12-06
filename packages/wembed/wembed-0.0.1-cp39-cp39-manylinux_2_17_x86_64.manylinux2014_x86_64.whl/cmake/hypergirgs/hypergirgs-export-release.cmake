#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "girgs::hypergirgs" for configuration "Release"
set_property(TARGET girgs::hypergirgs APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(girgs::hypergirgs PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libhypergirgs.so.1.0.2"
  IMPORTED_SONAME_RELEASE "libhypergirgs.so.1"
  )

list(APPEND _cmake_import_check_targets girgs::hypergirgs )
list(APPEND _cmake_import_check_files_for_girgs::hypergirgs "${_IMPORT_PREFIX}/lib/libhypergirgs.so.1.0.2" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
