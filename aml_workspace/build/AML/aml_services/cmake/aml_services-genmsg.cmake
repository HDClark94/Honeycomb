# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "aml_services: 0 messages, 4 services")

set(MSG_I_FLAGS "-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(aml_services_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictAction.srv" NAME_WE)
add_custom_target(_aml_services_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "aml_services" "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictAction.srv" ""
)

get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictState.srv" NAME_WE)
add_custom_target(_aml_services_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "aml_services" "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictState.srv" ""
)

get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/SendPisaHandCmd.srv" NAME_WE)
add_custom_target(_aml_services_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "aml_services" "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/SendPisaHandCmd.srv" ""
)

get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/ReadPisaHandCurr.srv" NAME_WE)
add_custom_target(_aml_services_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "aml_services" "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/ReadPisaHandCurr.srv" ""
)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services
_generate_srv_cpp(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictAction.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/aml_services
)
_generate_srv_cpp(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/ReadPisaHandCurr.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/aml_services
)
_generate_srv_cpp(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/SendPisaHandCmd.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/aml_services
)
_generate_srv_cpp(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictState.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/aml_services
)

### Generating Module File
_generate_module_cpp(aml_services
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/aml_services
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(aml_services_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(aml_services_generate_messages aml_services_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictAction.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_cpp _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictState.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_cpp _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/SendPisaHandCmd.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_cpp _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/ReadPisaHandCurr.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_cpp _aml_services_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(aml_services_gencpp)
add_dependencies(aml_services_gencpp aml_services_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS aml_services_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services
_generate_srv_lisp(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictAction.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/aml_services
)
_generate_srv_lisp(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/ReadPisaHandCurr.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/aml_services
)
_generate_srv_lisp(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/SendPisaHandCmd.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/aml_services
)
_generate_srv_lisp(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictState.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/aml_services
)

### Generating Module File
_generate_module_lisp(aml_services
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/aml_services
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(aml_services_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(aml_services_generate_messages aml_services_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictAction.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_lisp _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictState.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_lisp _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/SendPisaHandCmd.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_lisp _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/ReadPisaHandCurr.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_lisp _aml_services_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(aml_services_genlisp)
add_dependencies(aml_services_genlisp aml_services_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS aml_services_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages

### Generating Services
_generate_srv_py(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictAction.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services
)
_generate_srv_py(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/ReadPisaHandCurr.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services
)
_generate_srv_py(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/SendPisaHandCmd.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services
)
_generate_srv_py(aml_services
  "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictState.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services
)

### Generating Module File
_generate_module_py(aml_services
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(aml_services_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(aml_services_generate_messages aml_services_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictAction.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_py _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/PredictState.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_py _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/SendPisaHandCmd.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_py _aml_services_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/irlab/Projects/aml_workspace/src/AML/aml_services/srv/ReadPisaHandCurr.srv" NAME_WE)
add_dependencies(aml_services_generate_messages_py _aml_services_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(aml_services_genpy)
add_dependencies(aml_services_genpy aml_services_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS aml_services_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/aml_services)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/aml_services
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(aml_services_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/aml_services)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/aml_services
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(aml_services_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services
    DESTINATION ${genpy_INSTALL_DIR}
    # skip all init files
    PATTERN "__init__.py" EXCLUDE
    PATTERN "__init__.pyc" EXCLUDE
  )
  # install init files which are not in the root folder of the generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services
    DESTINATION ${genpy_INSTALL_DIR}
    FILES_MATCHING
    REGEX "${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/aml_services/.+/__init__.pyc?$"
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(aml_services_generate_messages_py std_msgs_generate_messages_py)
endif()
