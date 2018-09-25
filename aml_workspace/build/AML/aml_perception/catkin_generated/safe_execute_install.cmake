execute_process(COMMAND "/home/irlab/Projects/aml_workspace/build/AML/aml_perception/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/irlab/Projects/aml_workspace/build/AML/aml_perception/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
