#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/irlab/Projects/aml_workspace/src/AML/aml_io"

# snsure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/irlab/Projects/aml_workspace/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/irlab/Projects/aml_workspace/install/lib/python2.7/dist-packages:/home/irlab/Projects/aml_workspace/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/irlab/Projects/aml_workspace/build" \
    "/usr/bin/python" \
    "/home/irlab/Projects/aml_workspace/src/AML/aml_io/setup.py" \
    build --build-base "/home/irlab/Projects/aml_workspace/build/AML/aml_io" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/irlab/Projects/aml_workspace/install" --install-scripts="/home/irlab/Projects/aml_workspace/install/bin"
