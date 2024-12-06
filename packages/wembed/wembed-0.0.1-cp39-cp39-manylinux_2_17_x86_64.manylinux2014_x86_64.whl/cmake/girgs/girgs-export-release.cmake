#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "girgs::girgs" for configuration "Release"
set_property(TARGET girgs::girgs APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(girgs::girgs PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgirgs.so.1.0.2"
  IMPORTED_SONAME_RELEASE "libgirgs.so.1"
  )

list(APPEND _cmake_import_check_targets girgs::girgs )
list(APPEND _cmake_import_check_files_for_girgs::girgs "${_IMPORT_PREFIX}/lib/libgirgs.so.1.0.2" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
